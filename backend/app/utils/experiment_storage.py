from pathlib import Path
import sqlite3
from typing import Optional, List, Dict, Tuple
from datetime import datetime
import pandas as pd
from dataclasses import dataclass, asdict

# Local imports
from app.models.types import (
    PayoffMatrix, Move, RoundResult, OptimalStrategy,
    ExperimentMetrics, GameResult, ExperimentResult
)

@dataclass
class ExperimentMetrics:
    cooperation_rate: float
    points_below_optimal: float
    learning_rate: float
    avg_score: float
    total_rounds: int 

@dataclass 
class GameResult:
    game_id: str
    rounds: List
    final_scores: Tuple[int, int]
    cooperation_rate: float
    total_rounds: int

@dataclass
class ExperimentResult:
    experiment_id: str
    matrix_type: str
    player1_strategy: str
    player2_strategy: str
    payoff_matrix: PayoffMatrix
    start_time: datetime
    end_time: datetime
    games: List[GameResult]
    metrics: ExperimentMetrics


class ExperimentStorage:
    def __init__(self, data_dir: str = "experiment_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Create SQLite database for experiment metadata
        self.db_path = self.data_dir / "experiments.db"
        self.connection = sqlite3.connect(self.db_path)
        self.init_database()
        
        # Directory for CSV storage
        self.csv_dir = self.data_dir / "game_data"
        self.csv_dir.mkdir(exist_ok=True)

    def init_database(self):
        """Initialize SQLite database with required tables"""
        c = self.connection.cursor()
        
        # Create experiments table
        c.execute('''
            CREATE TABLE IF NOT EXISTS experiments (
                experiment_id TEXT PRIMARY KEY,
                matrix_type TEXT,
                player1_strategy TEXT,
                player2_strategy TEXT,
                payoff_matrix TEXT,
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                total_games INTEGER,
                cooperation_rate REAL,
                points_below_optimal REAL,
                learning_rate REAL
            )
        ''')
        
        self.connection.commit()

    def save_experiment(self, experiment_result: ExperimentResult):
        """Save experiment results to the database with upsert logic."""
        with self.connection:
            c = self.connection.cursor()
            c.execute(
                """
                INSERT INTO experiments (experiment_id, matrix_type, player1_strategy, player2_strategy, 
                                         payoff_matrix, start_time, end_time, total_games, cooperation_rate, 
                                         points_below_optimal, learning_rate)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(experiment_id) DO UPDATE SET
                    matrix_type = excluded.matrix_type,
                    player1_strategy = excluded.player1_strategy,
                    player2_strategy = excluded.player2_strategy,
                    payoff_matrix = excluded.payoff_matrix,
                    start_time = excluded.start_time,
                    end_time = excluded.end_time,
                    total_games = excluded.total_games,
                    cooperation_rate = excluded.cooperation_rate,
                    points_below_optimal = excluded.points_below_optimal,
                    learning_rate = excluded.learning_rate
                """,
                (
                    experiment_result.experiment_id,
                    experiment_result.matrix_type,
                    experiment_result.player1_strategy,
                    experiment_result.player2_strategy,
                    str(experiment_result.payoff_matrix),  # Ensure this is a string if necessary
                    experiment_result.start_time,
                    experiment_result.end_time,
                    len(experiment_result.games),  # Assuming you want to store the number of games
                    experiment_result.metrics.cooperation_rate,
                    experiment_result.metrics.points_below_optimal,
                    experiment_result.metrics.learning_rate
                )
            )
        
        # Save detailed game data as CSV
        games_df = self._games_to_dataframe(experiment_result)
        csv_path = self.csv_dir / f"{experiment_result.experiment_id}_games.csv"
        games_df.to_csv(csv_path, index=False)

    def _games_to_dataframe(self, result: ExperimentResult) -> pd.DataFrame:
        """Convert game results to pandas DataFrame for analysis"""
        rows = []
        for game in result.games:
            for round in game.rounds:
                rows.append({
                    'experiment_id': result.experiment_id,
                    'game_id': game.game_id,
                    'matrix_type': result.matrix_type,
                    'round_number': round.round_number,
                    'player1_move': round.player1_move.value,
                    'player2_move': round.player2_move.value,
                    'player1_score': round.player1_score,
                    'player2_score': round.player2_score,
                    'cumulative_player1_score': round.cumulative_player1_score,
                    'cumulative_player2_score': round.cumulative_player2_score,
                    'player1_reasoning': round.player1_reasoning,
                    'player2_reasoning': round.player2_reasoning
                })
        return pd.DataFrame(rows)

    def get_experiment_results(self, experiment_id: str) -> Optional[ExperimentResult]:
        """Retrieve full experiment results"""
        # Get metadata from SQLite
        c = self.connection.cursor()
        c.execute("SELECT * FROM experiments WHERE experiment_id = ?", (experiment_id,))
        metadata = c.fetchone()
        if not metadata:
            return None

        # Get detailed game data from CSV
        csv_path = self.csv_dir / f"{experiment_id}_games.csv"
        games_df = pd.read_csv(csv_path)
        
        return self._construct_experiment_result(metadata, games_df)

    def get_experiments_summary(self) -> pd.DataFrame:
        """Get summary of all experiments"""
        return pd.read_sql("SELECT * FROM experiments", self.connection)
    
    def _construct_experiment_result(self, metadata, games_df) -> ExperimentResult:
        """
        Construct ExperimentResult from database metadata and games DataFrame
        
        Args:
            metadata: Row tuple from SQLite experiments table
            games_df: DataFrame containing detailed game data
        """
        # Convert metadata row to dict for easier access
        meta_dict = {
            "experiment_id": metadata[0],
            "matrix_type": metadata[1],
            "player1_strategy": metadata[2],
            "player2_strategy": metadata[3],
            "payoff_matrix": eval(metadata[4]),  # Careful with eval!
            "start_time": datetime.fromisoformat(metadata[5]),
            "end_time": datetime.fromisoformat(metadata[6]),
            "total_games": metadata[7],
            "cooperation_rate": metadata[8],
            "points_below_optimal": metadata[9],
            "learning_rate": metadata[10]
        }
        
        # Group DataFrame by game_id to reconstruct games
        games = []
        for game_id, game_df in games_df.groupby('game_id'):
            # Convert moves back to Move enum
            rounds = [
                RoundResult(
                    round_number=row['round_number'],
                    player1_move=Move(row['player1_move']),
                    player2_move=Move(row['player2_move']),
                    player1_reasoning=row['player1_reasoning'],
                    player2_reasoning=row['player2_reasoning'],
                    player1_score=row['player1_score'],
                    player2_score=row['player2_score'],
                    cumulative_player1_score=row['cumulative_player1_score'],
                    cumulative_player2_score=row['cumulative_player2_score']
                )
                for _, row in game_df.iterrows()
            ]
            
            # Calculate final scores from last round
            final_scores = (
                game_df.iloc[-1]['cumulative_player1_score'],
                game_df.iloc[-1]['cumulative_player2_score']
            )
            
            # Calculate cooperation rate
            coop_moves = (
                (game_df['player1_move'] == 'cooperate').sum() +
                (game_df['player2_move'] == 'cooperate').sum()
            )
            total_moves = len(game_df) * 2
            cooperation_rate = coop_moves / total_moves
            
            games.append(GameResult(
                game_id=game_id,
                rounds=rounds,
                final_scores=final_scores,
                cooperation_rate=cooperation_rate,
                total_rounds=len(rounds)
            ))
        
        # Construct metrics from metadata
        metrics = ExperimentMetrics(
            cooperation_rate=meta_dict['cooperation_rate'],
            points_below_optimal=meta_dict['points_below_optimal'],
            learning_rate=meta_dict['learning_rate'],
            avg_score=sum(g.final_scores[0] for g in games) / len(games),
            total_rounds=sum(g.total_rounds for g in games)
        )
        
        return ExperimentResult(
            experiment_id=meta_dict['experiment_id'],
            matrix_type=meta_dict['matrix_type'],
            player1_strategy=meta_dict['player1_strategy'],
            player2_strategy=meta_dict['player2_strategy'],
            payoff_matrix=meta_dict['payoff_matrix'],
            start_time=meta_dict['start_time'],
            end_time=meta_dict['end_time'],
            games=games,
            metrics=metrics
        )