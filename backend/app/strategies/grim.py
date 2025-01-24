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
            
        if not self.triggered and self.history[-1].player2_move == Move.DEFECT:
            self.triggered = True
            
        return Move.DEFECT if self.triggered else Move.COOPERATE

    def reset(self):
        super().reset()
        self.triggered = False