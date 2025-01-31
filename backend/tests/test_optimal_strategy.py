# In tests/test_optimal_strategy.py

import pytest
from app.strategies.optimal_strategy import OptimalStrategy
from app.models.types import Move, MatrixType

def test_pure_defection_strategy():
    """Test optimal strategy with pure defection matrix"""
    strategy = OptimalStrategy(MatrixType.PURE_DEFECT, is_player1=True)
    # Should always defect
    for _ in range(100):
        assert strategy.get_move(0) == Move.DEFECT

def test_pure_cooperation_strategy():
    """Test optimal strategy with stag hunt matrix"""
    strategy = OptimalStrategy(MatrixType.STAG_HUNT, is_player1=True)
    # Should always cooperate
    for _ in range(100):
        assert strategy.get_move(0) == Move.COOPERATE

def test_mixed_strategy():
    """Test optimal strategy with mixed strategy matrix"""
    strategy = OptimalStrategy(MatrixType.MIXED_30, is_player1=True)
    
    # Run many trials to check cooperation rate
    num_trials = 10000
    cooperate_count = sum(
        1 for _ in range(num_trials) 
        if strategy.get_move(0) == Move.COOPERATE
    )
    
    # Check if cooperation rate is close to 30%
    cooperation_rate = cooperate_count / num_trials
    assert 0.28 <= cooperation_rate <= 0.32  # Allow small deviation

def test_strategy_name():
    """Test strategy name includes matrix type"""
    strategy = OptimalStrategy(MatrixType.MIXED_70, is_player1=True)
    assert "Optimal" in strategy.name
    assert "mixed_70" in strategy.name.lower()

def test_reset():
    """Test reset doesn't break strategy"""
    strategy = OptimalStrategy(MatrixType.MIXED_30, is_player1=True)
    strategy.get_move(0)  # Make a move
    strategy.reset()  # Reset
    # Should still work
    assert strategy.get_move(0) in [Move.COOPERATE, Move.DEFECT]