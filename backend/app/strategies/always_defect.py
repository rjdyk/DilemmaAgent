from app.models.types import Move
from .base import BaseStrategy

class AlwaysDefect(BaseStrategy):
    """
    A strategy that always defects regardless of the opponent's moves.
    """
    
    def __init__(self, is_player1: bool):
        super().__init__(name="Always Defect", is_player1=is_player1)

    def get_move(self, current_round: int) -> Move:
        """
        Always returns DEFECT regardless of game state
        
        Args:
            current_round: The current round number (0-based)
            
        Returns:
            Move.DEFECT: This strategy always DEFECT
        """
        return Move.DEFECT