from enum import Enum
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
from backend.app.strategies.base import BaseStrategy, AlwaysCooperate

class Move(Enum):
    COOPERATE = "cooperate"
    DEFECT = "defect"

@dataclass
class RoundResult:
    round_number: int
    ai_move: Move
    opponent_move: Move
    ai_reasoning: str
    ai_score: int
    opponent_score: int

class Game:
    def __init__(self, opponent_strategy: BaseStrategy):
        # Initialize game state
        self.opponent_strategy = opponent_strategy
        self.current_round = 0
        self.max_rounds = 10
        self.game_over = False
        self.rounds: List[RoundResult] = []
        self.ai_total_score = 0
        self.opponent_total_score = 0
        self.timestamp = datetime.now()
        
        # Standard prisoner's dilemma payoff matrix
        # (ai_payoff, opponent_payoff)
        self.payoff_matrix = {
            (Move.COOPERATE, Move.COOPERATE): (3, 3),
            (Move.COOPERATE, Move.DEFECT): (0, 5),
            (Move.DEFECT, Move.COOPERATE): (5, 0),
            (Move.DEFECT, Move.DEFECT): (1, 1)
        }

    def is_valid_move(self, move: str) -> bool:
        """Validate if the provided move is legal"""
        try:
            Move(move.lower())
            return True
        except ValueError:
            return False

    def process_round(self, ai_move: str, ai_reasoning: str) -> Optional[RoundResult]:
        """
        Process a single round of the game.
        
        Args:
            ai_move (str): The AI's move ('cooperate' or 'defect')
            ai_reasoning (str): The AI's explanation for its move
            
        Returns:
            Optional[RoundResult]: The result of the round, or None if the move was invalid
        
        Raises:
            ValueError: If the game is already over
        """
        # Check if game is already over
        if self.is_game_over():
            raise ValueError("Cannot process round: game is already over")

        # Validate AI move
        if not self.is_valid_move(ai_move):
            return None
            
        # Convert string move to Move enum
        ai_move_enum = Move(ai_move.lower())
        
        # Get opponent's move based on their strategy
        opponent_move = self.get_opponent_move()
        
        # Calculate scores for this round
        ai_score, opponent_score = self.calculate_scores(ai_move_enum, opponent_move)
        
        # Update total scores
        self.ai_total_score += ai_score
        self.opponent_total_score += opponent_score
        
        # Create round result
        round_result = RoundResult(
            round_number=self.current_round + 1,
            ai_move=ai_move_enum,
            opponent_move=opponent_move,
            ai_reasoning=ai_reasoning,
            ai_score=ai_score,
            opponent_score=opponent_score
        )
        
        # Add to game history
        self.rounds.append(round_result)
        
        # Increment round counter
        self.current_round += 1
        
        # Check if this was the final round
        if self.current_round >= self.max_rounds:
            self.game_over = True
            
        return round_result

    def calculate_scores(self, ai_move: Move, opponent_move: Move) -> tuple[int, int]:
        """
        Calculate scores for both players based on their moves using the payoff matrix.
        
        Args:
            ai_move (Move): The AI's move (COOPERATE or DEFECT)
            opponent_move (Move): The opponent's move (COOPERATE or DEFECT)
            
        Returns:
            tuple[int, int]: A tuple of (ai_score, opponent_score)
            
        Raises:
            KeyError: If the move combination is not found in the payoff matrix
        """
        try:
            # Look up the score combination in the payoff matrix
            ai_score, opponent_score = self.payoff_matrix[(ai_move, opponent_move)]
            return ai_score, opponent_score
            
        except KeyError as e:
            # This should never happen if moves are properly validated,
            # but we'll handle it just in case
            raise KeyError(f"Invalid move combination: {ai_move}, {opponent_move}") from e

    def get_opponent_move(self) -> Move:
        """Get the opponent's move based on their strategy"""
        return self.opponent_strategy.get_move(self.current_round)

    def get_game_state(self) -> Dict:
        """Return the current game state"""
        return {
            "game_id": id(self),
            "opponent_strategy": self.opponent_strategy.name,
            "current_round": self.current_round,
            "game_over": self.game_over,
            "ai_total_score": self.ai_total_score,
            "opponent_total_score": self.opponent_total_score,
            "rounds": self.rounds,
            "timestamp": self.timestamp
        }

    def get_game_history(self) -> List[RoundResult]:
        """Return the complete game history"""
        return self.rounds

    def is_game_over(self) -> bool:
        """Check if the game has ended"""
        return self.current_round >= self.max_rounds or self.game_over