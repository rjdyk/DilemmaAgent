from typing import List, Dict, Optional, Tuple
from datetime import datetime
from app.models.types import Move, RoundResult
from app.strategies.base import BaseStrategy

class Game:
    def __init__(self, player1_strategy: BaseStrategy, player2_strategy: BaseStrategy, max_rounds: int = 10,):
        """Initialize a new game with two strategies"""
        self.player1_strategy = player1_strategy
        self.player2_strategy = player2_strategy
        self.current_round = 0
        self.max_rounds = max_rounds        
        self.game_over = False
        self.rounds: List[RoundResult] = []
        self.player1_total_score = 0
        self.player2_total_score = 0
        self.timestamp = datetime.now()
        
        # Standard prisoner's dilemma payoff matrix
        # (player1_payoff, player2_payoff)
        self.payoff_matrix = {
            (Move.COOPERATE, Move.COOPERATE): (3, 3),
            (Move.COOPERATE, Move.DEFECT): (0, 5),
            (Move.DEFECT, Move.COOPERATE): (5, 0),
            (Move.DEFECT, Move.DEFECT): (1, 1)
        }

    def is_valid_move(self, move: str) -> bool:
        """Validate if a move is legal"""
        try:
            Move(move.lower())
            return True
        except ValueError:
            return False

    def get_player1_move(self) -> Move:
        """Get player 1's move based on their strategy"""
        return self.player1_strategy.get_move(self.current_round)

    def get_player2_move(self) -> Move:
        """Get player 2's move based on their strategy"""
        return self.player2_strategy.get_move(self.current_round)

    def process_round(self) -> Optional[RoundResult]:
        """
        Process a single round of the game.
        
        Returns:
            Optional[RoundResult]: The result of the round
        
        Raises:
            ValueError: If the game is already over
        """
        if self.is_game_over():
            raise ValueError("Cannot process round: game is already over")

        # Get moves from both players
        player1_move = self.get_player1_move()
        player2_move = self.get_player2_move()
        
        # Calculate scores for this round
        player1_score, player2_score = self.calculate_scores(player1_move, player2_move)
        
        # Update total scores
        self.player1_total_score += player1_score
        self.player2_total_score += player2_score
        
        # Create round result
        round_result = RoundResult(
            round_number=self.current_round + 1,
            player1_move=player1_move,
            player2_move=player2_move,
            player1_reasoning=self.player1_strategy.name,
            player2_reasoning=self.player2_strategy.name,
            player1_score=player1_score,
            player2_score=player2_score
        )
        
        # Add to game history
        self.rounds.append(round_result)
        
        # Increment round counter
        self.current_round += 1
        
        # Check if this was the final round
        if self.current_round >= self.max_rounds:
            self.game_over = True
            
        return round_result
    
    def run_all_rounds(self) -> List[RoundResult]:
        """
        Process all remaining rounds until game completion
        
        Returns:
            List[RoundResult]: Results of all processed rounds
            
        Raises:
            ValueError: If game is already over
        """
        if self.is_game_over():
            raise ValueError("Game is already complete")
            
        results = []
        while not self.is_game_over():
            result = self.process_round()
            if result:
                results.append(result)
                
        return results

    def calculate_scores(self, player1_move: Move, player2_move: Move) -> tuple[int, int]:
        """Calculate scores for both players based on their moves"""
        try:
            return self.payoff_matrix[(player1_move, player2_move)]
        except KeyError as e:
            raise KeyError(f"Invalid move combination: {player1_move}, {player2_move}") from e

    def is_game_over(self) -> bool:
        """Check if the game has ended"""
        return self.current_round >= self.max_rounds or self.game_over