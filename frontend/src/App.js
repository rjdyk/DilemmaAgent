// src/App.js
import React, { useState } from 'react';
import GameSetup from './components/GameSetup';
import GameBoard from './components/GameBoard';
import { createGame, getGameState } from './utils/api';

function App() {
  const [gameId, setGameId] = useState(null);
  const [gameState, setGameState] = useState(null);
  const [error, setError] = useState(null);

  const handleStartGame = async (params) => {
    try {
      setError(null);
      const response = await createGame(params);
      setGameId(response.game_id);
      setGameState(response);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to start game');
    }
  };

  const handleGameComplete = (result) => {
    setGameState({
      ...gameState,
      ...result,
      is_game_over: true
    });
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
        <GameBoard 
          gameId={gameId}
          gameState={gameState}
          onGameComplete={handleGameComplete}
        />
      )}
    </div>
  );
}

export default App;