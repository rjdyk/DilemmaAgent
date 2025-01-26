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
        
        # Get our move and score based on which player we are
        if self.is_player1:
            my_move = last_round.player1_move
            my_score = last_round.player1_score
        else:
            my_move = last_round.player2_move
            my_score = last_round.player2_score
            
        # Win = Cooperate/Cooperate (3,3) or Defect/Cooperate (5,0)
        # Stay with previous move if won, switch if lost
        won = (my_score >= 3)
        return my_move if won else Move.COOPERATE if my_move == Move.DEFECT else Move.DEFECT