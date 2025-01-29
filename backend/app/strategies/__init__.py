import os
from dotenv import load_dotenv
from enum import Enum
from typing import Dict, Type

from .base import BaseStrategy
from .always_cooperate import AlwaysCooperate
from .always_defect import AlwaysDefect
from .tit_for_tat import TitForTat
from .pavlov import Pavlov
from .random_strategy import RandomStrategy
from .grim import GrimTrigger
from .haiku_strategy import HaikuStrategy

# Load environment variables
load_dotenv()

class StrategyType(Enum):
    """Available opponent strategies"""
    ALWAYS_COOPERATE = "always_cooperate"
    ALWAYS_DEFECT = "always_defect"
    TIT_FOR_TAT = "tit_for_tat"
    PAVLOV = "pavlov"
    RANDOM = "random"
    GRIM = "grim"
    CLAUDE_HAIKU = "claude_haiku"


# Registry mapping strategy types to their implementing classes
_strategy_registry: Dict[StrategyType, Type[BaseStrategy]] = {
    StrategyType.ALWAYS_COOPERATE: AlwaysCooperate,
    StrategyType.ALWAYS_DEFECT: AlwaysDefect,
    StrategyType.TIT_FOR_TAT: TitForTat,
    StrategyType.PAVLOV: Pavlov,
    StrategyType.RANDOM: RandomStrategy,
    StrategyType.GRIM: GrimTrigger,
}


def register_strategy(strategy_type: StrategyType, strategy_class: Type[BaseStrategy]):
    """
    Register a new strategy implementation
    
    Args:
        strategy_type: The enum type for this strategy
        strategy_class: The class that implements this strategy
    
    Raises:
        ValueError: If the strategy type is already registered
    """
    if strategy_type in _strategy_registry:
        raise ValueError(f"Strategy {strategy_type} is already registered")
    
    _strategy_registry[strategy_type] = strategy_class


def create_strategy(strategy_type: StrategyType, is_player1: bool) -> BaseStrategy:
    """
    Create a new instance of the specified strategy
    
    Args:
        strategy_type: The type of strategy to create
        is_player1: Whether this strategy is for player 1 (True) or player 2 (False)
    
    Returns:
        BaseStrategy: A new instance of the requested strategy
    
    Raises:
        ValueError: If the strategy type is not registered or environment variables are missing
    """
    # Special handling for Haiku strategy since it needs API key
    if strategy_type == StrategyType.CLAUDE_HAIKU:
        api_key = os.getenv('CLAUDE_API_KEY')
        if not api_key:
            raise ValueError("CLAUDE_API_KEY not found in environment variables")
        return HaikuStrategy(
            name="Claude Haiku",
            is_player1=is_player1,
            api_key=api_key
        )
    
    # Handle other strategies normally
    if strategy_type not in _strategy_registry:
        raise ValueError(f"Strategy {strategy_type.value} is not implemented yet")
    
    strategy_class = _strategy_registry[strategy_type]
    return strategy_class(is_player1=is_player1)

def get_available_strategies() -> list[StrategyType]:
    """
    Get a list of all registered strategy types
    
    Returns:
        list[StrategyType]: List of available strategy types
    """
    return list(_strategy_registry.keys())


def get_strategy_name(strategy_type: StrategyType) -> str:
    """
    Get the display name for a strategy type
    
    Args:
        strategy_type: The strategy type
    
    Returns:
        str: The human-readable name of the strategy
    """
    return strategy_type.value.replace('_', ' ').title()