// src/App.jsx
import React, { useState } from 'react';
import GameSetup from './components/GameSetup';
import { createGame, getGameState } from './utils/api';

function App() {
  const [gameId, setGameId] = useState(null);
  const [gameState, setGameState] = useState(null);
  const [error, setError] = useState(null);

  const handleStartGame = async (strategy, rounds) => {
    try {
      setError(null);
      const response = await createGame(strategy);
      setGameId(response.game_id);
      setGameState(response);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to start game');
    }
  };

  const checkGameState = async () => {
    if (!gameId) return;
    
    try {
      const response = await getGameState(gameId);
      setGameState(response);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to fetch game state');
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Prisoner's Dilemma Simulator</h1>
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}
      {!gameId ? (
        <GameSetup onStartGame={handleStartGame} />
      ) : (
        <div>
          <p>Game in progress - ID: {gameId}</p>
          <p>Current round: {gameState?.current_round} / {gameState?.max_rounds}</p>
        </div>
      )}
    </div>
  );
}

export default App;