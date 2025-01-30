import pytest
from app.models.game import Game, Move
from app.strategies.base import BaseStrategy
from app.strategies.always_cooperate import AlwaysCooperate
from app.strategies.haiku_strategy import HaikuStrategy
from unittest.mock import AsyncMock, patch



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

@pytest.mark.asyncio
async def test_valid_move_processing():
    """Test that a valid move is properly processed"""
    player1_strategy = AlwaysCooperate(is_player1=True)  
    player2_strategy = AlwaysCooperate(is_player1=False)  
    game = Game(player1_strategy, player2_strategy)
    
    # Process one round - both should cooperate based on their strategies
    result = await game.process_round()
    
    assert result is not None
    assert result.round_number == 1
    assert result.player1_move == Move.COOPERATE
    assert result.player2_move == Move.COOPERATE
    assert result.player1_score == 3  # Both cooperated, so both get 3 points
    assert result.player2_score == 3
    assert game.current_round == 1
    assert len(game.rounds) == 1

@pytest.mark.asyncio
async def test_player_moves():
    """Test that both players' strategies are correctly used"""
    player1_strategy = AlwaysCooperate(is_player1=True)
    player2_strategy = AlwaysCooperate(is_player1=False)
    game = Game(player1_strategy, player2_strategy)
    
    move1 = await game.get_player1_move()
    move2 = await game.get_player2_move()
    
    assert move1 == Move.COOPERATE
    assert move2 == Move.COOPERATE

@pytest.mark.asyncio
async def test_game_over():
    """Test that game ends after max rounds"""
    player1_strategy = AlwaysCooperate(is_player1=True)
    player2_strategy = AlwaysCooperate(is_player1=False)
    game = Game(player1_strategy, player2_strategy)
    
    # Play max_rounds
    for _ in range(game.max_rounds):
        await game.process_round()
        
    assert game.is_game_over()
    
    # Should not be able to play another round
    with pytest.raises(ValueError):
        await game.process_round()

@pytest.mark.asyncio
async def test_run_all_rounds():
    """Test running all rounds automatically"""
    player1_strategy = AlwaysCooperate(is_player1=True)
    player2_strategy = AlwaysCooperate(is_player1=False)
    game = Game(player1_strategy, player2_strategy)
    
    results = await game.run_all_rounds()
    
    assert len(results) == game.max_rounds
    assert game.is_game_over()
    assert game.current_round == game.max_rounds
    assert game.player1_total_score == 30  # 10 rounds * 3 points per round
    assert game.player2_total_score == 30
    
    # Should not be able to run again
    with pytest.raises(ValueError):
        await game.run_all_rounds()

@pytest.mark.asyncio
async def test_run_all_rounds_partial():
    """Test running remaining rounds after some manual rounds"""
    player1_strategy = AlwaysCooperate(is_player1=True)
    player2_strategy = AlwaysCooperate(is_player1=False)
    game = Game(player1_strategy, player2_strategy)
    
    # Play 3 rounds manually
    for _ in range(3):
        await game.process_round()
        
    results = await game.run_all_rounds()
    
    assert len(results) == 7  # Should complete remaining 7 rounds
    assert game.is_game_over()
    assert game.current_round == game.max_rounds

@pytest.fixture
def mock_haiku_strategy():
    with patch('app.strategies.haiku_strategy.HaikuStrategy') as MockStrategy:
        # Create a class that inherits from AIStrategy
        from app.strategies.ai_strategy import AIStrategy
        
        class MockHaikuStrategy(AIStrategy):
            def __init__(self):
                super().__init__("Test Haiku", True)
                self.model_name = "claude-3-haiku"
                self.conversation_history = [{"reasoning": "Test reasoning"}]
                self.total_tokens_used = 100
                
            async def _get_ai_response(self, current_round):
                return AsyncMock()

        return MockHaikuStrategy()

@pytest.fixture
def mock_haiku_strategy():
    from app.strategies.ai_strategy import AIStrategy, AIResponse
    from app.models.types import Move, TokenUsage
    
    class MockHaikuStrategy(AIStrategy):
        def __init__(self):
            super().__init__("Test Haiku", True)
            self.model_name = "claude-3-haiku"
            self.conversation_history = [{"reasoning": "Test reasoning"}]
            self.total_tokens_used = 100
                
        async def get_move(self, current_round: int) -> Move:
            # Override to avoid fallback behavior
            self.conversation_history = [{"reasoning": "Test reasoning"}]
            return Move.COOPERATE

        async def _get_ai_response(self, current_round):
            # This won't be called due to overridden get_move
            return AIResponse(
                move=Move.COOPERATE,
                reasoning="Test reasoning",
                token_usage=TokenUsage(100, 0, 100)
            )

    return MockHaikuStrategy()

@pytest.mark.asyncio
async def test_game_with_ai_player(mock_haiku_strategy):
    """Test game with one AI player"""
    player2_strategy = AlwaysCooperate(is_player1=False)
    game = Game(mock_haiku_strategy, player2_strategy)
    
    assert game.has_ai_player == True
    assert game.player1_model == "claude-3-haiku"
    assert game.player2_model is None
    
    result = await game.process_round()
    
    assert result.token_usage is not None
    assert result.player1_reasoning == "Test reasoning"
    assert result.token_usage.prompt_tokens == 100