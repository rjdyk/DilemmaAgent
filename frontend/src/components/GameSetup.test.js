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
  
    // Get the select elements
    const selects = screen.getAllByRole('combobox');
    expect(selects).toHaveLength(2);
    
    // Set player 1 strategy
    await act(async () => {
      fireEvent.change(selects[0], { 
        target: { value: 'tit_for_tat' }
      });
    });
  
    // Set player 2 strategy
    await act(async () => {
      console.log('Player 2 select props:', {
        onChange: selects[1].onChange,
        value: selects[1].value,
        options: selects[1].options
      });
      fireEvent.change(selects[1], { 
        target: { value: 'always_cooperate' }
      });
      console.log('After player 2 change event fired');
    });
  
    // Click the button
    await act(async () => {
      fireEvent.click(screen.getByText('Run Game'));
    });
  
    expect(mockOnStartGame).toHaveBeenCalledWith({
      player1Strategy: 'tit_for_tat',
      player2Strategy: 'always_cooperate', 
      rounds: 5
    });  });

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