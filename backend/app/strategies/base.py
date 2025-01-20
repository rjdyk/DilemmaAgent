from typing import List, Optional
from backend.app.models.game import Move, RoundResult
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
    
    def __init__(self, name: str):
        self.name = name
        self._history: List[RoundResult] = []
        
    def get_move(self, current_round: int) -> Move:
        """
        Get the next move based on game state
        
        Args:
            current_round: The current round number (0-based)
            
        Returns:
            Move: The strategy's chosen move (COOPERATE or DEFECT)
        """
        raise NotImplementedError("Strategies must implement get_move()")
        
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
