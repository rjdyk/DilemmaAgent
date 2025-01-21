# tests/test_storage.py
import pytest
from app.utils.storage import GameStorage
from app.utils.history import GameHistory
from app.models.game import Game
from app.strategies.always_cooperate import AlwaysCooperate

@pytest.fixture
def storage():
    """Provide a fresh GameStorage instance for each test"""
    return GameStorage()

@pytest.fixture
def history(tmp_path):
    """Provide a GameHistory instance using a temporary directory"""
    history_file = tmp_path / "test_history.json"
    return GameHistory(str(history_file))

def test_game_storage_creation(storage):
    """Test creating and retrieving a game"""
    strategy = AlwaysCooperate()
    game_id, game = storage.create_game(strategy)
    
    assert game_id is not None
    assert storage.get_game(game_id) is game

def test_game_storage_removal(storage):
    """Test removing a game from storage"""
    strategy = AlwaysCooperate()
    game_id, _ = storage.create_game(strategy)
    
    storage.remove_game(game_id)
    assert storage.get_game(game_id) is None

def test_game_history_save_and_retrieve(history):
    """Test saving and retrieving a completed game"""
    strategy = AlwaysCooperate()
    game = Game(strategy)
    game_id = "test_id"
    
    # Play a round
    game.process_round("cooperate", "Test reasoning")
    game.game_over = True
    
    # Save game
    history.save_game(game_id, game)
    
    # Retrieve game
    saved_game = history.get_game(game_id)
    assert saved_game is not None
    assert saved_game["game_id"] == game_id
    assert len(saved_game["rounds"]) == 1