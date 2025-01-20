from backend.app.models.game import Move
from .base import BaseStrategy

class AlwaysCooperate(BaseStrategy):
    """
    A strategy that always cooperates regardless of the opponent's moves.
    
    This is one of the simplest possible strategies. It's not particularly effective
    in terms of maximizing score since it can be exploited by defecting opponents,
    but it's useful as a baseline strategy and for testing.
    """
    
    def __init__(self):
        """Initialize the Always Cooperate strategy"""
        super().__init__(name="Always Cooperate")

    def get_move(self, current_round: int) -> Move:
        """
        Always returns COOPERATE regardless of game state
        
        Args:
            current_round: The current round number (0-based)
            
        Returns:
            Move.COOPERATE: This strategy always cooperates
        """
        return Move.COOPERATE