// src/components/GameBoard.jsx
import React, { useState } from 'react';
import { completeGame, makeMove } from '../utils/api';
import './GameBoard.css';

function GameBoard({ gameId, gameState, onGameComplete }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const scores = gameState?.is_game_over ? 
    (gameState?.final_scores || gameState?.scores) : 
    (gameState?.scores || { player1: 0, player2: 0 });
  const currentRound = gameState?.current_round || 0;
  const maxRounds = gameState?.max_rounds || 0;
  const isGameOver = gameState?.is_game_over;
  const rounds = gameState?.rounds || [];

  const handleNextRound = async () => {
    try {
      setLoading(true);
      setError(null);
      const result = await makeMove(gameId);
      onGameComplete(result);
    } catch (err) {
      setError(err.message || 'Failed to process round');
    } finally {
      setLoading(false);
    }
  };

  const handleAutoComplete = async () => {
    try {
      setLoading(true);
      setError(null);
      const result = await completeGame(gameId);
      onGameComplete(result);
    } catch (err) {
      setError(err.message || 'Failed to complete game');
    } finally {
      setLoading(false);
    }
  };

  const getWinner = () => {
    if (!isGameOver) return null;
    if (scores.player1 > scores.player2) return 'Player 1 Wins!';
    if (scores.player2 > scores.player1) return 'Player 2 Wins!';
    return 'Game Tied!';
  };

  return (
    <div className="game-board">
      <div className={`status-panel ${isGameOver ? 'game-over' : ''}`}>
        <h2>{isGameOver ? 'Game Complete' : 'Game in Progress'}</h2>
        
        <div className="score-grid">
          <div className="score-box">
            <div className="score-label">Player 1</div>
            <div className="score-value">{scores.player1}</div>
          </div>
          
          <div className="score-box">
            <div className="score-label">Round</div>
            <div className="score-value">{currentRound} / {maxRounds}</div>
          </div>
          
          <div className="score-box">
            <div className="score-label">Player 2</div>
            <div className="score-value">{scores.player2}</div>
          </div>
        </div>
      </div>

      {rounds.length > 0 && (
        <table className="game-table">
          <thead>
            <tr>
              <th>Round</th>
              <th>Player 1</th>
              <th>Player 2</th>
              <th>P1 Score</th>
              <th>P2 Score</th>
            </tr>
          </thead>
          <tbody>
            {rounds.map((round) => (
              <tr key={round.round_number}>
                <td>{round.round_number}</td>
                <td className={`move-${round.player1_move}`}>
                  {round.player1_move}
                </td>
                <td className={`move-${round.player2_move}`}>
                  {round.player2_move}
                </td>
                <td>{round.player1_score}</td>
                <td>{round.player2_score}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {!isGameOver && (
        <div className="button-group">
          <button
            onClick={handleNextRound}
            disabled={loading}
            className="next-round-button"
          >
            {loading ? 'Processing...' : 'Next Round'}
          </button>
          
          <button
            onClick={handleAutoComplete}
            disabled={loading}
            className="complete-button"
          >
            {loading ? 'Completing...' : 'Auto-Complete Game'}
          </button>
        </div>
      )}

      {error && <div className="error-message">{error}</div>}
    </div>
  );
}

export default GameBoard;