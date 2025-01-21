# TODO

## Backend Game Logic:
[x] Create Game class with:
    [x] Initialize game state (scores, round number, history)
    [x] Implement move validation
    [x] Add round processing logic
    [x] Add score calculation based on payoff matrix
    [x] Add game history tracking
    [x] Add game end conditions

## Basic Strategy Implementation:
[x] Create BaseStrategy class
[x] Implement one simple strategy (e.g., Always Cooperate) for testing
[x] Add strategy factory/registry

## Flask Setup:
### Basic Flask Configuration
 [x] Import required dependencies and Game class
 [x] Create Flask app instance
 [x] Configure CORS settings for local development
 [x] Set up basic error handlers
 [x] Set up storage utilities for game state management
### Core API Endpoints
 [x] POST /api/game/new - Create new game with specified opponent strategy
 [x] POST /api/game/{game_id}/move - Submit AI move for current round
 [x] GET /api/game/{game_id}/state - Get current game state
 [x] GET /api/game/{game_id}/history - Get full game history
 [x] GET /api/strategies - List available opponent strategies
### Storage System (MVP)
 [x] Create JSON file-based storage for game states
 [x] Implement functions to read/write game states
 [x] Implement functions to archive completed games
 [x] Add basic concurrency handling
### Error Handling
 [x] Add 404 handler for invalid game IDs
 [x] Add 400 handler for invalid moves/requests
 [x] Add 500 handler for API/storage errors


## React Setup:
[] Clean up create-react-app template
[] Set up axios with base configuration
[] Create basic app layout
[] Add API service module
[] Create GameBoard component skeleton
[] Add basic state management (game status, moves)
[] Create simple form for starting game
[] Add basic move display

## Integration Testing:
[] Test health endpoint connection
[] Test game start flow
[] Test basic move submission
[] Verify game state updates
[] Test error handling