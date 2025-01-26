// src/components/GameBoard.jsx
import React, { useState } from 'react';
import { completeGame, makeMove } from '../utils/api';
import './GameBoard.css';

function GameBoard({ gameId, gameState, onGameComplete, onNewGame }) {
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

  const calculateCooperationRate = (rounds, playerNum) => {
    if (!rounds.length) return "0%";
    const cooperateMoves = rounds.filter(
      round => (playerNum === 1 ? round.player1_move : round.player2_move) === "cooperate"
    ).length;
    return `${Math.round((cooperateMoves / rounds.length) * 100)}%`;
  };

  return (
    <div className="game-board">
      <div className={`status-panel ${isGameOver ? 'game-over' : ''}`}>
        <h2>{isGameOver ? 'Game Complete' : 'Game in Progress'}</h2>

        <div className="score-grid">
          <div className="score-box">
            <div className="score-label">Player 1</div>
            <div className="score-value">{scores.player1}</div>
            <div className="strategy-name">
              {gameState?.strategy_names?.player1 || 'Unknown Strategy'}
            </div>
          </div>

          <div className="score-box">
            <div className="score-label">Round</div>
            <div className="score-value">{currentRound} / {maxRounds}</div>
          </div>

          <div className="score-box">
            <div className="score-label">Player 2</div>
            <div className="score-value">{scores.player2}</div>
            <div className="strategy-name">
              {gameState?.strategy_names?.player2 || 'Unknown Strategy'}
            </div>
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
            {rounds.map((round, index) => {
              // Calculate cumulative scores up to this round
              const p1Cumulative = rounds
                .slice(0, index + 1)
                .reduce((sum, r) => sum + r.player1_score, 0);
              const p2Cumulative = rounds
                .slice(0, index + 1)
                .reduce((sum, r) => sum + r.player2_score, 0);

              return (
                <tr key={round.round_number}>
                  <td>{round.round_number}</td>
                  <td className={`move-${round.player1_move}`}>
                    {round.player1_move}
                  </td>
                  <td className={`move-${round.player2_move}`}>
                    {round.player2_move}
                  </td>
                  <td>
                    +{round.player1_score} ({p1Cumulative})
                  </td>
                  <td>
                    +{round.player2_score} ({p2Cumulative})
                  </td>
                </tr>
              );
            })}
            <tr className="totals-row">
              <td>Totals</td>
              <td>{calculateCooperationRate(rounds, 1)}</td>
              <td>{calculateCooperationRate(rounds, 2)}</td>
              <td>
                {rounds.reduce((sum, round) => sum + round.player1_score, 0)}
              </td>
              <td>
                {rounds.reduce((sum, round) => sum + round.player2_score, 0)}
              </td>
            </tr>
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
      {isGameOver && (
        <div className="button-group">
          <button
            onClick={onNewGame}  // Change from window.location.reload()
            className="new-game-button"
          >
            New Game
          </button>
        </div>
      )}



      {error && <div className="error-message">{error}</div>}
    </div>
  );
}

export default GameBoard;