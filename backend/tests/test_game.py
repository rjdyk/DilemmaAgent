import pytest
from app.models.game import Game, Move
from app.strategies.base import BaseStrategy
from app.strategies.always_cooperate import AlwaysCooperate

def test_game_initialization():
    """Test that a new game is properly initialized"""
    strategy = AlwaysCooperate()
    game = Game(strategy)
    
    assert game.current_round == 0
    assert game.max_rounds == 10
    assert game.game_over == False
    assert len(game.rounds) == 0
    assert game.ai_total_score == 0
    assert game.opponent_total_score == 0

def test_valid_move_processing():
    """Test that a valid move is properly processed"""
    strategy = AlwaysCooperate()  # Will always cooperate
    game = Game(strategy)
    
    # Process one round where AI cooperates
    result = game.process_round("cooperate", "Test reasoning")
    
    assert result is not None
    assert result.round_number == 1
    assert result.ai_move == Move.COOPERATE
    assert result.opponent_move == Move.COOPERATE
    assert result.ai_score == 3  # Both cooperated, so both get 3 points
    assert result.opponent_score == 3
    assert game.current_round == 1
    assert len(game.rounds) == 1

def test_invalid_move():
    """Test that invalid moves are rejected"""
    strategy = AlwaysCooperate()
    game = Game(strategy)
    
    result = game.process_round("invalid_move", "Test reasoning")
    assert result is None
    assert game.current_round == 0
    assert len(game.rounds) == 0