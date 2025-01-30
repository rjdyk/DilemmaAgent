# tests/test_ai_strategy.py
import pytest
import asyncio
from dataclasses import asdict, dataclass
from app.models.types import Move, TokenUsage
from app.strategies.ai_strategy import AIStrategy, AIResponse

class MockAIStrategy(AIStrategy):
    def __init__(self, name="Mock AI", is_player1=True, should_fail=False, token_budget=4000):
        super().__init__(name=name, is_player1=is_player1, token_budget=token_budget)
        self.should_fail = should_fail
        
    async def _get_ai_response(self, current_round: int) -> AIResponse:
        # Check token budget here instead
        if self.total_tokens_used + 100 > self.token_budget:
            raise ValueError("Token budget exceeded")
            
        if self.should_fail:
            raise Exception("Simulated API failure")
            
        return AIResponse(
            move=Move.COOPERATE,
            reasoning="Test reasoning",
            token_usage=TokenUsage(100, 50, 150)
        )

@pytest.mark.asyncio
async def test_ai_strategy_basic_move():
    strategy = MockAIStrategy()
    move = await strategy.get_move(0)
    
    assert move == Move.COOPERATE
    assert strategy.total_tokens_used == 150
    assert len(strategy.conversation_history) == 1
    assert strategy.last_error is None

@pytest.mark.asyncio
async def test_ai_strategy_token_budget():
    strategy = MockAIStrategy(token_budget=100)  # Set low budget
    move = await strategy.get_move(0)
    
    assert move == Move.COOPERATE  # Should get fallback move
    assert "Token budget exceeded" in strategy.last_error
    assert len(strategy.conversation_history) == 1

@pytest.mark.asyncio
async def test_ai_strategy_retries():
    strategy = MockAIStrategy(should_fail=True)
    move = await strategy.get_move(0)
    
    assert move == Move.COOPERATE  # Should get fallback move
    assert "Failed after 3 attempts" in strategy.last_error
    assert len(strategy.conversation_history) == 1

@pytest.mark.asyncio
async def test_ai_strategy_reset():
    strategy = MockAIStrategy()
    await strategy.get_move(0)
    strategy.reset()
    
    assert strategy.total_tokens_used == 0
    assert len(strategy.conversation_history) == 0
    assert strategy.last_error is None