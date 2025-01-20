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
 [] Import required dependencies and Game class
 [] Create Flask app instance
 [] Configure CORS settings for local development
 [] Set up basic error handlers
 [] Set up storage utilities for game state management
### Core API Endpoints
 [] POST /api/game/new - Create new game with specified opponent strategy
 [] POST /api/game/{game_id}/move - Submit AI move for current round
 [] GET /api/game/{game_id}/state - Get current game state
 [] GET /api/game/{game_id}/history - Get full game history
 [] GET /api/strategies - List available opponent strategies
### Storage System (MVP)
 [] Create JSON file-based storage for game states
 [] Implement functions to read/write game states
 [] Implement functions to archive completed games
 [] Add basic concurrency handling
### Error Handling
 [] Add 404 handler for invalid game IDs
 [] Add 400 handler for invalid moves/requests
 [] Add 500 handler for API/storage errors


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