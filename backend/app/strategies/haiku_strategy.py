from typing import Dict, List, Optional
import json
import anthropic
from app.strategies.ai_strategy import AIStrategy, AIResponse, TokenUsage
from app.models.types import Move

class HaikuStrategy(AIStrategy):
    def __init__(self, name: str, is_player1: bool, api_key: str):
        if not api_key:
            raise ValueError("API key cannot be empty")
        super().__init__(name, is_player1, token_budget=4000)
        self.client = anthropic.AsyncAnthropic(api_key=api_key)
        
        # Base system prompt explaining the game
        self.system_prompt = """You are playing an iterated prisoner's dilemma game. 
In each round, you must choose to either COOPERATE or DEFECT.

The payoffs for each round are:
- If both players cooperate: Both get 3 points
- If both players defect: Both get 1 point
- If one cooperates and one defects: The defector gets 5 points, the cooperator gets 0

Your goal is to maximize your total points across all rounds.
Always respond with a JSON object containing:
{
    "reasoning": "Your explanation for the move",
    "move": "COOPERATE" or "DEFECT"
}"""

    async def get_move(self, current_round: int) -> Move:
        # Check if next response would exceed budget (estimate 100 tokens for safety margin)
        if self.total_tokens_used + 100 > self.token_budget:
            raise ValueError("Token budget exceeded")
        
        # Call the parent class's get_move method
        return await super().get_move(current_round)

    async def _get_ai_response(self, current_round: int) -> AIResponse:
        """Get next move from Claude Haiku"""

        estimated_tokens = self._estimate_token_usage(self._format_history()) + 200
        if self.total_tokens_used + estimated_tokens > self.token_budget:
            raise ValueError("Token budget exceeded")
        
        # Build the game history context
        history_text = self._format_history()
        
        # Construct the full prompt
        user_prompt = f"""Current round: {current_round + 1}
Game history:
{history_text}

What is your next move? Remember to respond with a JSON object containing your move and reasoning."""

        try:
            response = await self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=150,
                system=self.system_prompt,
                messages=[{
                    "role": "user",
                    "content": user_prompt
                }]
            )
            
            # Parse the response
            content = response.content[0].text
            try:
                move_data = json.loads(content)
                move = Move(move_data["move"].lower())
                reasoning = move_data["reasoning"]
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                raise ValueError(f"Failed to parse AI response: {str(e)}")
                
            # Calculate token usage
            token_usage = TokenUsage(
                prompt_tokens=response.usage.input_tokens,
                completion_tokens=response.usage.output_tokens,
                total_tokens=response.usage.input_tokens + response.usage.output_tokens
            )           
            
            return AIResponse(
                move=move,
                reasoning=reasoning,
                token_usage=token_usage
            )
            
        except anthropic.APIError as e:
            raise ValueError(f"Anthropic API error: {str(e)}")

    def _format_history(self) -> str:
        """Format game history for the prompt"""
        if not self.history:
            return "No previous rounds played."
            
        history_lines = []
        for round_result in self.history:
            my_move = round_result.player1_move if self.is_player1 else round_result.player2_move
            opponent_move = round_result.player2_move if self.is_player1 else round_result.player1_move
            my_score = round_result.player1_score if self.is_player1 else round_result.player2_score
            opponent_score = round_result.player2_score if self.is_player1 else round_result.player1_score
            
            history_lines.append(
                f"Round {round_result.round_number}:\n"
                f"- You played: {my_move.value}\n"
                f"- Opponent played: {opponent_move.value}\n"
                f"- Scores: You: {my_score}, Opponent: {opponent_score}"
            )
            
        return "\n".join(history_lines)