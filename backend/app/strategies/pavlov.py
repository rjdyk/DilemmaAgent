# pavlov.py
from app.models.types import Move
from app.strategies.base import BaseStrategy

class Pavlov(BaseStrategy):
    def __init__(self, is_player1: bool):
        super().__init__("Pavlov", is_player1)

    def get_move(self, current_round: int) -> Move:
        if not self.history:
            return Move.COOPERATE
            
        last_round = self.history[-1]
        my_move = last_round.player1_move if self.is_player1 else last_round.player2_move
        my_score = last_round.player1_score if self.is_player1 else last_round.player2_score
            
        # Win = score >= 3 (Cooperate/Cooperate or Defect/Cooperate)
        won = (my_score >= 3)
        return my_move if won else Move.COOPERATE if my_move == Move.DEFECT else Move.DEFECT