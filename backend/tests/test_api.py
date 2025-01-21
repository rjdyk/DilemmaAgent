# tests/test_api.py
import pytest
from app import create_app  # You'll need to modify your app structure to support this
import json

@pytest.fixture
def client():
    """Create a test client using an app configured for testing"""
    app = create_app(testing=True)
    with app.test_client() as client:
        yield client

def test_get_strategies(client):
    """Test retrieving available strategies"""
    response = client.get('/api/strategies')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "strategies" in data
    assert len(data["strategies"]) > 0

def test_create_game(client):
    """Test creating a new game"""
    response = client.post('/api/game/new', 
                         json={"strategy": "always_cooperate"})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "game_id" in data
    assert data["current_round"] == 0

def test_make_move(client):
    """Test making a move in a game"""
    # First create a game
    response = client.post('/api/game/new', 
                         json={"strategy": "always_cooperate"})
    game_id = json.loads(response.data)["game_id"]
    
    # Make a move
    response = client.post(f'/api/game/{game_id}/move',
                         json={"move": "cooperate", 
                              "reasoning": "Test move"})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["round_number"] == 1
    assert "ai_move" in data
    assert "opponent_move" in data

def test_game_not_found(client):
    """Test handling of non-existent game"""
    response = client.get('/api/game/nonexistent/state')
    assert response.status_code == 404

def test_invalid_move(client):
    """Test handling of invalid move"""
    # Create game
    response = client.post('/api/game/new', 
                         json={"strategy": "always_cooperate"})
    game_id = json.loads(response.data)["game_id"]
    
    # Make invalid move
    response = client.post(f'/api/game/{game_id}/move',
                         json={"move": "invalid_move", 
                              "reasoning": "Test move"})
    assert response.status_code == 400