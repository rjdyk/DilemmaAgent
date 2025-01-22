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

  test('calls onStartGame with selected strategy and rounds', async () => {
    const mockOnStartGame = jest.fn();
    
    await act(async () => {
      render(<GameSetup onStartGame={mockOnStartGame} />);
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
      // Click the start button
      const startButton = screen.getByText('Run Game');
      fireEvent.click(startButton);
    });

    expect(mockOnStartGame).toHaveBeenCalledWith('tit_for_tat', 5);
  });

  test('shows error when trying to start without selecting strategy', async () => {
    await act(async () => {
      render(<GameSetup onStartGame={() => {}} />);
    });

    await act(async () => {
      // Click start without selecting strategy
      const startButton = screen.getByText('Run Game');
      fireEvent.click(startButton);
    });

    expect(screen.getByText('Please select a strategy')).toBeInTheDocument();
  });
});