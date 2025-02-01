from typing import List, Dict, Optional
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Local imports
from app.utils.experiment_storage import ExperimentStorage, ExperimentResult
from app.models.types import MatrixType, Move

class ExperimentAnalyzer:
    def __init__(self, storage: ExperimentStorage):
        self.storage = storage

    def plot_cooperation_rates(self, experiment_id: str):
        """Plot cooperation rates over rounds"""
        df = self._load_experiment_data(experiment_id)
        # Use matplotlib or plotly for visualizations
        
    def plot_score_distribution(self, experiment_id: str):
        """Plot distribution of scores"""
        pass

    def plot_learning_rate(self, experiment_id: str):
        """Plot how cooperation rate changes over time"""
        pass

    def generate_summary_report(self, experiment_id: str):
        """Generate comprehensive analysis report"""
        pass

    def _load_experiment_data(self, experiment_id: str) -> pd.DataFrame:
        """Load and preprocess experiment data"""
        csv_path = self.storage.csv_dir / f"{experiment_id}_games.csv"
        return pd.read_csv(csv_path)

    def get_experiment_summary(self, experiment_id: str) -> dict:
        """Get high-level experiment statistics"""
        experiment = self.storage.get_experiment_results(experiment_id)
        if not experiment:
            raise ValueError(f"No experiment found with id {experiment_id}")
            
        return {
            "experiment_id": experiment.experiment_id,
            "matrix_type": experiment.matrix_type,
            "start_time": experiment.start_time,
            "end_time": experiment.end_time,
            "games_summary": [
                {
                    "game_id": game.game_id,
                    "opponent_strategy": experiment.player2_strategy,
                    "cooperation_rate": game.cooperation_rate,
                    "final_scores": game.final_scores,
                    "ai_won": game.final_scores[0] > game.final_scores[1],
                    "rounds_played": game.total_rounds
                }
                for game in experiment.games
            ]
        }

    def get_game_details(self, experiment_id: str, game_id: str) -> dict:
        """Get detailed round-by-round information for a specific game"""
        experiment = self.storage.get_experiment_results(experiment_id)
        if not experiment:
            raise ValueError(f"No experiment found with id {experiment_id}")
            
        game = next((g for g in experiment.games if g.game_id == game_id), None)
        if not game:
            raise ValueError(f"No game found with id {game_id}")
            
        return {
            "game_id": game.game_id,
            "rounds": [
                {
                    "round_number": r.round_number,
                    "player1_move": r.player1_move.value,
                    "player2_move": r.player2_move.value,
                    "player1_score": r.player1_score,
                    "player2_score": r.player2_score,
                    "cumulative_player1_score": r.cumulative_player1_score,
                    "cumulative_player2_score": r.cumulative_player2_score,
                    "ai_reasoning": r.player1_reasoning
                }
                for r in game.rounds
            ],
            "final_scores": game.final_scores,
            "cooperation_rate": game.cooperation_rate
        }