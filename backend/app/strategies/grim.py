# grim.py
from app.models.types import Move
from app.strategies.base import BaseStrategy

class GrimTrigger(BaseStrategy):
    def __init__(self, is_player1: bool):
        super().__init__("Grim Trigger", is_player1)
        self.triggered = False

    def get_move(self, current_round: int) -> Move:
        if not self.history:
            return Move.COOPERATE
            
        opponent_last_move = self.get_opponent_last_move()
        if not self.triggered and opponent_last_move == Move.DEFECT:
            self.triggered = True
            
        return Move.DEFECT if self.triggered else Move.COOPERATE

    def reset(self):
        super().reset()
        self.triggered = False