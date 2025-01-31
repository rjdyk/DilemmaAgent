# TODO

# Wednesday TODO - Reasoning Infrastructure

## Game Class Updates
- [x] Clean up games.py with reasoning
- [ ] Add separate reasoning storage in RoundResult
- [x] Update process_round() to handle structured reasoning
- [x] Add reasoning analysis utilities

## Frontend Updates
- [ ] Add reasoning display to GameBoard
- [ ] Create ReasoningHistory component
- [ ] Style reasoning display

## Storage Updates
- [ ] Update game_history.json structure
- [ ] Add reasoning to GameHistory class
- [ ] Add reasoning serialization/deserialization

## Testing
- [ ] Add tests for reasoning storage
- [ ] Test reasoning display
- [ ] Verify history storage works

# Thursday TODO - Experimental Infrastructure

## ExperimentRunner Development
- [ ] Create ExperimentRunner class
- [ ] Add batch game execution
- [ ] Implement experiment configuration
- [ ] Add results collection

## Payoff Matrix System
- [ ] Create PayoffMatrixBuilder
- [ ] Add preset matrices (mild/severe/asymmetric)
- [ ] Add matrix validation
- [ ] Update Game class to use new matrix system

## Analysis Tools
- [ ] Add cooperation rate calculation
- [ ] Add score analysis utilities
- [ ] Create basic statistical functions
- [ ] Add experiment result export

## Visualization
- [ ] Create ResultsVisualizer class
- [ ] Add cooperation rate charts
- [ ] Add score distribution charts
- [ ] Add matrix comparison views

# Friday TODO - Experiments & Analysis

## Morning - Run Experiments
- [ ] Run baseline matrix (100 games)
- [ ] Run mild penalty matrix (100 games)
- [ ] Run severe penalty matrix (100 games)
- [ ] Run asymmetric matrix (100 games)

## Results Processing
- [ ] Calculate cooperation rates
- [ ] Analyze score distributions
- [ ] Compare against optimal play
- [ ] Extract interesting reasoning patterns

## Analysis Documentation
- [ ] Document key findings
- [ ] Create final visualizations
- [ ] Identify surprising behaviors
- [ ] Find best examples for blog post

## Blog Preparation
- [ ] Create outline
- [ ] Select key screenshots
- [ ] Prepare data visualizations
- [ ] Draft key sections

# Saturday TODO - Blog Post

## Writing
- [ ] Introduction & motivation
- [ ] Experimental setup
- [ ] Results & analysis
- [ ] Implications for AI safety
- [ ] Future work

## Repository
- [ ] Clean up code
- [ ] Add documentation
- [ ] Include experiment configs
- [ ] Add result examples

## Final Tasks
- [ ] Proofread blog post
- [ ] Double-check visualizations
- [ ] Verify all links work
- [ ] Add references

# Phase 3
## Implementation Plan

### Phase 3.1: Core AI Infrastructure
[x] Create AIStrategy base class
[x] Implement token tracking
[x] Add basic error handling
[x] Update game logic

### Phase 3.2: Model Integration
[x] Implement HaikuStrategy
[x] Add prompt management
[x] Test API integration
[x] Add failure handling

### Phase 3.3: Enhanced Features
[ ] Add context management
[ ] Implement history truncation
[ ] Add detailed logging
[ ] Update game state tracking

## Future Work (Out of Scope for MVP3)

### Additional Models
- Support for GPT-4
- Open source model integration
- Model comparison tools
- Custom prompt engineering interface

### Enhanced Features
- Dynamic token budgeting
- Advanced context management
- Performance analytics
- Strategy effectiveness metrics
- Training data generation

### UI Improvements
- AI reasoning display
- Token usage visualization
- Error status indicators
- Context inspection tools

## Known Limitations
1. Fixed prompts only
2. Basic error handling
3. Limited context management
4. No dynamic token adjustment
5. Single AI agent per game
6. Basic fallback mechanisms


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
