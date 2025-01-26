# tit_for_tat.py
from app.models.types import Move
from app.strategies.base import BaseStrategy

class TitForTat(BaseStrategy):
    def __init__(self):
        super().__init__("Tit for Tat")

    def get_move(self, current_round: int) -> Move:
        if not self.history:
            return Move.COOPERATE
            
        # If we're player 1, look at player2's last move
        # If we're player 2, look at player1's last move
        last_opponent_move = (
            self.history[-1].player2_move if self.is_player1 
            else self.history[-1].player1_move
        )
        return last_opponent_move