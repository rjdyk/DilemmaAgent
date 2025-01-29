# utils/history.py
import json
from datetime import datetime
from pathlib import Path
from app.models.game import Game
from app.strategies.ai_strategy import AIStrategy

class GameHistory:
    def __init__(self, storage_path: str = "game_history.json"):
        self.storage_path = Path(storage_path)
        self._initialize_storage()
    
    def _initialize_storage(self):
        if not self.storage_path.exists():
            self.storage_path.write_text('{"completed_games": []}')
    
    def save_game(self, game_id: str, game: Game):
        history = self._read_history()
        
        # Start with the original game data structure
        game_data = {
            "game_id": game_id,
            "timestamp": game.timestamp.isoformat(),
            "player1_strategy": game.player1_strategy.__class__.__name__,
            "player2_strategy": game.player2_strategy.__class__.__name__,
            "rounds": [vars(round) for round in game.rounds],
            "final_scores": {
                "player1": game.player1_total_score,
                "player2": game.player2_total_score
            },
            "payoff_matrix": {
                "cooperate_cooperate": game.payoff_matrix.cooperate_cooperate,
                "cooperate_defect": game.payoff_matrix.cooperate_defect,
                "defect_cooperate": game.payoff_matrix.defect_cooperate,
                "defect_defect": game.payoff_matrix.defect_defect
            }
        }

        # Add AI-specific data only if AI strategies are involved
        if isinstance(game.player1_strategy, AIStrategy):
            game_data["player1_ai_data"] = {
                "total_tokens": game.player1_strategy.total_tokens_used,
                "conversation_history": game.player1_strategy.conversation_history
            }
            
        if isinstance(game.player2_strategy, AIStrategy):
            game_data["player2_ai_data"] = {
                "total_tokens": game.player2_strategy.total_tokens_used,
                "conversation_history": game.player2_strategy.conversation_history
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