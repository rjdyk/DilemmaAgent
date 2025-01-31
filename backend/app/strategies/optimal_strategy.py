from typing import Optional
import random
from app.strategies.base import BaseStrategy
from app.models.types import Move, MatrixType, MATRIX_PAYOFFS

class OptimalStrategy(BaseStrategy):
    """Strategy that plays according to the theoretically optimal strategy for each matrix type"""
    
    def __init__(self, matrix_type: MatrixType, is_player1: bool):
        name = f"Optimal ({matrix_type.value})"
        super().__init__(name=name, is_player1=is_player1)
        self.matrix_type = matrix_type
        self.optimal_coop_rate = MATRIX_PAYOFFS[matrix_type].optimal_strategy.cooperation_rate

    def get_move(self, current_round: int) -> Move:
        """
        Get the next move based on optimal cooperation rate
        
        For mixed strategies, uses randomization to achieve the target cooperation rate.
        For pure strategies (cooperation_rate 0 or 1), always plays that move.
        """
        # Pure strategy cases
        if self.optimal_coop_rate == 0:
            return Move.DEFECT
        if self.optimal_coop_rate == 1:
            return Move.COOPERATE
            
        # Mixed strategy case - use randomization
        return Move.COOPERATE if random.random() < self.optimal_coop_rate else Move.DEFECT

    def reset(self):
        """Reset strategy state"""
        super().reset()
        # No additional state to reset for this strategy