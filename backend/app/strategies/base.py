from typing import List, Optional
from app.models.types import Move, RoundResult
from enum import Enum, auto


class StrategyType(Enum):
    ALWAYS_COOPERATE = "always_cooperate"
    ALWAYS_DEFECT = "always_defect"
    TIT_FOR_TAT = "tit_for_tat"
    PAVLOV = "pavlov"
    RANDOM = "random"
    GRIM = "grim"

class BaseStrategy:
    """Base class for all opponent strategies"""
    
    def __init__(self, name: str, is_player1: bool):
        self.name = name
        self._history: List[RoundResult] = []
        self.is_player1 = is_player1
        
    def get_move(self, current_round: int) -> Move:
        """
        Get the next move based on game state
        
        Args:
            current_round: The current round number (0-based)
            
        Returns:
            Move: The strategy's chosen move (COOPERATE or DEFECT)
        """
        raise NotImplementedError("Strategies must implement get_move()")
    
    def get_opponent_last_move(self) -> Optional[Move]:
        """Get the opponent's move from the last round"""

        if not self.history:
            return None
        return (
            self.history[-1].player2_move if self.is_player1
            else self.history[-1].player1_move
        )
        
    @property 
    def history(self) -> List[RoundResult]:
        """Get the game history"""
        return self._history
        
    def add_round(self, round_result: RoundResult):
        """
        Record the result of a completed round
        
        Args:
            round_result: Complete information about the round that just finished
        """
        self._history.append(round_result)

    def reset(self):
        """Reset the strategy's history for a new game"""
        self._history = []
