import pytest
from pathlib import Path
import json
from app.utils.history import GameHistory
from app.models.game import Game
from app.strategies.ai_strategy import AIStrategy, AIResponse
from app.models.types import Move, RoundResult
from datetime import datetime

class MockGame:
    def __init__(self, use_ai=False):
        self.timestamp = datetime.now()
        self.player1_strategy = MockAIStrategy() if use_ai else MockRegularStrategy()
        self.player2_strategy = MockRegularStrategy()
        self.player1_total_score = 10
        self.player2_total_score = 5
        self.rounds = [
            RoundResult(
                round_number=1,
                player1_move=Move.COOPERATE,
                player2_move=Move.DEFECT,
                player1_reasoning="Test reasoning",
                player2_reasoning="Regular strategy",
                player1_score=0,
                player2_score=5
            )
        ]
        self.payoff_matrix = MockPayoffMatrix()

class MockAIStrategy(AIStrategy):
    """Mock AI strategy for testing"""
    def __init__(self, name="Mock AI", is_player1=True, should_fail=False):
        super().__init__(name, is_player1)
        self.should_fail = should_fail
        
    async def _get_ai_response(self, current_round: int) -> AIResponse:
        if self.should_fail:
            raise Exception("Simulated API failure")
            
        return AIResponse(
            move=Move.COOPERATE,
            reasoning="Test reasoning",
            token_usage=TokenUsage(100, 50, 150)
        )

class MockRegularStrategy:
    def __init__(self):
        self.__class__.__name__ = "RegularStrategy"

class MockPayoffMatrix:
    def __init__(self):
        self.cooperate_cooperate = (3, 3)
        self.cooperate_defect = (0, 5)
        self.defect_cooperate = (5, 0)
        self.defect_defect = (1, 1)

@pytest.fixture
def temp_history_file(tmp_path):
    return tmp_path / "test_history.json"

def test_history_initialization(temp_history_file):
    history = GameHistory(storage_path=str(temp_history_file))
    assert temp_history_file.exists()
    data = json.loads(temp_history_file.read_text())
    assert "completed_games" in data

def test_save_regular_game(temp_history_file):
    history = GameHistory(storage_path=str(temp_history_file))
    game = MockGame(use_ai=False)
    history.save_game("test_id", game)
    
    saved_data = json.loads(temp_history_file.read_text())
    saved_game = saved_data["completed_games"][0]
    
    assert saved_game["game_id"] == "test_id"
    assert saved_game["player1_strategy"] == "RegularStrategy"
    assert "player1_ai_data" not in saved_game

def test_save_ai_game(temp_history_file):
    history = GameHistory(storage_path=str(temp_history_file))
    game = MockGame(use_ai=True)
    history.save_game("test_id", game)
    
    saved_data = json.loads(temp_history_file.read_text())
    saved_game = saved_data["completed_games"][0]
    
    assert saved_game["game_id"] == "test_id"
    assert "player1_ai_data" in saved_game
    assert "total_tokens" in saved_game["player1_ai_data"]
    assert "conversation_history" in saved_game["player1_ai_data"]

def test_get_game(temp_history_file):
    history = GameHistory(storage_path=str(temp_history_file))
    game = MockGame()
    history.save_game("test_id", game)
    
    retrieved_game = history.get_game("test_id")
    assert retrieved_game is not None
    assert retrieved_game["game_id"] == "test_id"

def test_get_nonexistent_game(temp_history_file):
    history = GameHistory(storage_path=str(temp_history_file))
    retrieved_game = history.get_game("nonexistent_id")
    assert retrieved_game is None