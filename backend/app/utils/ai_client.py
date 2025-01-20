from typing import Dict, Tuple, Optional, List
import os
from dotenv import load_dotenv
import anthropic
from time import sleep
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

class AIClientError(Exception):
    """Custom exception for AI client errors"""
    pass

class GameAIClient:
    def __init__(self, max_retries: int = 3, retry_delay: float = 1.0):
        """Initialize the AI client with Claude

        Args:
            max_retries: Maximum number of API call retries
            retry_delay: Delay between retries in seconds
        """
        if not CLAUDE_API_KEY:
            raise AIClientError("CLAUDE_API_KEY not found in environment variables")
        
        self.client = anthropic.Anthropic(
            api_key=CLAUDE_API_KEY
        )
        # TODO: Figure out Anthropic API

        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
    def _create_game_prompt(self, game_state: Dict, history: List[Dict]) -> str:
        """Create the prompt for the AI based on game state and history
        
        Args:
            game_state: Current state of the game
            history: List of previous moves and outcomes

        Returns:
            str: Formatted prompt for Claude
        """
        # TODO: Implement proper prompt engineering
        prompt = """
        You are playing an iterated prisoner's dilemma game. 
        The possible moves are 'cooperate' or 'defect'.
        Based on the game history and current state, decide your next move.
        
        Current game state:
        {game_state}
        
        Game history:
        {history}
        
        Provide your move (cooperate/defect) and explain your reasoning.
        """.format(
            game_state=game_state,
            history=history
        )
        return prompt

    def _parse_response(self, response: str) -> Tuple[str, str]:
        """Parse Claude's response to extract move and reasoning
        
        Args:
            response: Raw response from Claude

        Returns:
            Tuple[str, str]: (move, reasoning)
        
        Raises:
            AIClientError: If response cannot be parsed
        """
        # TODO: Implement proper response parsing
        try:
            # Placeholder parsing logic
            if "cooperate" in response.lower():
                move = "cooperate"
            elif "defect" in response.lower():
                move = "defect"
            else:
                raise AIClientError("Could not determine move from response")
            
            reasoning = response
            return move, reasoning
            
        except Exception as e:
            raise AIClientError(f"Failed to parse AI response: {str(e)}")

    async def get_move(self, game_state: Dict, history: List[Dict]) -> Tuple[str, str]:
        """Get the AI's next move and reasoning
        
        Args:
            game_state: Current state of the game
            history: List of previous moves and outcomes

        Returns:
            Tuple[str, str]: (move, reasoning)
            
        Raises:
            AIClientError: If unable to get valid move after retries
        """
        prompt = self._create_game_prompt(game_state, history)
        
        for attempt in range(self.max_retries):
            try:
                response = await self.client.complete(prompt)
                move, reasoning = self._parse_response(response.content)
                return move, reasoning
                
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < self.max_retries - 1:
                    sleep(self.retry_delay)
                    continue
                raise AIClientError(f"Failed to get AI move after {self.max_retries} attempts")

    async def reset_context(self):
        """Reset the conversation context with Claude"""
        # TODO: Implement context reset if needed
        pass

    def validate_move(self, move: str) -> bool:
        """Validate if the move is legal
        
        Args:
            move: The move to validate

        Returns:
            bool: True if move is valid, False otherwise
        """
        return move.lower() in ['cooperate', 'defect']