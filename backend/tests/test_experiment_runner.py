import pytest
from unittest.mock import Mock, AsyncMock, patch
import asyncio
from datetime import datetime

from app.models.types import MatrixType, Move, PayoffMatrix, OptimalStrategy
from app.models.game import Game
from app.strategies import StrategyType
from app.utils.experiment_runner import ExperimentRunner, ExperimentConfig
from app.utils.experiment_storage import ExperimentStorage, GameResult, ExperimentMetrics

# Test fixtures
@pytest.fixture
def mock_storage():
    storage = Mock(spec=ExperimentStorage)
    storage.save_experiment = AsyncMock()
    return storage

@pytest.fixture
def basic_config():
    return ExperimentConfig(
        matrix_type=MatrixType.MIXED_30,
        num_games=2,  # Small number for testing
        num_rounds=3,
        strategies_to_test=[StrategyType.ALWAYS_COOPERATE]  # Just one strategy for basic tests
    )

@pytest.fixture
def mock_game():
    game = Mock(spec=Game)
    game.player1_total_score = 10
    game.player2_total_score = 8
    game.run_all_rounds = AsyncMock(return_value=[
        Mock(
            player1_move=Move.COOPERATE,
            player2_move=Move.COOPERATE,
            player1_score=3,
            player2_score=3,
            round_number=1
        ),
        Mock(
            player1_move=Move.DEFECT,
            player2_move=Move.COOPERATE,
            player1_score=5,
            player2_score=0,
            round_number=2
        )
    ])
    return game

@pytest.fixture
def runner(basic_config, mock_storage):
    return ExperimentRunner(basic_config, mock_storage)

# Test experiment configuration
def test_experiment_config_default_strategies():
    """Test that default strategies are set correctly"""
    config = ExperimentConfig(matrix_type=MatrixType.MIXED_30)
    assert len(config.strategies_to_test) > 0
    assert StrategyType.ALWAYS_COOPERATE in config.strategies_to_test
    assert StrategyType.ALWAYS_DEFECT in config.strategies_to_test

def test_experiment_config_custom_strategies():
    """Test that custom strategies override defaults"""
    custom_strategies = [StrategyType.ALWAYS_COOPERATE]
    config = ExperimentConfig(
        matrix_type=MatrixType.MIXED_30,
        strategies_to_test=custom_strategies
    )
    assert config.strategies_to_test == custom_strategies

# Test experiment runner initialization
def test_experiment_runner_initialization(runner):
    """Test runner initializes correctly"""
    assert runner.experiment_id is not None
    assert runner.start_time is None
    assert runner.payoff_matrix is not None

# Test single game execution
@pytest.mark.asyncio
async def test_run_single_game(runner, mock_game):
    """Test running a single game"""
    result = await runner._run_single_game(mock_game)
    
    assert isinstance(result, GameResult)
    assert result.game_id is not None
    assert result.cooperation_rate == 0.75  # 3/4 moves were cooperate
    assert result.total_rounds == 2

# Test strategy games execution
@pytest.mark.asyncio
async def test_run_strategy_games(runner):
    """Test running games against a specific strategy"""
    with patch('app.utils.experiment_runner.Game') as MockGame:
        mock_game = Mock(spec=Game)
        mock_game.run_all_rounds = AsyncMock(return_value=[
            Mock(
                player1_move=Move.COOPERATE,
                player2_move=Move.COOPERATE,
                player1_score=3,
                player2_score=3,
                round_number=1
            )
        ])
        mock_game.player1_total_score = 3
        mock_game.player2_total_score = 3
        MockGame.return_value = mock_game
        
        games = await runner._run_strategy_games(StrategyType.ALWAYS_COOPERATE)
        
        assert len(games) == runner.config.num_games
        assert all(isinstance(g, GameResult) for g in games)

# Test metrics calculation
def test_calculate_experiment_metrics(runner):
    """Test metrics calculation"""
    games = [
        GameResult(
            game_id="1",
            rounds=[Mock(player1_move=Move.COOPERATE, player2_move=Move.COOPERATE)],
            final_scores=(3, 3),
            cooperation_rate=1.0,
            total_rounds=1
        ),
        GameResult(
            game_id="2",
            rounds=[Mock(player1_move=Move.DEFECT, player2_move=Move.DEFECT)],
            final_scores=(1, 1),
            cooperation_rate=0.0,
            total_rounds=1
        )
    ]
    
    metrics = runner._calculate_experiment_metrics(games)
    
    assert isinstance(metrics, ExperimentMetrics)
    assert metrics.cooperation_rate == 0.5
    assert metrics.total_rounds == 2

# Test full experiment execution
@pytest.mark.asyncio
async def test_run_full_experiment(runner):
    """Test running a complete experiment"""
    with patch('app.utils.experiment_runner.Game') as MockGame:
        mock_game = Mock(spec=Game)
        mock_game.run_all_rounds = AsyncMock(return_value=[
            Mock(
                player1_move=Move.COOPERATE,
                player2_move=Move.COOPERATE,
                player1_score=3,
                player2_score=3,
                round_number=1
            )
        ])
        mock_game.player1_total_score = 3 
        mock_game.player2_total_score = 3        
        MockGame.return_value = mock_game
        
        result = await runner.run_full_experiment()
        
        assert result.experiment_id == runner.experiment_id
        assert result.start_time is not None
        assert result.end_time is not None
        assert len(result.games) == runner.config.num_games
        assert runner.storage.save_experiment.called

# Test error handling
@pytest.mark.asyncio
async def test_error_handling_in_single_game(runner, mock_game):
    """Test error handling in single game execution"""
    mock_game.run_all_rounds.side_effect = Exception("Game error")
    
    with pytest.raises(Exception):
        await runner._run_single_game(mock_game)

# Test LLM vs LLM games
@pytest.mark.asyncio
async def test_run_llm_vs_llm_games(runner):
    """Test running games between two LLM agents"""
    with patch('app.utils.experiment_runner.Game') as MockGame:
        mock_game = Mock(spec=Game)
        mock_game.run_all_rounds = AsyncMock(return_value=[
            Mock(
                player1_move=Move.COOPERATE,
                player2_move=Move.COOPERATE,
                player1_score=3,
                player2_score=3,
                round_number=1
            )
        ])
        mock_game.player1_total_score = 3 
        mock_game.player2_total_score = 3 
        MockGame.return_value = mock_game
        
        games = await runner._run_llm_vs_llm_games()
        
        assert len(games) == runner.config.num_games
        assert all(isinstance(g, GameResult) for g in games)

# Test empty games handling
def test_metrics_calculation_empty_games(runner):
    """Test metrics calculation with empty games list"""
    with pytest.raises(ValueError):
        runner._calculate_experiment_metrics([])