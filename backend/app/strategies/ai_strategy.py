from typing import Optional, List, Dict
from dataclasses import dataclass, asdict
import asyncio
from app.models.types import Move, RoundResult
from app.strategies.base import BaseStrategy

@dataclass
class TokenUsage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

@dataclass
class AIResponse:
    move: Move
    reasoning: str
    token_usage: TokenUsage

class AIStrategy(BaseStrategy):
    def __init__(
        self,
        name: str,
        is_player1: bool,
        token_budget: int = 4000,
        max_retries: int = 3,
        retry_delay: float = 1.0
    ):
        super().__init__(name, is_player1)
        self.token_budget = token_budget
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.total_tokens_used = 0
        self.conversation_history: List[Dict] = []
        self._last_error: Optional[str] = None
        self.current_round = 0

    async def get_move(self, current_round: int) -> Move:
        """Get the AI's next move"""
        self.current_round = current_round

        # Token budget check 
        estimated_next_tokens = 200  
        if self.total_tokens_used + estimated_next_tokens > self.token_budget:
            self._last_error = "Token budget exceeded"
            return self._get_fallback_move(self._last_error)

        last_error = None
        for attempt in range(self.max_retries):
            try:
                response = await self._get_ai_response(current_round)
                
                # Check if this response would exceed budget
                if self.total_tokens_used + response.token_usage.total_tokens > self.token_budget:
                    self._last_error = "Token budget would be exceeded"
                    return self._get_fallback_move(self._last_error)
                    
                self._update_token_usage(response.token_usage)
                self._record_interaction(current_round, response)
                return response.move

            except Exception as e:
                last_error = str(e)
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay)
                    continue
        
        # If we get here, we've failed all retries
        self._last_error = f"Failed after {self.max_retries} attempts. Last error: {last_error}"
        return self._get_fallback_move(self._last_error)

    def _get_fallback_move(self, reason: str) -> Move:
        """Return cooperative move as fallback with explanation"""
        self._record_interaction(
            self.current_round,
            AIResponse(
                move=Move.COOPERATE,
                reasoning=f"Fallback cooperation due to: {reason}",
                token_usage=TokenUsage(0, 0, 0)
            )
        )
        return Move.COOPERATE

    def _update_token_usage(self, usage: TokenUsage):
        """Track token usage"""
        self.total_tokens_used += usage.total_tokens

    def _record_interaction(self, round_number: int, response: AIResponse):
        """Record the interaction in conversation history"""
        self.conversation_history.append({
            "round": round_number,
            "move": response.move.value,
            "reasoning": response.reasoning,
            "token_usage": asdict(response.token_usage)
        })

    def _estimate_token_usage(self, text: str) -> int:
        """Rough estimate of token count for a text string"""
        # Very rough approximation: ~1 token per 4 chars
        return len(text) // 4 + 100  # Add padding for safety

    async def _get_ai_response(self, current_round: int) -> AIResponse:
        """
        Get response from AI model. Must be implemented by child classes.
        """
        raise NotImplementedError("AI strategy must implement _get_ai_response")

    def reset(self):
        """Reset the strategy's state"""
        super().reset()
        self.total_tokens_used = 0
        self.conversation_history = []
        self._last_error = None

    @property
    def last_error(self) -> Optional[str]:
        """Get the last error that occurred"""
        return self._last_error