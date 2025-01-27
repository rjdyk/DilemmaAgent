import pytest
from app.models.game import Game, Move
from app.strategies.base import BaseStrategy
from app.strategies.always_cooperate import AlwaysCooperate

def test_game_initialization():
    """Test that a new game is properly initialized"""
    player1_strategy = AlwaysCooperate(is_player1=True)
    player2_strategy = AlwaysCooperate(is_player1=False)
    game = Game(player1_strategy, player2_strategy)
    
    assert game.current_round == 0
    assert game.max_rounds == 10
    assert game.game_over == False
    assert len(game.rounds) == 0
    assert game.player1_total_score == 0
    assert game.player2_total_score == 0

def test_valid_move_processing():
    """Test that a valid move is properly processed"""
    player1_strategy = AlwaysCooperate(is_player1=True)  
    player2_strategy = AlwaysCooperate(is_player1=False)  
    game = Game(player1_strategy, player2_strategy)
    
    # Process one round - both should cooperate based on their strategies
    result = game.process_round()
    
    assert result is not None
    assert result.round_number == 1
    assert result.player1_move == Move.COOPERATE
    assert result.player2_move == Move.COOPERATE
    assert result.player1_score == 3  # Both cooperated, so both get 3 points
    assert result.player2_score == 3
    assert game.current_round == 1
    assert len(game.rounds) == 1

def test_player_moves():
    """Test that both players' strategies are correctly used"""
    player1_strategy = AlwaysCooperate(is_player1=True)
    player2_strategy = AlwaysCooperate(is_player1=False)
    game = Game(player1_strategy, player2_strategy)
    
    move1 = game.get_player1_move()
    move2 = game.get_player2_move()
    
    assert move1 == Move.COOPERATE
    assert move2 == Move.COOPERATE

def test_game_over():
    """Test that game ends after max rounds"""
    player1_strategy = AlwaysCooperate(is_player1=True)
    player2_strategy = AlwaysCooperate(is_player1=False)
    game = Game(player1_strategy, player2_strategy)
    
    # Play max_rounds
    for _ in range(game.max_rounds):
        game.process_round()
        
    assert game.is_game_over()
    
    # Should not be able to play another round
    with pytest.raises(ValueError):
        game.process_round()

def test_run_all_rounds():
    """Test running all rounds automatically"""
    player1_strategy = AlwaysCooperate(is_player1=True)
    player2_strategy = AlwaysCooperate(is_player1=False)
    game = Game(player1_strategy, player2_strategy)
    
    results = game.run_all_rounds()
    
    assert len(results) == game.max_rounds
    assert game.is_game_over()
    assert game.current_round == game.max_rounds
    assert game.player1_total_score == 30  # 10 rounds * 3 points per round
    assert game.player2_total_score == 30
    
    # Should not be able to run again
    with pytest.raises(ValueError):
        game.run_all_rounds()

def test_run_all_rounds_partial():
    """Test running remaining rounds after some manual rounds"""
    player1_strategy = AlwaysCooperate(is_player1=True)
    player2_strategy = AlwaysCooperate(is_player1=False)
    game = Game(player1_strategy, player2_strategy)
    
    # Play 3 rounds manually
    for _ in range(3):
        game.process_round()
        
    results = game.run_all_rounds()
    
    assert len(results) == 7  # Should complete remaining 7 rounds
    assert game.is_game_over()
    assert game.current_round == game.max_rounds