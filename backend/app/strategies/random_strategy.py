# random_strategy.py
from app.models.types import Move
from app.strategies.base import BaseStrategy
import random

class RandomStrategy(BaseStrategy):
    def __init__(self, seed: int = 42):
        super().__init__("Random")
        self.rng = random.Random(seed)

    def get_move(self, current_round: int) -> Move:
        return self.rng.choice([Move.COOPERATE, Move.DEFECT])