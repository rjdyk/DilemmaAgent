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