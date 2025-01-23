// src/components/GameSetup.test.jsx
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import '@testing-library/jest-dom';
import GameSetup from './GameSetup';
import { getStrategies } from '../utils/api';

jest.mock('../utils/api', () => ({
  getStrategies: jest.fn()
}));

// Silence console.error in tests
beforeAll(() => {
  jest.spyOn(console, 'error').mockImplementation(() => {});
});

afterAll(() => {
  console.error.mockRestore();
});

describe('GameSetup', () => {
  const mockStrategies = [
    { id: 'tit_for_tat', name: 'Tit for Tat' },
    { id: 'always_cooperate', name: 'Always Cooperate' }
  ];

  beforeEach(() => {
    jest.clearAllMocks();
    getStrategies.mockResolvedValue(mockStrategies);
  });

  afterEach(() => {
    jest.clearAllTimers();
  });

  test('handles API error gracefully', async () => {
    getStrategies.mockRejectedValue(new Error('API Error'));
    
    await act(async () => {
      render(<GameSetup onStartGame={() => {}} />);
    });
    
    await waitFor(() => {
      expect(screen.getByText('Failed to load strategies')).toBeInTheDocument();
    });
  });

  test('calls onStartGame with both selected strategies and rounds', async () => {
    const mockOnStartGame = jest.fn();
    
    await act(async () => {
      render(<GameSetup onStartGame={mockOnStartGame} />);
    });

    await waitFor(() => {
      expect(screen.getAllByRole('combobox')).toHaveLength(2);
    });

    await act(async () => {
      const [player1Select, player2Select] = screen.getAllByRole('combobox');
      fireEvent.change(player1Select, { target: { value: 'tit_for_tat' } });
      fireEvent.change(player2Select, { target: { value: 'always_cooperate' } });
    });

    await act(async () => {
      const startButton = screen.getByText('Run Game');
      fireEvent.click(startButton);
    });

    expect(mockOnStartGame).toHaveBeenCalledWith('tit_for_tat', 'always_cooperate', 5);
  });

  test('shows error when trying to start without selecting both strategies', async () => {
    await act(async () => {
      render(<GameSetup onStartGame={() => {}} />);
    });

    await act(async () => {
      const startButton = screen.getByText('Run Game');
      fireEvent.click(startButton);
    });

    expect(screen.getByText('Please select strategies for both players')).toBeInTheDocument();
  });
});