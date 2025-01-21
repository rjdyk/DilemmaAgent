from flask import Blueprint, request, jsonify
from flask_cors import CORS
from typing import Dict
from uuid import uuid4

# Import our custom classes
from app.models.game import Game
from app.strategies import StrategyType, create_strategy, get_available_strategies
from app.utils.storage import GameStorage
from app.utils.history import GameHistory


bp = Blueprint('api', __name__)

# Initialize storage
game_storage = GameStorage()
game_history = GameHistory()

# Error handlers
@bp.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Resource not found"}), 404

@bp.errorhandler(400)
def bad_request_error(error):
    return jsonify({"error": str(error)}), 400

@bp.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

@bp.errorhandler(ValueError)
def value_error(error):
    return jsonify({"error": str(error)}), 400

# Routes
@bp.route('/api/strategies', methods=['GET'])
def get_strategies():
    """Get list of available opponent strategies"""
    strategies = get_available_strategies()
    return jsonify({
        "strategies": [
            {"id": strategy.value, "name": strategy.value.replace('_', ' ').title()}
            for strategy in strategies
        ]
    })

@bp.route('/api/game/new', methods=['POST'])
def create_game():
    """Create a new game with specified strategy"""
    try:
        # Get strategy from request
        data = request.get_json()
        if 'strategy' not in data:
            return jsonify({"error": "Strategy not specified"}), 400
            
        # Create strategy instance
        strategy_type = StrategyType(data['strategy'])
        strategy = create_strategy(strategy_type)
        
        # Create and store new game
        game_id, game = game_storage.create_game(strategy)
        
        return jsonify({
            "game_id": game_id,
            "status": "created",
            "current_round": 0,
            "max_rounds": game.max_rounds
        })
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@bp.route('/api/game/<game_id>/state', methods=['GET'])
def get_game_state(game_id: str):
    """Get current state of specified game"""
    # Get game from active storage
    game = game_storage.get_game(game_id)
    if not game:
        return jsonify({"error": "Game not found"}), 404
        
    return jsonify({
        "game_id": game_id,
        "current_round": game.current_round,
        "max_rounds": game.max_rounds,
        "is_game_over": game.is_game_over(),
        "scores": {
            "ai": game.ai_total_score,
            "opponent": game.opponent_total_score
        }
    })

@bp.route('/api/game/<game_id>/move', methods=['POST'])
def make_move(game_id: str):
    """Process an AI move in the specified game"""
    # Get game from active storage
    game = game_storage.get_game(game_id)
    if not game:
        return jsonify({"error": "Game not found"}), 404
    
    try:
        # Get move from request
        data = request.get_json()
        if 'move' not in data or 'reasoning' not in data:
            return jsonify({"error": "Move or reasoning not specified"}), 400
        
        # Validate move value
        valid_moves = ['cooperate', 'defect']
        if data['move'].lower() not in valid_moves:
            return jsonify({"error": f"Invalid move. Must be one of: {', '.join(valid_moves)}"}), 400
         
            
        # Process the move
        result = game.process_round(data['move'].lower(), data['reasoning'])

        # Validate result object
        if not result:
            return jsonify({"error": "Failed to process round"}), 500
            
        # Validate required attributes
        required_attrs = ['round_number', 'ai_move', 'opponent_move', 'ai_score', 'opponent_score']
        missing_attrs = [attr for attr in required_attrs if not hasattr(result, attr)]
        if missing_attrs:
            return jsonify({
                "error": f"Invalid round result - missing attributes: {', '.join(missing_attrs)}"
            }), 500
        
        # Check if game is over
        if game.is_game_over():
            # Save to history and remove from active games
            game_history.save_game(game_id, game)
            game_storage.remove_game(game_id)
            
        # Return round result
        return jsonify({
            "round_number": result.round_number,
            "ai_move": result.ai_move,
            "opponent_move": result.opponent_move,
            "ai_score": result.ai_score,
            "opponent_score": result.opponent_score,
            "game_over": game.is_game_over(),
            "scores": {
                "ai": game.ai_total_score,
                "opponent": game.opponent_total_score
            }
        })
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

@bp.route('/api/game/<game_id>/history', methods=['GET'])
def get_game_history(game_id: str):
    """Get full history of specified game"""
    # First check active games
    game = game_storage.get_game(game_id)
    if game:
        # Game is still active, return current rounds
        rounds = [
            {
                "round_number": r.round_number,
                "ai_move": r.ai_move,
                "opponent_move": r.opponent_move,
                "ai_reasoning": r.ai_reasoning,
                "ai_score": r.ai_score,
                "opponent_score": r.opponent_score
            }
            for r in game.rounds
        ]
        
        return jsonify({
            "game_id": game_id,
            "is_active": True,
            "rounds": rounds,
            "scores": {
                "ai": game.ai_total_score,
                "opponent": game.opponent_total_score
            }
        })
    
    # If not in active games, check history
    completed_game = game_history.get_game(game_id)
    if completed_game:
        return jsonify({
            "game_id": game_id,
            "is_active": False,
            "rounds": completed_game["rounds"],
            "final_scores": completed_game["final_scores"]
        })
        
    return jsonify({"error": "Game not found"}), 404


