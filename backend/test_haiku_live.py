import asyncio
import logging
import os
from dotenv import load_dotenv
import json

from app.strategies import create_strategy, StrategyType
from app.models.game import Game

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def run_test_game():
    try:
        logger.info("Starting live Haiku strategy test")
        
        # Create strategies
        haiku_strategy = create_strategy(StrategyType.CLAUDE_HAIKU, is_player1=True)
        always_coop = create_strategy(StrategyType.ALWAYS_COOPERATE, is_player1=False)
        
        logger.info("Created strategies successfully")
        logger.info(f"Initial Haiku token count: {haiku_strategy.total_tokens_used}")
        
        # Create game
        game = Game(haiku_strategy, always_coop, max_rounds=3)
        logger.info("Created game instance")
        
        # Run rounds
        for round_num in range(3):
            logger.info(f"\nProcessing round {round_num + 1}")
            logger.info(f"Tokens used before round: {haiku_strategy.total_tokens_used}")
            
            # Log the full AI response before processing the round
            ai_response = await haiku_strategy._get_ai_response(round_num)
            logger.info("Full AI Response:")
            logger.info(f"Move: {ai_response.move}")
            logger.info(f"Reasoning: {ai_response.reasoning}")
            logger.info(f"Token Usage: {ai_response.token_usage}")
            
            # Process round
            result = await game.process_round()
            
            # Log round results
            logger.info(f"Round {round_num + 1} results:")
            logger.info(f"Haiku move: {result.player1_move}")
            logger.info(f"Haiku reasoning (from game): {result.player1_reasoning}")
            logger.info(f"Always Cooperate move: {result.player2_move}")
            logger.info(f"Scores - Haiku: {result.player1_score}, Always Cooperate: {result.player2_score}")
            logger.info(f"Tokens used after round: {haiku_strategy.total_tokens_used}")

            # Log the AI's conversation history
            logger.info("\nAI Conversation History:")
            for entry in haiku_strategy.conversation_history:
                logger.info(json.dumps(entry, indent=2))
            
            if hasattr(game, 'ai_errors') and game.ai_errors:
                logger.warning(f"AI errors detected: {game.ai_errors}")
        
        # Log final results
        logger.info("\nGame complete!")
        logger.info(f"Final scores - Haiku: {game.player1_total_score}, Always Cooperate: {game.player2_total_score}")
        logger.info(f"Total tokens used: {haiku_strategy.total_tokens_used}")
        
    except Exception as e:
        logger.error(f"Error during test: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    load_dotenv()
    
    if not os.getenv('CLAUDE_API_KEY'):
        raise ValueError("CLAUDE_API_KEY not found in environment")
    
    asyncio.run(run_test_game())