from typing import List, Dict, Optional, Tuple
from datetime import datetime
from app.models.types import Move, RoundResult, PayoffMatrix, TokenUsage, OptimalStrategy
from app.strategies.base import BaseStrategy
from app.strategies.ai_strategy import AIStrategy

class Game:
    def __init__(self, player1_strategy: BaseStrategy, player2_strategy: BaseStrategy, max_rounds: int = 10, payoff_matrix: Optional[PayoffMatrix] = None):
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

        self.has_ai_player = isinstance(player1_strategy, AIStrategy) or isinstance(player2_strategy, AIStrategy)
        self.ai_errors: Dict[str, str] = {}  # Track AI errors by player
        
        # Use provided matrix or default
        default_matrix = PayoffMatrix(
            cooperate_cooperate=(3, 3),
            cooperate_defect=(0, 5),
            defect_cooperate=(5, 0),
            defect_defect=(1, 1),
            optimal_strategy=OptimalStrategy(
                cooperation_rate=0.0,
                expected_score_per_round=(1, 1),
                description="Pure defection is dominant strategy"
            )
        )

        self.payoff_matrix = payoff_matrix or default_matrix
        
        self.player1_model = (
            player1_strategy.model_name if isinstance(player1_strategy, AIStrategy) else None
        )
        self.player2_model = (
            player2_strategy.model_name if isinstance(player2_strategy, AIStrategy) else None
        )
        self.has_ai_player = isinstance(player1_strategy, AIStrategy) or isinstance(player2_strategy, AIStrategy)
        self.ai_errors = {
            "player1": None,
            "player2": None
        }

        self.payoff_dict = {
            (Move.COOPERATE, Move.COOPERATE): self.payoff_matrix.cooperate_cooperate,
            (Move.COOPERATE, Move.DEFECT): self.payoff_matrix.cooperate_defect,
            (Move.DEFECT, Move.COOPERATE): self.payoff_matrix.defect_cooperate,
            (Move.DEFECT, Move.DEFECT): self.payoff_matrix.defect_defect
        }

    def is_valid_move(self, move: str) -> bool:
        """Validate if a move is legal"""
        try:
            Move(move.lower())
            return True
        except ValueError:
            return False

    async def get_player1_move(self) -> Move:
        """Get player 1's move based on their strategy"""
        if isinstance(self.player1_strategy, AIStrategy):
            move = await self.player1_strategy.get_move(self.current_round)
            if self.player1_strategy.last_error:
                self.ai_errors["player1"] = self.player1_strategy.last_error
        else:
            move = self.player1_strategy.get_move(self.current_round)
        print(f"Player 1 ({self.player1_strategy.name}) move: {move}")
        return move

    async def get_player2_move(self) -> Move:
        """Get player 2's move based on their strategy"""
        if isinstance(self.player2_strategy, AIStrategy):
            move = await self.player2_strategy.get_move(self.current_round)
            if self.player2_strategy.last_error:
                self.ai_errors["player2"] = self.player2_strategy.last_error
        else:
            move = self.player2_strategy.get_move(self.current_round)
        print(f"Player 2 ({self.player2_strategy.name}) move: {move}")
        return move

    async def process_round(self) -> Optional[RoundResult]:
        """
        Process a single round of the game.
        
        Returns:
            Optional[RoundResult]: The result of the round
        
        Raises:
            ValueError: If the game is already over
        """
        if self.is_game_over():
            raise ValueError("Cannot process round: game is already over")

        # Get moves from both players - error handling already done in strategies
        player1_move = await self.get_player1_move()
        player2_move = await self.get_player2_move()

        # Get reasoning - for AI strategies this will include their explanation
        player1_reasoning = (
            self.player1_strategy.conversation_history[-1]["reasoning"]  # AI stores its reasoning here
            if isinstance(self.player1_strategy, AIStrategy)
            else self.player1_strategy.name
        )
        player2_reasoning = (
            self.player2_strategy.conversation_history[-1]["reasoning"]  # AI stores its reasoning here
            if isinstance(self.player2_strategy, AIStrategy) 
            else self.player2_strategy.name
        )       

        # Calculate scores
        player1_score, player2_score = self.calculate_scores(player1_move, player2_move)
        
        # Update total scores
        self.player1_total_score += player1_score
        self.player2_total_score += player2_score

        cumulative_player1_score = self.player1_total_score
        cumulative_player2_score = self.player2_total_score

        # Get token usage if applicable
        token_usage = None
        if isinstance(self.player1_strategy, AIStrategy) or isinstance(self.player2_strategy, AIStrategy):
            total_prompt_tokens = 0
            total_completion_tokens = 0
            
            if isinstance(self.player1_strategy, AIStrategy):
                total_prompt_tokens += self.player1_strategy.total_tokens_used
            if isinstance(self.player2_strategy, AIStrategy):
                total_prompt_tokens += self.player2_strategy.total_tokens_used
                
            token_usage = TokenUsage(
                prompt_tokens=total_prompt_tokens,
                completion_tokens=0,  # Will be updated when we implement completion token tracking
                total_tokens=total_prompt_tokens
            )

        # Create round result
        round_result = RoundResult(
            round_number=self.current_round + 1,
            player1_move=player1_move,
            player2_move=player2_move,
            player1_reasoning=player1_reasoning,
            player2_reasoning=player2_reasoning,
            player1_score=player1_score,
            player2_score=player2_score,
            cumulative_player1_score=cumulative_player1_score,  # Pass cumulative score
            cumulative_player2_score=cumulative_player2_score,  # Pass cumulative score
            token_usage=token_usage,
            api_errors=None  # The strategies handle their own errors
        )

        # Update histories
        self.rounds.append(round_result)
        self.player1_strategy.add_round(round_result)
        self.player2_strategy.add_round(round_result)

        # Increment round counter
        self.current_round += 1
        
        # Check for game over
        if self.current_round >= self.max_rounds:
            self.game_over = True

        return round_result
    
    async def run_all_rounds(self) -> List[RoundResult]:
        """Process all remaining rounds until game completion"""
        if self.is_game_over():
            raise ValueError("Game is already complete")
            
        results = []
        while not self.is_game_over():
            result = await self.process_round()
            if result:
                results.append(result)
                
        return results

    def calculate_scores(self, player1_move: Move, player2_move: Move) -> tuple[int, int]:
        """Calculate scores for both players based on their moves"""
        try:
            return self.payoff_dict[(player1_move, player2_move)]
        except KeyError as e:
            raise KeyError(f"Invalid move combination: {player1_move}, {player2_move}") from e

    def is_game_over(self) -> bool:
        """Check if the game has ended"""
        return self.current_round >= self.max_rounds or self.game_over
    
    def reset(self):
        """Reset the game and strategies to initial state"""
        self.current_round = 0
        self.game_over = False
        self.rounds = []
        self.player1_total_score = 0
        self.player2_total_score = 0
        self.player1_strategy.reset()
        self.player2_strategy.reset()