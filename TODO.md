# TODO

# Phase 2
## 1. Strategy Implementation
- [x] Implement AlwaysDefect strategy
- [x] Implement TitForTat strategy
- [x] Implement Pavlov strategy
- [x] Implement Random strategy
- [x] Implement GrimTrigger strategy
- [x] Add tests for each strategy implementation
- [x] Update strategy registry with new implementations

## 2. Game Flow Control
### Backend
- [x] Add gameMode (AUTO/MANUAL) to Game class
- [x] Add runAllRounds() method for AUTO mode
- [ ] Add gameStatus field (ACTIVE/COMPLETE/ERROR)
- [ ] Add error message tracking
- [ ] Update game state validation
- [ ] Add tests for both game modes

### Frontend
#### GameSetup Component
- [x] Add strategy selection dropdowns
- [x] Add game mode toggle
- [x] Add start game validation
- [ ] Add loading states

#### GameBoard Component
- [x] Create round history table
- [x] Add current scores display
- [x] Add "Next Round" button for manual mode
- [x] Add "Auto-Complete" button
- [ ] Implement loading states
- [ ] Add error message display

#### Results Component
- [x] Display final scores
- [x] Show complete round history
- [x] Calculate and display statistics
  - [x] Cooperation rates
  - [x] Average scores
  - [x] Win/loss status
- [x] Add "New Game" button

## 3. Integration
### API Functions
- [ ] Implement getStrategies()
- [ ] Implement createGame()
- [ ] Implement getGameState()
- [ ] Implement makeMove()
- [ ] Implement completeGame()
- [ ] Add error handling

### State Management
- [ ] Add game state transitions
- [ ] Implement game state polling
- [ ] Add error state handling
- [ ] Add loading state management

## 4. Testing
- [ ] Unit tests for all strategies
- [ ] Integration tests for game flow
- [ ] API endpoint tests
- [ ] Frontend component tests
- [ ] End-to-end game flow tests

## 5. Documentation
- [ ] Add JSDoc comments to frontend components
- [ ] Update API documentation
- [ ] Add setup instructions
- [ ] Document testing procedures

## Future Tasks (Post-MVP)
- [ ] AI agent integration
- [ ] Retry logic for API failures
- [ ] Enhanced error handling
- [ ] Performance optimizations
- [ ] Advanced statistics

---
# Phase 1
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
