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

describe('App', () => {
  const mockStrategies = [
    { id: 'tit_for_tat', name: 'Tit for Tat' },
    { id: 'always_cooperate', name: 'Always Cooperate' }
  ];

  const mockGameResponse = {
    game_id: 'test-123',
    status: 'created',
    current_round: 0,
    max_rounds: 5
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
      scores: { ai: 0, opponent: 0 }
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
      expect(screen.getByText('Tit for Tat')).toBeInTheDocument();
    });
    
    await act(async () => {
      // Select strategies for both players
      const [player1Select, player2Select] = screen.getAllByRole('combobox');
      fireEvent.change(player1Select, { target: { value: 'tit_for_tat' } });
      fireEvent.change(player2Select, { target: { value: 'always_cooperate' } });
    });

    await act(async () => {
      const startButton = screen.getByText('Run Game');
      fireEvent.click(startButton);
    });

    await waitFor(() => {
      expect(screen.getByText(/Game in progress/)).toBeInTheDocument();
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
      expect(screen.getByText('Tit for Tat')).toBeInTheDocument();
    });

    await act(async () => {
      // Select a strategy
      const strategySelect = screen.getByRole('combobox');
      fireEvent.change(strategySelect, { target: { value: 'tit_for_tat' } });
    });
    
    await act(async () => {
      const startButton = screen.getByText('Run Game');
      fireEvent.click(startButton);
    });

    await waitFor(() => {
      expect(screen.getByText('Failed to create game')).toBeInTheDocument();
    });
  });
});