// src/components/GameBoard.test.jsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import GameBoard from './GameBoard';
import { completeGame } from '../utils/api';

jest.mock('../utils/api');

describe('GameBoard', () => {
  const mockGameState = {
    current_round: 0,
    max_rounds: 5,
    is_game_over: false,
    scores: {
      player1: 0,
      player2: 0
    },
    rounds: []
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders game state correctly', () => {
    render(
      <GameBoard 
        gameId="test-123"
        gameState={mockGameState}
        onGameComplete={() => {}}
      />
    );

    expect(screen.getByRole('heading', { name: 'Game in Progress' })).toBeInTheDocument();

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
    expect(screen.getByText('Auto-Complete Game')).toBeInTheDocument();
  });

  test('handles auto-complete click', async () => {
    const mockComplete = jest.fn();
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
      }
    };

    completeGame.mockResolvedValue(completedGameState);

    render(
      <GameBoard 
        gameId="test-123"
        gameState={mockGameState}
        onGameComplete={mockComplete}
      />
    );

    fireEvent.click(screen.getByText('Auto-Complete Game'));

    await waitFor(() => {
      expect(completeGame).toHaveBeenCalledWith('test-123');
      expect(mockComplete).toHaveBeenCalledWith(completedGameState);
    });
  });

  test('displays error message on completion failure', async () => {
    completeGame.mockRejectedValue(new Error('Failed to complete game'));

    render(
      <GameBoard 
        gameId="test-123"
        gameState={mockGameState}
        onGameComplete={() => {}}
      />
    );

    fireEvent.click(screen.getByText('Auto-Complete Game'));

    await waitFor(() => {
      expect(screen.getByText('Failed to complete game')).toBeInTheDocument();
    });
  });

  test('displays round history', () => {
    const gameStateWithRounds = {
      ...mockGameState,
      rounds: [
        {
          round_number: 1,
          player1_move: 'cooperate',
          player2_move: 'cooperate',
          player1_score: 3,
          player2_score: 3
        }
      ]
    };
  
    render(
      <GameBoard 
        gameId="test-123"
        gameState={gameStateWithRounds}
        onGameComplete={() => {}}
      />
    );
  
    // Look for table headers
    expect(screen.getByRole('columnheader', { name: 'Player 1' })).toBeInTheDocument();
    expect(screen.getByRole('columnheader', { name: 'Player 2' })).toBeInTheDocument()
    
    // Use getAllByText for moves since there are multiple
    const cooperateMoves = screen.getAllByText('cooperate');
    expect(cooperateMoves).toHaveLength(2);
    
    // Check scores - be more specific by finding the cells
    const scoreElements = screen.getAllByText('3');
    expect(scoreElements).toHaveLength(2);
    
    // Verify round number
    expect(screen.getByText('1')).toBeInTheDocument();
  });
});