import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import json
import anthropic
from app.strategies.haiku_strategy import HaikuStrategy
from app.models.types import Move, RoundResult

# Test fixtures
@pytest.fixture
def mock_anthropic_client():
    with patch('anthropic.AsyncAnthropic') as mock:
        yield mock

@pytest.fixture
def strategy(mock_anthropic_client):
    return HaikuStrategy(
        name="Test Haiku",
        is_player1=True,
        api_key="fake-api-key"
    )

@pytest.fixture
def sample_round_result():
    return RoundResult(
        round_number=1,
        player1_move=Move.COOPERATE,
        player2_move=Move.DEFECT,
        player1_reasoning="Test reasoning",
        player2_reasoning="Test reasoning",
        player1_score=0,
        player2_score=5
    )

# Strategy initialization tests
def test_strategy_initialization():
    """Test basic strategy initialization"""
    strategy = HaikuStrategy("Test", True, "fake-key")
    assert strategy.name == "Test"
    assert strategy.is_player1 == True
    assert strategy.token_budget == 4000
    assert strategy.total_tokens_used == 0
    assert len(strategy.conversation_history) == 0

def test_strategy_initialization_no_api_key():
    """Test strategy fails with empty API key"""
    with pytest.raises(ValueError):
        HaikuStrategy("Test", True, "")

# History formatting tests
def test_format_empty_history(strategy):
    """Test history formatting with no previous rounds"""
    assert "No previous rounds played" in strategy._format_history()

def test_format_history_with_rounds(strategy, sample_round_result):
    """Test history formatting with previous rounds"""
    strategy._history.append(sample_round_result)
    history = strategy._format_history()
    
    assert "Round 1" in history
    assert "You played: cooperate" in history
    assert "Opponent played: defect" in history
    assert "Scores: You: 0, Opponent: 5" in history

# API response parsing tests
@pytest.mark.asyncio
async def test_valid_cooperate_response(strategy, mock_anthropic_client):
    """Test parsing a valid cooperative move response"""
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text=json.dumps({
        "move": "COOPERATE",
        "reasoning": "Test reasoning"
    }))]
    mock_response.usage.input_tokens = 50
    mock_response.usage.output_tokens = 30
    
    mock_client = AsyncMock()
    mock_client.messages.create.return_value = mock_response
    strategy.client = mock_client

    response = await strategy._get_ai_response(0)
    assert response.move == Move.COOPERATE
    assert response.reasoning == "Test reasoning"
    assert response.token_usage.total_tokens == 80

@pytest.mark.asyncio
async def test_valid_defect_response(strategy, mock_anthropic_client):
    """Test parsing a valid defect move response"""
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text=json.dumps({
        "move": "DEFECT",
        "reasoning": "Test reasoning"
    }))]
    mock_response.usage.input_tokens = 50
    mock_response.usage.output_tokens = 30
    
    mock_client = AsyncMock()
    mock_client.messages.create.return_value = mock_response
    strategy.client = mock_client

    response = await strategy._get_ai_response(0)
    assert response.move == Move.DEFECT
    assert response.token_usage.total_tokens == 80

# Error handling tests
@pytest.mark.asyncio
async def test_invalid_json_response(strategy, mock_anthropic_client):
    """Test handling of invalid JSON response"""
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="Invalid JSON")]
    
    mock_client = AsyncMock()
    mock_client.messages.create.return_value = mock_response
    strategy.client = mock_client

    with pytest.raises(ValueError, match="Failed to parse AI response"):
        await strategy._get_ai_response(0)

@pytest.mark.asyncio
async def test_missing_move_field(strategy, mock_anthropic_client):
    """Test handling of response missing required field"""
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text=json.dumps({
        "reasoning": "Test reasoning"
    }))]
    
    mock_client = AsyncMock()
    mock_client.messages.create.return_value = mock_response
    strategy.client = mock_client

    with pytest.raises(ValueError):
        await strategy._get_ai_response(0)

@pytest.mark.asyncio
async def test_invalid_move_value(strategy, mock_anthropic_client):
    """Test handling of invalid move value"""
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text=json.dumps({
        "move": "INVALID",
        "reasoning": "Test reasoning"
    }))]
    
    mock_client = AsyncMock()
    mock_client.messages.create.return_value = mock_response
    strategy.client = mock_client

    with pytest.raises(ValueError):
        await strategy._get_ai_response(0)

@pytest.mark.asyncio
async def test_api_error(strategy, mock_anthropic_client):
    """Test handling of API errors"""
    mock_client = AsyncMock()
    mock_request = MagicMock()
    mock_client.messages.create.side_effect = anthropic.APIError(
        message="API Error",
        request=mock_request,
        body={"error": {"message": "Test error"}}
    )
    strategy.client = mock_client

    with pytest.raises(ValueError, match="Anthropic API error"):
        await strategy._get_ai_response(0)

# Token budget tests
async def test_token_budget_tracking(strategy, mock_anthropic_client):
    """Test token budget is properly tracked"""
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text=json.dumps({
        "move": "COOPERATE",
        "reasoning": "Test reasoning"
    }))]
    mock_response.usage.input_tokens = 2000
    mock_response.usage.output_tokens = 1000
    
    mock_client = AsyncMock()
    mock_client.messages.create.return_value = mock_response
    strategy.client = mock_client

    # Use get_move() instead of _get_ai_response()
    move = await strategy.get_move(0)
    assert strategy.total_tokens_used == 3000
    
    # Second call should exceed budget
    with pytest.raises(ValueError, match="Token budget exceeded"):
        await strategy.get_move(1)

def test_reset_clears_token_count(strategy):
    """Test reset clears token usage"""
    strategy.total_tokens_used = 1000
    strategy.reset()
    assert strategy.total_tokens_used == 0

# Game integration tests
@pytest.mark.asyncio
async def test_full_game_round(strategy, mock_anthropic_client, sample_round_result):
    """Test strategy in a full game round context"""
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text=json.dumps({
        "move": "COOPERATE",
        "reasoning": "Test reasoning"
    }))]
    mock_response.usage.input_tokens = 50
    mock_response.usage.output_tokens = 30
    
    mock_client = AsyncMock()
    mock_client.messages.create.return_value = mock_response
    strategy.client = mock_client

    # Add some history
    strategy._history.append(sample_round_result)
    
    # Get move should work and update history
    move = await strategy.get_move(1)
    assert move == Move.COOPERATE
    assert len(strategy.conversation_history) == 1
    assert strategy.total_tokens_used == 80