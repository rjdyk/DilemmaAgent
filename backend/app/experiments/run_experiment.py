# experiments/run_experiment.py
import asyncio
from app.utils.experiment_runner import ExperimentConfig, ExperimentRunner
from app.utils.experiment_storage import ExperimentStorage
from app.models.types import MatrixType
from app.strategies import StrategyType

async def run_matrix_experiment(matrix_type: MatrixType):
    config = ExperimentConfig(
        matrix_type=matrix_type,
        num_games=10,
        num_rounds=5
    )
    storage = ExperimentStorage()
    runner = ExperimentRunner(config, storage)
    results = await runner.run_full_experiment()
    return results.experiment_id

async def test_run():
    config = ExperimentConfig(
        matrix_type=MatrixType.BASELINE,
        num_games=5,
        num_rounds=5,
        strategies_to_test=[
            StrategyType.ALWAYS_COOPERATE,
            StrategyType.ALWAYS_DEFECT,
            # StrategyType.OPTIMAL
        ]
    )
    storage = ExperimentStorage()
    runner = ExperimentRunner(config, storage)
    results = await runner.run_full_experiment()
    return results.experiment_id

async def main():
    # Run experiments for different matrices
    experiment_ids = []
    for matrix_type in [MatrixType.BASELINE, MatrixType.MIXED_30, MatrixType.MIXED_70, MatrixType.PURE_DEFECT]:
        experiment_id = await run_matrix_experiment(matrix_type)
        experiment_ids.append(experiment_id)
        print(f"Completed experiment {experiment_id} for matrix {matrix_type.value}")
    return experiment_ids

if __name__ == "__main__":
    experiment_ids = asyncio.run(main())
