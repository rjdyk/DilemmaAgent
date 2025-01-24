# pavlov.py
from app.models.types import Move
from app.strategies.base import BaseStrategy

class Pavlov(BaseStrategy):
    def __init__(self):
        super().__init__("Pavlov")

    def get_move(self, current_round: int) -> Move:
        if not self.history:
            return Move.COOPERATE
            
        last_round = self.history[-1]
        # Win = Cooperate/Cooperate (3,3) or Defect/Cooperate (5,0)
        # Stay with previous move if won, switch if lost
        previous_move = last_round.player1_move
        won = (last_round.player1_score >= 3)
        return previous_move if won else Move.COOPERATE if previous_move == Move.DEFECT else Move.DEFECT