# tests/test_api.py
import pytest
from app import create_app
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
                         json={
                             "player1Strategy": "always_cooperate",
                             "player2Strategy": "always_cooperate"
                         })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "game_id" in data
    assert data["current_round"] == 0
    assert data["player1_strategy"] == "always_cooperate"
    assert data["player2_strategy"] == "always_cooperate"

def test_make_move(client):
    """Test making a move in a game"""
    # First create a game
    response = client.post('/api/game/new', 
                         json={
                             "player1Strategy": "always_cooperate",
                             "player2Strategy": "always_cooperate"
                         })
    assert response.status_code == 200
    game_id = json.loads(response.data)["game_id"]
    
    # Make a move
    response = client.post(f'/api/game/{game_id}/move',
                         json={"auto_play": True})  # Since moves now come from strategies
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["round_number"] == 1
    assert "player1_move" in data
    assert "player2_move" in data
    assert "player1_score" in data
    assert "player2_score" in data

def test_game_not_found(client):
    """Test handling of non-existent game"""
    response = client.get('/api/game/nonexistent/state')
    assert response.status_code == 404

def test_get_game_state(client):
    """Test getting current game state"""
    # Create game
    response = client.post('/api/game/new',
                         json={
                             "player1Strategy": "always_cooperate",
                             "player2Strategy": "always_cooperate"
                         })
    game_id = json.loads(response.data)["game_id"]
    
    # Get state
    response = client.get(f'/api/game/{game_id}/state')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["current_round"] == 0
    assert data["scores"]["player1"] == 0
    assert data["scores"]["player2"] == 0

def test_create_game_missing_strategy(client):
    """Test error handling when strategy is missing"""
    response = client.post('/api/game/new',
                         json={"player1Strategy": "always_cooperate"})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data

def test_create_game_invalid_strategy(client):
    """Test error handling when strategy is invalid"""
    response = client.post('/api/game/new',
                         json={
                             "player1Strategy": "invalid_strategy",
                             "player2Strategy": "always_cooperate"
                         })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data