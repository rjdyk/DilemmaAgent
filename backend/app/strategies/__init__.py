from enum import Enum
from typing import Dict, Type

from .base import BaseStrategy
from .always_cooperate import AlwaysCooperate
# Import other strategies as they are implemented
# from .always_defect import AlwaysDefect
# from .tit_for_tat import TitForTat
# from .pavlov import Pavlov
# from .random import RandomStrategy
# from .grim import GrimTrigger


class StrategyType(Enum):
    """Available opponent strategies"""
    ALWAYS_COOPERATE = "always_cooperate"
    ALWAYS_DEFECT = "always_defect"
    TIT_FOR_TAT = "tit_for_tat"
    PAVLOV = "pavlov"
    RANDOM = "random"
    GRIM = "grim"


# Registry mapping strategy types to their implementing classes
_strategy_registry: Dict[StrategyType, Type[BaseStrategy]] = {
    StrategyType.ALWAYS_COOPERATE: AlwaysCooperate,
    # Add other strategies as they are implemented
    # StrategyType.ALWAYS_DEFECT: AlwaysDefect,
    # StrategyType.TIT_FOR_TAT: TitForTat,
    # StrategyType.PAVLOV: Pavlov,
    # StrategyType.RANDOM: RandomStrategy,
    # StrategyType.GRIM: GrimTrigger,
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


def create_strategy(strategy_type: StrategyType) -> BaseStrategy:
    """
    Create a new instance of the specified strategy
    
    Args:
        strategy_type: The type of strategy to create
    
    Returns:
        BaseStrategy: A new instance of the requested strategy
    
    Raises:
        ValueError: If the strategy type is not registered
    """
    if strategy_type not in _strategy_registry:
        raise ValueError(f"Unknown strategy type: {strategy_type}")
    
    strategy_class = _strategy_registry[strategy_type]
    return strategy_class()


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