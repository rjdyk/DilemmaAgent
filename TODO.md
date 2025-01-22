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
[x] Clean up create-react-app template
[x] Set up axios with base configuration
[x] Create basic app layout
[x] Add API service module
[~] Create GameBoard component skeleton (Started with GameSetup)
[x] Add basic state management (game status, moves)
[x] Create simple form for starting game
GameBoard Component:
[] Create move buttons (Cooperate/Defect)
[] Add round number and score display
[] Implement move history table/list
[] Handle move submission with AI reasoning
[] Add loading states during API calls
Analytics Section:
[] Create TotalScores component
[] Add CooperationRates component
[] Implement CooperationRatesOverTime chart
[] Set up data processing for analytics
[] Add refresh/update logic for live stats
Additional Features:
[] Add complete game history view
[] Create win rates grid for strategies
[] Implement round-by-round visualization
[] Add game completion handling
[] Set up error boundary for API failures

## Integration Testing:
[] Test health endpoint connection
[] Test game start flow
[] Test basic move submission
[] Verify game state updates
[] Test error handling