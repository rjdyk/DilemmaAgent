# utils/storage.py
from typing import Dict, Optional, Tuple
from uuid import uuid4
from app.models.game import Game
from app.strategies.base import BaseStrategy

class GameStorage:
    def __init__(self):
        self.active_games: Dict[str, Game] = {}
    
    def create_game(self, player1_strategy: BaseStrategy, player2_strategy: BaseStrategy) -> Tuple[str, Game]:
        """
        Create a new game with two players
        
        Args:
            player1_strategy: Strategy for player 1
            player2_strategy: Strategy for player 2
            
        Returns:
            Tuple of (game_id, game)
        """
        game_id = str(uuid4())
        game = Game(player1_strategy, player2_strategy)  # Game class will need updating too
        self.active_games[game_id] = game
        return game_id, game
    
    def get_game(self, game_id: str) -> Optional[Game]:
        return self.active_games.get(game_id)
        
    def remove_game(self, game_id: str):
        if game_id in self.active_games:
            del self.active_games[game_id]