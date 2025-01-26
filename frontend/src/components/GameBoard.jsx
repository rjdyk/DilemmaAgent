// src/components/GameBoard.jsx
import React, { useState } from 'react';
import { completeGame } from '../utils/api';

function GameBoard({ gameId, gameState, onGameComplete }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const scores = gameState?.scores || { player1: 0, player2: 0 };
  const currentRound = gameState?.current_round || 0;
  const maxRounds = gameState?.max_rounds || 0;

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

  return (
    <div className="space-y-4">
      {/* Game Status Header */}
      <div className="bg-gray-100 p-4 rounded">
        <h2 className="text-xl font-bold">Game Progress</h2>
        <p>Round: {currentRound} / {maxRounds}</p>
        <div className="flex justify-between mt-2">
          <div>Player 1: {scores.player1} points</div>
          <div>Player 2: {scores.player2} points</div>
        </div>
      </div>

      {/* Round History Table */}
      <div className="overflow-x-auto">
        <table className="min-w-full border">
          <thead>
            <tr className="bg-gray-50">
              <th className="border p-2">Round</th>
              <th className="border p-2">Player 1 Move</th>
              <th className="border p-2">Player 2 Move</th>
              <th className="border p-2">P1 Score</th>
              <th className="border p-2">P2 Score</th>
            </tr>
          </thead>
          <tbody>
            {gameState.rounds?.map((round) => (
              <tr key={round.round_number}>
                <td className="border p-2">{round.round_number}</td>
                <td className="border p-2">{round.player1_move}</td>
                <td className="border p-2">{round.player2_move}</td>
                <td className="border p-2">{round.player1_score}</td>
                <td className="border p-2">{round.player2_score}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Controls */}
      <div className="flex justify-end space-x-4">
        <button
          onClick={handleAutoComplete}
          disabled={loading || gameState.is_game_over}
          className="bg-black text-white px-4 py-2 disabled:bg-gray-400"
        >
          {loading ? 'Completing...' : 'Auto-Complete Game'}
        </button>
      </div>

      {/* Error Display */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}
    </div>
  );
}

export default GameBoard;