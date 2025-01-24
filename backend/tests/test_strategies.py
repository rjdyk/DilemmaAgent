import pytest
from app.models.types import Move, RoundResult
from app.strategies.tit_for_tat import TitForTat
from app.strategies.pavlov import Pavlov
from app.strategies.random_strategy import RandomStrategy
from app.strategies.grim import GrimTrigger

def create_round_result(player1_move: Move, player2_move: Move) -> RoundResult:
    return RoundResult(
        round_number=1,
        player1_move=player1_move,
        player2_move=player2_move,
        player1_reasoning="test",
        player2_reasoning="test",
        player1_score=3 if player1_move == Move.COOPERATE and player2_move == Move.COOPERATE else 5 if player1_move == Move.DEFECT and player2_move == Move.COOPERATE else 0 if player1_move == Move.COOPERATE and player2_move == Move.DEFECT else 1,
        player2_score=3 if player1_move == Move.COOPERATE and player2_move == Move.COOPERATE else 0 if player1_move == Move.DEFECT and player2_move == Move.COOPERATE else 5 if player1_move == Move.COOPERATE and player2_move == Move.DEFECT else 1
    )

class TestTitForTat:
    def test_first_move_cooperates(self):
        strategy = TitForTat()
        assert strategy.get_move(0) == Move.COOPERATE

    def test_copies_opponent_last_move(self):
        strategy = TitForTat()
        strategy.add_round(create_round_result(Move.COOPERATE, Move.DEFECT))
        assert strategy.get_move(1) == Move.DEFECT
        
    def test_reset_clears_history(self):
        strategy = TitForTat()
        strategy.add_round(create_round_result(Move.COOPERATE, Move.DEFECT))
        strategy.reset()
        assert strategy.get_move(0) == Move.COOPERATE

class TestPavlov:
    def test_first_move_cooperates(self):
        strategy = Pavlov()
        assert strategy.get_move(0) == Move.COOPERATE

    def test_stays_after_mutual_cooperation(self):
        strategy = Pavlov()
        strategy.add_round(create_round_result(Move.COOPERATE, Move.COOPERATE))
        assert strategy.get_move(1) == Move.COOPERATE

    def test_switches_after_being_betrayed(self):
        strategy = Pavlov()
        strategy.add_round(create_round_result(Move.COOPERATE, Move.DEFECT))
        assert strategy.get_move(1) == Move.DEFECT

    def test_switches_after_defecting_against_cooperation(self):
        strategy = Pavlov()
        strategy.add_round(create_round_result(Move.DEFECT, Move.COOPERATE))
        assert strategy.get_move(1) == Move.DEFECT

class TestRandomStrategy:
    def test_consistent_with_same_seed(self):
        strategy1 = RandomStrategy(seed=42)
        strategy2 = RandomStrategy(seed=42)
        assert strategy1.get_move(0) == strategy2.get_move(0)

    def test_different_with_different_seeds(self):
        strategy1 = RandomStrategy(seed=42)
        strategy2 = RandomStrategy(seed=43)
        # Run multiple times to avoid rare false negatives
        moves1 = [strategy1.get_move(i) for i in range(10)]
        moves2 = [strategy2.get_move(i) for i in range(10)]
        assert moves1 != moves2

    def test_returns_valid_moves(self):
        strategy = RandomStrategy()
        for _ in range(10):
            move = strategy.get_move(0)
            assert move in [Move.COOPERATE, Move.DEFECT]

class TestGrimTrigger:
    def test_first_move_cooperates(self):
        strategy = GrimTrigger()
        assert strategy.get_move(0) == Move.COOPERATE

    def test_continues_cooperation_until_betrayed(self):
        strategy = GrimTrigger()
        strategy.add_round(create_round_result(Move.COOPERATE, Move.COOPERATE))
        assert strategy.get_move(1) == Move.COOPERATE

    def test_defects_forever_after_betrayal(self):
        strategy = GrimTrigger()
        strategy.add_round(create_round_result(Move.COOPERATE, Move.DEFECT))
        assert strategy.get_move(1) == Move.DEFECT
        strategy.add_round(create_round_result(Move.DEFECT, Move.COOPERATE))
        assert strategy.get_move(2) == Move.DEFECT

    def test_reset_clears_triggered_state(self):
        strategy = GrimTrigger()
        strategy.add_round(create_round_result(Move.COOPERATE, Move.DEFECT))
        strategy.reset()
        assert strategy.get_move(0) == Move.COOPERATE