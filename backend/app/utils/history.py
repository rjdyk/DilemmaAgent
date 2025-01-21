# utils/history.py
import json
from datetime import datetime
from pathlib import Path
from app.models.game import Game

class GameHistory:
    def __init__(self, storage_path: str = "game_history.json"):
        self.storage_path = Path(storage_path)
        self._initialize_storage()
    
    def _initialize_storage(self):
        if not self.storage_path.exists():
            self.storage_path.write_text('{"completed_games": []}')
    
    def save_game(self, game_id: str, game: Game):
        history = self._read_history()
        game_data = {
            "game_id": game_id,
            "timestamp": game.timestamp.isoformat(),
            "opponent_strategy": game.opponent_strategy.__class__.__name__,
            "rounds": [vars(round) for round in game.rounds],
            "final_scores": {
                "ai": game.ai_total_score,
                "opponent": game.opponent_total_score
            }
        }
        history["completed_games"].append(game_data)
        self._write_history(history)

    def get_game(self, game_id: str):
        """
        Retrieve a game from history by its ID
        
        Args:
            game_id: The ID of the game to retrieve
            
        Returns:
            dict: The game data if found, None if not found
        """
        history = self._read_history()
        for game in history["completed_games"]:
            if game["game_id"] == game_id:
                return game
        return None
    
    def _read_history(self):
        return json.loads(self.storage_path.read_text())
    
    def _write_history(self, history):
        self.storage_path.write_text(json.dumps(history, indent=2))