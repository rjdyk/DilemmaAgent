// src/components/GameSetup.jsx
import React, { useState, useEffect } from 'react';
import { getStrategies } from '../utils/api';

function GameSetup({ onStartGame }) {
  const [strategies, setStrategies] = useState([]);
  const [player1Strategy, setPlayer1Strategy] = useState('');
  const [player2Strategy, setPlayer2Strategy] = useState('');
  const [rounds, setRounds] = useState(5);
  const [error, setError] = useState(null);

  useEffect(() => {
    let mounted = true;

    const fetchStrategies = async () => {
      try {
        const strategies = await getStrategies();
        if (mounted) {
          setStrategies(strategies);
        }
      } catch (err) {
        if (mounted) {
          setError('Failed to load strategies');
          if (process.env.NODE_ENV === 'development') {
            console.error('Error loading strategies:', err);
          }
        }
      }
    };

    fetchStrategies();

    return () => {
      mounted = false;
    };
  }, []);

  const handleSubmit = () => {
    if (!player1Strategy || !player2Strategy) {
      setError('Please select strategies for both players');
      return;
    }
    onStartGame(player1Strategy, player2Strategy, rounds);
  };

  const StrategySelect = ({ value, onChange, label }) => (
    <div className="mb-4">
      <label className="block mb-2">{label}</label>
      <select 
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="border p-2 w-full"
      >
        <option value="">Select a strategy</option>
        {strategies.map(strategy => (
          <option key={strategy.id} value={strategy.id}>
            {strategy.name}
          </option>
        ))}
      </select>
    </div>
  );

  return (
    <div className="mb-6">
      <h2 className="text-xl font-bold mb-4">Game Setup</h2>
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}
      <div className="mb-4">
        <label className="block mb-2">Rounds</label>
        <input 
          type="number" 
          value={rounds}
          onChange={(e) => setRounds(parseInt(e.target.value, 10))}
          min="1"
          className="border p-2"
        />
      </div>
      <StrategySelect 
        value={player1Strategy}
        onChange={setPlayer1Strategy}
        label="Player 1 Strategy"
      />
      <StrategySelect 
        value={player2Strategy}
        onChange={setPlayer2Strategy}
        label="Player 2 Strategy"
      />
      <button 
        onClick={handleSubmit}
        className="bg-black text-white px-4 py-2 w-full"
      >
        Run Game
      </button>
    </div>
  );
}

export default GameSetup;