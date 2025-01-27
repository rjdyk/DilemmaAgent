from flask import Blueprint, request, jsonify
from flask_cors import CORS
from typing import Dict
from uuid import uuid4

# Import our custom classes
from app.models.game import Game
from app.strategies import StrategyType, create_strategy, get_available_strategies
from app.utils.storage import GameStorage
from app.utils.history import GameHistory

bp = Blueprint('api', __name__, url_prefix='/api')

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
@bp.route('/strategies', methods=['GET'])
def get_strategies():
    """Get list of available opponent strategies"""
    strategies = get_available_strategies()
    return jsonify({
        "strategies": [
            {"id": strategy.value, "name": strategy.value.replace('_', ' ').title()}
            for strategy in strategies
        ]
    })

@bp.route('/game/new', methods=['POST'])
def create_game():
    """Create a new game with two specified strategies"""
    try:
        # Get strategies from request
        data = request.get_json()
        if 'player1Strategy' not in data or 'player2Strategy' not in data:
            return jsonify({"error": "Both player strategies must be specified"}), 400
        # Get rounds parameter with default of 10
        rounds = int(data.get('rounds', 10))
        if rounds < 1:
            return jsonify({"error": "Rounds must be at least 1"}), 400
        
        # Create strategy instances
        strategy1_type = StrategyType(data['player1Strategy'])
        strategy2_type = StrategyType(data['player2Strategy'])
        strategy1 = create_strategy(strategy1_type, is_player1=True)
        strategy2 = create_strategy(strategy2_type, is_player1=False)
        
        # Create and store new game
        game_id, game = game_storage.create_game(strategy1, strategy2, max_rounds=rounds)

        print(f"Created game {game_id}, stored in game_storage:", game_storage.active_games)
 
        return jsonify({
            "game_id": game_id,
            "status": "created",
            "current_round": 0,
            "max_rounds": game.max_rounds,
            "player1_strategy": strategy1_type.value,
            "player2_strategy": strategy2_type.value,
            "strategy_names": {
                "player1": strategy1.name,
                "player2": strategy2.name
            }
        })
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@bp.route('/game/<game_id>/state', methods=['GET'])
def get_game_state(game_id: str):
    """Get current state of specified game"""
    game = game_storage.get_game(game_id)
    if not game:
        return jsonify({"error": "Game not found"}), 404
        
    return jsonify({
        "game_id": game_id,
        "current_round": game.current_round,
        "max_rounds": game.max_rounds,
        "is_game_over": game.is_game_over(),
        "scores": {
            "player1": game.player1_total_score,
            "player2": game.player2_total_score
        }
    })

@bp.route('/game/<game_id>/move', methods=['POST'])
def make_move(game_id: str):
    """Process a round in the specified game"""
    game = game_storage.get_game(game_id)
    if not game:
        return jsonify({"error": "Game not found"}), 404
    
    try:
        # Process the round - moves come from strategies
        result = game.process_round()
        print(f"Round result: P1 move: {result.player1_move}, P2 move: {result.player2_move}")
        if not result:
            return jsonify({"error": "Failed to process round"}), 500

        # Check if game is over
        if game.is_game_over():
            # Save to history and remove from active games
            game_history.save_game(game_id, game)
            game_storage.remove_game(game_id)
            
        # Return round result
        return jsonify({
            "round_number": result.round_number,
            "player1_move": result.player1_move.value,
            "player2_move": result.player2_move.value,
            "player1_score": result.player1_score,
            "player2_score": result.player2_score,
            "game_over": game.is_game_over(),
            "scores": {
                "player1": game.player1_total_score,
                "player2": game.player2_total_score
            }
        })
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    
@bp.route('/game/<game_id>/complete', methods=['POST'])
def complete_game(game_id: str):
    """Auto-complete all remaining rounds in the game"""

    game = game_storage.get_game(game_id)
    if not game:
        return jsonify({"error": "Game not found"}), 404
        
    try:
        # Run all remaining rounds
        round_results = game.run_all_rounds()
        
        # Save completed game to history and remove from active storage
        game_history.save_game(game_id, game)
        game_storage.remove_game(game_id)
        
        return jsonify({
            "rounds": [
                {
                    "round_number": r.round_number,
                    "player1_move": r.player1_move.value,
                    "player2_move": r.player2_move.value,
                    "player1_score": r.player1_score,
                    "player2_score": r.player2_score
                }
                for r in round_results
            ],
            "final_scores": {
                "player1": game.player1_total_score,
                "player2": game.player2_total_score  
            }
        })
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@bp.route('/game/<game_id>/history', methods=['GET'])
def get_game_history(game_id: str):
    """Get full history of specified game"""
    # First check active games
    game = game_storage.get_game(game_id)
    if game:
        # Game is still active, return current rounds
        rounds = [
            {
                "round_number": r.round_number,
                "player1_move": r.player1_move.value,
                "player2_move": r.player2_move.value,
                "player1_reasoning": r.player1_reasoning,
                "player2_reasoning": r.player2_reasoning,
                "player1_score": r.player1_score,
                "player2_score": r.player2_score
            }
            for r in game.rounds
        ]
        
        # Add payoff matrix to response
        matrix = {
            "cooperate_cooperate": game.payoff_matrix.cooperate_cooperate,
            "cooperate_defect": game.payoff_matrix.cooperate_defect,
            "defect_cooperate": game.payoff_matrix.defect_cooperate,
            "defect_defect": game.payoff_matrix.defect_defect
        }
        
        return jsonify({
            "game_id": game_id,
            "is_active": True,
            "rounds": rounds,
            "scores": {
                "player1": game.player1_total_score,
                "player2": game.player2_total_score
            },
            "payoff_matrix": matrix
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