from pathlib import Path
import sqlite3
from typing import Optional, List, Dict, Tuple
from datetime import datetime
import pandas as pd
from dataclasses import dataclass, asdict

# Local imports
from app.models.types import PayoffMatrix, Move, RoundResult

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
        self.init_database()
        
        # Directory for CSV storage
        self.csv_dir = self.data_dir / "game_data"
        self.csv_dir.mkdir(exist_ok=True)

    def init_database(self):
        """Initialize SQLite database with required tables"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
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
        
        conn.commit()
        conn.close()

    def save_experiment(self, result: ExperimentResult):
        """Save experiment results"""
        # Save metadata to SQLite
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute(
            "INSERT INTO experiments VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (
                result.experiment_id,
                result.matrix_type,
                result.player1_strategy,
                result.player2_strategy,
                str(result.payoff_matrix),
                result.start_time,
                result.end_time,
                len(result.games),
                result.metrics.cooperation_rate,
                result.metrics.points_below_optimal,
                result.metrics.learning_rate
            )
        )
        conn.commit()
        
        # Save detailed game data as CSV
        games_df = self._games_to_dataframe(result)
        csv_path = self.csv_dir / f"{result.experiment_id}_games.csv"
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
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
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
        conn = sqlite3.connect(self.db_path)
        return pd.read_sql("SELECT * FROM experiments", conn)