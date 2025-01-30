// src/App.test.jsx
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from './App';
import { createGame, getStrategies, getGameState } from './utils/api';


jest.mock('./utils/api');

// Silence console.error in tests
beforeAll(() => {
  jest.spyOn(console, 'error').mockImplementation(() => {});
});

afterAll(() => {
  console.error.mockRestore();
});

// At the top of App.test.js, add:
beforeEach(() => {
  jest.clearAllMocks();
});

afterEach(() => {
  jest.clearAllTimers();
});

describe('App', () => {
  const mockStrategies = [
    { id: 'tit_for_tat', name: 'Tit for Tat' },
    { id: 'always_cooperate', name: 'Always Cooperate' }
  ];

  // Update the mockGameResponse in App.test.js
  const mockGameResponse = {
    game_id: 'test-123',
    status: 'created',
    current_round: 0,
    max_rounds: 5,
    scores: {
      player1: 0,
      player2: 0
    }
  };

  beforeEach(() => {
    jest.clearAllMocks();
    getStrategies.mockResolvedValue(mockStrategies);
    createGame.mockResolvedValue(mockGameResponse);
    getGameState.mockResolvedValue({
      game_id: 'test-123',
      current_round: 0,
      max_rounds: 5,
      is_game_over: false,
      scores: { player1: 0, player2: 0 }
    });
  });

  test('renders title', async () => {
    await act(async () => {
      render(<App />);
    });
    expect(screen.getByText("Prisoner's Dilemma Simulator")).toBeInTheDocument();
  });

  test('starts game when form submitted', async () => {
    await act(async () => {
      render(<App />);
    });
    
    await waitFor(() => {
      const player1Select = screen.getByLabelText('Player 1 Strategy');
      const player2Select = screen.getByLabelText('Player 2 Strategy');
      expect(player1Select).toBeInTheDocument();
      expect(player2Select).toBeInTheDocument();
    });
  
    await act(async () => {
      const player1Select = screen.getByLabelText('Player 1 Strategy');
      const player2Select = screen.getByLabelText('Player 2 Strategy');
      fireEvent.change(player1Select, { target: { value: 'tit_for_tat' } });
      fireEvent.change(player2Select, { target: { value: 'always_cooperate' } });
    });
  
    await act(async () => {
      const startButton = screen.getByText('Run Game');
      fireEvent.click(startButton);
    });
  
    await waitFor(() => {
      // Look for actual elements that appear in GameBoard
      expect(screen.getByRole('heading', { name: 'Game in Progress' })).toBeInTheDocument();
      expect(screen.getByText((content, element) => {
        return element.classList.contains('score-value') && 
               element.parentElement.querySelector('.score-label').textContent === 'Round' &&
               content.includes('0');
      })).toBeInTheDocument();      expect(screen.getByText('Auto-Complete Game')).toBeInTheDocument();
    });
  });
  
  test('shows error message when game creation fails', async () => {
    createGame.mockRejectedValue({ 
      response: { 
        data: { error: 'Failed to create game' }
      }
    });

    await act(async () => {
      render(<App />);
    });
    
    await waitFor(() => {
      const player1Select = screen.getByLabelText('Player 1 Strategy');
      const player2Select = screen.getByLabelText('Player 2 Strategy');
      expect(player1Select).toBeInTheDocument();
      expect(player2Select).toBeInTheDocument();
    });

    await act(async () => {
      const player1Select = screen.getByLabelText('Player 1 Strategy');
      fireEvent.change(player1Select, { target: { value: 'tit_for_tat' } });
      const player2Select = screen.getByLabelText('Player 2 Strategy');
      fireEvent.change(player2Select, { target: { value: 'always_cooperate' } });
    });
    
    await act(async () => {
      const startButton = screen.getByText('Run Game');
      fireEvent.click(startButton);
    });

    await waitFor(() => {
      expect(screen.getByText('Failed to create game')).toBeInTheDocument();
    });
  });
  // Add these tests to the existing App.test.js describe block

  test('renders GameBoard when game is started', async () => {
    await act(async () => {
      render(<App />);
    });

    // Set up and start game
    await act(async () => {
      const player1Select = screen.getByLabelText('Player 1 Strategy');
      const player2Select = screen.getByLabelText('Player 2 Strategy');
      fireEvent.change(player1Select, { target: { value: 'tit_for_tat' } });
      fireEvent.change(player2Select, { target: { value: 'always_cooperate' } });
      fireEvent.click(screen.getByText('Run Game'));
    });

    await waitFor(() => {
      expect(screen.getByText((content, element) => {
        return element.classList.contains('score-value') && 
               element.parentElement.querySelector('.score-label').textContent === 'Round' &&
               content.includes('0');
      })).toBeInTheDocument();
      expect(screen.getByText((content, element) => {
        return element.classList.contains('score-value') && content === '0' &&
               element.parentElement.querySelector('.score-label').textContent === 'Player 1';
      })).toBeInTheDocument();
      expect(screen.getByText((content, element) => {
        return element.classList.contains('score-value') && content === '0' &&
               element.parentElement.querySelector('.score-label').textContent === 'Player 2';
      })).toBeInTheDocument();    
    });
  });

  test('handles game completion', async () => {
    const completedGameState = {
      rounds: [
        {
          round_number: 1,
          player1_move: 'cooperate',
          player2_move: 'cooperate',
          player1_score: 3,
          player2_score: 3
        }
      ],
      final_scores: {
        player1: 3,
        player2: 3
      },
      is_game_over: true,
      scores: {
        player1: 3,
        player2: 3
      }
    };
    
    getGameState.mockResolvedValue({
      ...mockGameResponse,
      ...completedGameState
    });
  
    await act(async () => {
      render(<App />);
    });
  
    // Start game
    await act(async () => {
      const player1Select = screen.getByLabelText('Player 1 Strategy');
      const player2Select = screen.getByLabelText('Player 2 Strategy');
      fireEvent.change(player1Select, { target: { value: 'tit_for_tat' } });
      fireEvent.change(player2Select, { target: { value: 'always_cooperate' } });
      fireEvent.click(screen.getByText('Run Game'));
    });
  
    await waitFor(() => {
      expect(screen.getByText(/Auto-Complete Game/)).toBeInTheDocument();
    });
  });
});