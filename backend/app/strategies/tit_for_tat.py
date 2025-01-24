# tit_for_tat.py
from app.models.types import Move
from app.strategies.base import BaseStrategy

class TitForTat(BaseStrategy):
    def __init__(self):
        super().__init__("Tit for Tat")

    def get_move(self, current_round: int) -> Move:
        if not self.history:
            return Move.COOPERATE
        return self.history[-1].player2_move