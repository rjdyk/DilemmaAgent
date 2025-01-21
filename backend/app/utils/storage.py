# utils/storage.py
from typing import Dict, Optional
from uuid import uuid4
from app.models.game import Game

class GameStorage:
    def __init__(self):
        self.active_games: Dict[str, Game] = {}
    
    def create_game(self, strategy) -> tuple[str, Game]:
        game_id = str(uuid4())
        game = Game(strategy)
        self.active_games[game_id] = game
        return game_id, game
    
    def get_game(self, game_id: str) -> Optional[Game]:
        return self.active_games.get(game_id)
        
    def remove_game(self, game_id: str):
        if game_id in self.active_games:
            del self.active_games[game_id]