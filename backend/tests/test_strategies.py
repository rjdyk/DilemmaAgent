import pytest
from app.models.types import Move, RoundResult
from app.strategies.tit_for_tat import TitForTat
from app.strategies.pavlov import Pavlov
from app.strategies.random_strategy import RandomStrategy
from app.strategies.grim import GrimTrigger

def create_round_result(round_num: int, p1_move: Move, p2_move: Move) -> RoundResult:
    """Helper to create round results with proper scoring"""
    scores = {
        (Move.COOPERATE, Move.COOPERATE): (3, 3),
        (Move.COOPERATE, Move.DEFECT): (0, 5),
        (Move.DEFECT, Move.COOPERATE): (5, 0),
        (Move.DEFECT, Move.DEFECT): (1, 1)
    }
    p1_score, p2_score = scores[(p1_move, p2_move)]
    return RoundResult(
        round_number=round_num,
        player1_move=p1_move,
        player2_move=p2_move,
        player1_score=p1_score,
        player2_score=p2_score,
        player1_reasoning="test",
        player2_reasoning="test",
        cumulative_player1_score=0,
        cumulative_player2_score=5,
    )

class TestTitForTat:
    def test_initial_move_as_player2(self):
        """Player 2 TitForTat should cooperate on first move"""
        strategy = TitForTat(is_player1=False)
        assert strategy.get_move(0) == Move.COOPERATE

    def test_copies_cooperate_as_player2(self):
        """Player 2 TitForTat should cooperate after player 1 cooperates"""
        strategy = TitForTat(is_player1=False)
        # Add round where player 1 cooperated
        strategy.add_round(create_round_result(1, Move.COOPERATE, Move.COOPERATE))
        assert strategy.get_move(1) == Move.COOPERATE

    def test_copies_defect_as_player2(self):
        """Player 2 TitForTat should defect after player 1 defects"""
        strategy = TitForTat(is_player1=False)
        # Add round where player 1 defected
        strategy.add_round(create_round_result(1, Move.DEFECT, Move.COOPERATE))
        assert strategy.get_move(1) == Move.DEFECT

    def test_multiple_rounds_as_player2(self):
        """Player 2 TitForTat should copy player 1's previous move each round"""
        strategy = TitForTat(is_player1=False)
        
        # Round 1: Player 1 cooperates
        strategy.add_round(create_round_result(1, Move.COOPERATE, Move.COOPERATE))
        assert strategy.get_move(1) == Move.COOPERATE
        
        # Round 2: Player 1 defects
        strategy.add_round(create_round_result(2, Move.DEFECT, Move.COOPERATE))
        assert strategy.get_move(2) == Move.DEFECT
        
        # Round 3: Player 1 cooperates again
        strategy.add_round(create_round_result(3, Move.COOPERATE, Move.DEFECT))
        assert strategy.get_move(3) == Move.COOPERATE

    def test_ignores_own_moves_as_player2(self):
        """Player 2 TitForTat should only look at player 1's moves, not its own"""
        strategy = TitForTat(is_player1=False)
        # Player 1 cooperates, Player 2 defects
        strategy.add_round(create_round_result(1, Move.COOPERATE, Move.DEFECT))
        # Should still copy Player 1's cooperate, not its own defect
        assert strategy.get_move(1) == Move.COOPERATE
        
    def test_handles_empty_history_as_player2(self):
        """Player 2 TitForTat should handle empty history gracefully"""
        strategy = TitForTat(is_player1=False)
        strategy.reset()  # Explicitly empty history
        assert strategy.get_move(0) == Move.COOPERATE

    def test_reset_as_player2(self):
        """Player 2 TitForTat should reset properly between games"""
        strategy = TitForTat(is_player1=False)
        # Add some history
        strategy.add_round(create_round_result(1, Move.DEFECT, Move.COOPERATE))
        assert strategy.get_move(1) == Move.DEFECT
        
        # Reset and verify back to initial state
        strategy.reset()
        assert strategy.get_move(0) == Move.COOPERATE

class TestPavlov:
    def test_initial_move(self):
        strategy = Pavlov(is_player1=True)
        assert strategy.get_move(0) == Move.COOPERATE

    @pytest.mark.parametrize("is_player1,opponent_move,expected", [
        # Win scenarios (stay with previous move COOPERATE)
        (True, Move.COOPERATE, Move.COOPERATE),   # I cooperated (3,3)
        (False, Move.COOPERATE, Move.COOPERATE),  # I cooperated (3,3)

        # Loss scenarios (switch from COOPERATE to DEFECT)
        (True, Move.DEFECT, Move.DEFECT),    # I cooperated and got exploited (0,5)
        (False, Move.DEFECT, Move.DEFECT),   # I cooperated and got exploited (0,5)
        ])
    def test_win_stay_lose_shift(self, is_player1: bool, opponent_move: Move, expected: Move):
        strategy = Pavlov(is_player1=is_player1)
        # Create a round where I cooperated and opponent did their move
        if is_player1:
            round_result = create_round_result(1, Move.COOPERATE, opponent_move)
        else:
            round_result = create_round_result(1, opponent_move, Move.COOPERATE)
        strategy.add_round(round_result)
        assert strategy.get_move(1) == expected

class TestRandomStrategy:
    def test_consistent_with_same_seed(self):
        strategy1 = RandomStrategy(is_player1=True, seed=42)
        strategy2 = RandomStrategy(is_player1=False, seed=42)
        assert strategy1.get_move(0) == strategy2.get_move(0)

    def test_different_with_different_seeds(self):
        strategy1 = RandomStrategy(is_player1=True, seed=42)
        strategy2 = RandomStrategy(is_player1=False, seed=43)
        # Run multiple times to avoid rare false negatives
        moves1 = [strategy1.get_move(i) for i in range(10)]
        moves2 = [strategy2.get_move(i) for i in range(10)]
        assert moves1 != moves2

    def test_returns_valid_moves(self):
        strategy = RandomStrategy(is_player1=True)
        for _ in range(10):
            move = strategy.get_move(0)
            assert move in [Move.COOPERATE, Move.DEFECT]

class TestGrimTrigger:
    def test_initial_move(self):
        strategy = GrimTrigger(is_player1=True)
        assert strategy.get_move(0) == Move.COOPERATE

    def test_defects_forever_after_opponent_defects_as_player1(self):
        strategy = GrimTrigger(is_player1=True)
        strategy.add_round(create_round_result(1, Move.COOPERATE, Move.DEFECT))
        assert strategy.get_move(1) == Move.DEFECT
        strategy.add_round(create_round_result(2, Move.DEFECT, Move.COOPERATE))
        assert strategy.get_move(2) == Move.DEFECT

    def test_defects_forever_after_opponent_defects_as_player2(self):
        strategy = GrimTrigger(is_player1=False)
        strategy.add_round(create_round_result(1, Move.DEFECT, Move.COOPERATE))
        assert strategy.get_move(1) == Move.DEFECT
        strategy.add_round(create_round_result(2, Move.COOPERATE, Move.DEFECT))
        assert strategy.get_move(2) == Move.DEFECT