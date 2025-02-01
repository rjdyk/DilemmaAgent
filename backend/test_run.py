# test_run.py
import asyncio
from datetime import datetime
from app.utils.experiment_runner import ExperimentConfig, ExperimentRunner
from app.utils.experiment_storage import ExperimentStorage
from app.models.types import MatrixType
from app.strategies import StrategyType

async def test_run():
    print(f"\nStarting test run at {datetime.now().strftime('%H:%M:%S')}")
    
    config = ExperimentConfig(
        matrix_type=MatrixType.MIXED_30,
        num_games=5,
        num_rounds=5,
        strategies_to_test=[
            StrategyType.OPTIMAL,
        ]
    )
    storage = ExperimentStorage()
    runner = ExperimentRunner(config, storage)
    
    def progress_callback(strategy: str, game_num: int, round_num: int):
        print(f"Strategy: {strategy:15} Game: {game_num}/5  Round: {round_num}/5", end='\r')
    
    runner.set_progress_callback(progress_callback)
    results = await runner.run_full_experiment()
    
    print(f"\nExperiment completed at {datetime.now().strftime('%H:%M:%S')}")
    print(f"Experiment ID: {results.experiment_id}")
    return results.experiment_id

if __name__ == "__main__":
    experiment_id = asyncio.run(test_run())