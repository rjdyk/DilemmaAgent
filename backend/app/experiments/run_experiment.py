# experiments/run_experiment.py
import asyncio
from datetime import datetime
from app.utils.experiment_runner import ExperimentConfig, ExperimentRunner
from app.utils.experiment_storage import ExperimentStorage
from app.models.types import MatrixType
from app.strategies import StrategyType

async def run_matrix_experiment(matrix_type: MatrixType):
    config = ExperimentConfig(
        matrix_type=matrix_type,
        num_games=20,
        num_rounds=5
    )
    storage = ExperimentStorage()
    runner = ExperimentRunner(config, storage)
    
    # Add progress callback
    def progress_callback(strategy: str, game_num: int, round_num: int):
        print(f"Strategy: {strategy:15} Game: {game_num}/10  Round: {round_num}/10", end='\r')
    
    runner.set_progress_callback(progress_callback)
    results = await runner.run_full_experiment()
    return results.experiment_id

async def main():
    # Run experiments for different matrices
    print(f"\nStarting experiments at {datetime.now().strftime('%H:%M:%S')}")
    
    experiment_ids = []
    for matrix_type in [MatrixType.BASELINE, MatrixType.MIXED_30, MatrixType.MIXED_70]:
        print(f"\nRunning experiment for matrix: {matrix_type.value}")
        experiment_id = await run_matrix_experiment(matrix_type)
        experiment_ids.append(experiment_id)
        print(f"\nCompleted experiment {experiment_id} for matrix {matrix_type.value}")
    
    print(f"\nAll experiments completed at {datetime.now().strftime('%H:%M:%S')}")
    return experiment_ids

if __name__ == "__main__":
    experiment_ids = asyncio.run(main())
