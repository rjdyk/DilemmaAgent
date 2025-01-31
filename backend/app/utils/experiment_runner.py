from typing import List, Optional, Dict, Tuple
from datetime import datetime
import asyncio
import uuid
import logging
from dataclasses import dataclass

# Local imports
from app.models.types import MatrixType, Move, PayoffMatrix, MATRIX_PAYOFFS
from app.models.game import Game
from app.strategies import create_strategy, StrategyType
from app.utils.experiment_storage import ExperimentStorage, ExperimentResult, ExperimentMetrics, GameResult

logger = logging.getLogger(__name__)

@dataclass
class ExperimentConfig:
    matrix_type: MatrixType
    num_games: int = 100
    num_rounds: int = 10
    strategies_to_test: List[StrategyType] = None
    
    def __post_init__(self):
        if self.strategies_to_test is None:
            # Default strategies to test against
            self.strategies_to_test = [
                StrategyType.ALWAYS_COOPERATE,
                StrategyType.ALWAYS_DEFECT,
                StrategyType.TIT_FOR_TAT,
                StrategyType.RANDOM,
                StrategyType.CLAUDE_HAIKU  # LLM vs LLM
            ]

class ExperimentRunner:
    def __init__(self, config: ExperimentConfig, storage: ExperimentStorage):
        self.config = config
        self.storage = storage
        self.payoff_matrix = MATRIX_PAYOFFS[config.matrix_type]
        self.experiment_id = str(uuid.uuid4())
        self.start_time = None
        self.end_time = None

    def set_progress_callback(self, callback):
        self.progress_callback = callback
        
    async def run_full_experiment(self) -> ExperimentResult:
        """Run complete experiment testing AI against all specified strategies"""
        self.start_time = datetime.now()
        logger.info(f"Starting experiment {self.experiment_id} with matrix {self.config.matrix_type}")
        
        all_games: List[GameResult] = []
        
        # Test AI against each strategy
        for opponent_strategy in self.config.strategies_to_test:
            logger.info(f"Testing against {opponent_strategy}")
            
            # For LLM vs LLM, both players use Claude
            if opponent_strategy == StrategyType.CLAUDE_HAIKU:
                games = await self._run_llm_vs_llm_games()
            else:
                games = await self._run_strategy_games(opponent_strategy)
            
            all_games.extend(games)
            
        self.end_time = datetime.now()
        
        # Calculate overall metrics
        metrics = self._calculate_experiment_metrics(all_games)
        
        # Create experiment result
        result = ExperimentResult(
            experiment_id=self.experiment_id,
            matrix_type=self.config.matrix_type.value,
            player1_strategy="claude_haiku",
            player2_strategy="multiple",
            payoff_matrix=self.payoff_matrix,
            start_time=self.start_time,
            end_time=self.end_time,
            games=all_games,
            metrics=metrics
        )
        
        # Save results
        self.storage.save_experiment(result)
        
        return result
        
    async def _run_strategy_games(self, opponent_strategy: StrategyType) -> List[GameResult]:
        """Run batch of games against a specific strategy"""
        games: List[GameResult] = []

        
        for game_num in range(self.config.num_games):
            # Create strategies
            ai_strategy = create_strategy(StrategyType.CLAUDE_HAIKU, is_player1=True)
            opponent = create_strategy(opponent_strategy, is_player1=False)
            
            # Create and run game
            game = Game(
                player1_strategy=ai_strategy,
                player2_strategy=opponent,
                max_rounds=self.config.num_rounds,
                payoff_matrix=self.payoff_matrix
            )

            if hasattr(self, 'progress_callback'):
                self.progress_callback(opponent_strategy.value, game_num + 1, game.current_round)
            
            game_result = await self._run_single_game(game)
            games.append(game_result)
            
        return games
            
    async def _run_llm_vs_llm_games(self) -> List[GameResult]:
        """Run batch of games with LLM playing against itself"""
        games: List[GameResult] = []
        
        for game_num in range(self.config.num_games):
            # Create two AI strategies
            ai_player1 = create_strategy(StrategyType.CLAUDE_HAIKU, is_player1=True)
            ai_player2 = create_strategy(StrategyType.CLAUDE_HAIKU, is_player1=False)
            
            game = Game(
                player1_strategy=ai_player1,
                player2_strategy=ai_player2,
                max_rounds=self.config.num_rounds,
                payoff_matrix=self.payoff_matrix
            )
            
            game_result = await self._run_single_game(game)
            games.append(game_result)
            
        return games
    
    async def _run_single_game(self, game: Game) -> GameResult:
        """Run a single game to completion and return results"""
        game_id = str(uuid.uuid4())
        
        try:
            results = await game.run_all_rounds()
            
            # Calculate cooperation rate
            p1_coop_moves = sum(1 for r in results if r.player1_move == Move.COOPERATE)
            p2_coop_moves = sum(1 for r in results if r.player2_move == Move.COOPERATE)
            avg_coop_rate = (p1_coop_moves + p2_coop_moves) / (2 * len(results))
            
            return GameResult(
                game_id=game_id,
                rounds=results,
                final_scores=(game.player1_total_score, game.player2_total_score),
                cooperation_rate=avg_coop_rate,
                total_rounds=len(results)
            )
            
        except Exception as e:
            logger.error(f"Error in game {game_id}: {str(e)}")
            raise
    
    def _calculate_experiment_metrics(self, games: List[GameResult]) -> ExperimentMetrics:
        """Calculate aggregate metrics across all games"""
        total_games = len(games)
        if total_games == 0:
            raise ValueError("No games to analyze")
            
        # Calculate average cooperation rate
        avg_coop_rate = sum(g.cooperation_rate for g in games) / total_games
        
        # Calculate average score difference from optimal
        optimal_score = self.payoff_matrix.optimal_strategy.expected_score_per_round[0]
        actual_scores = [g.final_scores[0]/g.total_rounds for g in games]
        avg_score_diff = sum(optimal_score - score for score in actual_scores) / total_games
        
        # Calculate "learning rate" - change in cooperation over time
        early_coop = sum(g.cooperation_rate for g in games[:total_games//2]) / (total_games//2)
        late_coop = sum(g.cooperation_rate for g in games[total_games//2:]) / (total_games - total_games//2)
        learning_rate = late_coop - early_coop
        
        return ExperimentMetrics(
            cooperation_rate=avg_coop_rate,
            points_below_optimal=avg_score_diff,
            learning_rate=learning_rate,
            avg_score=sum(g.final_scores[0] for g in games) / total_games,
            total_rounds=sum(g.total_rounds for g in games)
        )