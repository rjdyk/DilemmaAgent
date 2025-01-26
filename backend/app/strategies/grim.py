# grim.py
from app.models.types import Move
from app.strategies.base import BaseStrategy

class GrimTrigger(BaseStrategy):
    def __init__(self):
        super().__init__("Grim Trigger")
        self.triggered = False

    def get_move(self, current_round: int) -> Move:
        if not self.history:
            return Move.COOPERATE
            
        # Get opponent's last move based on which player we are
        opponent_last_move = (
            self.history[-1].player2_move if self.is_player1 
            else self.history[-1].player1_move
        )
            
        if not self.triggered and opponent_last_move == Move.DEFECT:
            self.triggered = True
            
        return Move.DEFECT if self.triggered else Move.COOPERATE

    def reset(self):
        super().reset()
        self.triggered = False