# tit_for_tat.py
from app.models.types import Move
from app.strategies.base import BaseStrategy

class TitForTat(BaseStrategy):
    def __init__(self, is_player1: bool):
        super().__init__("Tit for Tat", is_player1)

    def get_move(self, current_round: int) -> Move:
        opponent_last_move = self.get_opponent_last_move()
        return opponent_last_move if opponent_last_move else Move.COOPERATE