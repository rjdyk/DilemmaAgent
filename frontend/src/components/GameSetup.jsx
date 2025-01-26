// src/components/GameSetup.jsx
import React, { useState, useEffect } from 'react';
import { getStrategies } from '../utils/api';
import './GameSetup.css';

const StrategySelect = ({ value, onChange, label, strategies }) => (
  <div className="input-group">
    <label htmlFor={`strategy-${label}`} className="input-label">
      {label}
    </label>
    <select 
      id={`strategy-${label}`}
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="select-input"
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
    onStartGame({player1Strategy, player2Strategy, rounds});
  };

  return (
    <div className="game-setup">
      <h2 className="setup-title">Game Setup</h2>
      
      {error && (
        <div className="error-message">
          {error}
        </div>
      )}
      
      <div className="input-group">
        <label className="input-label">Rounds</label>
        <input 
          type="number" 
          value={rounds}
          onChange={(e) => setRounds(parseInt(e.target.value, 10))}
          min="1"
          className="number-input"
        />
      </div>
      
      <StrategySelect 
        value={player1Strategy}
        onChange={setPlayer1Strategy}
        label="Player 1 Strategy"
        strategies={strategies}
      />
      
      <StrategySelect 
        value={player2Strategy}
        onChange={setPlayer2Strategy}
        label="Player 2 Strategy"
        strategies={strategies}
      />
      
      <button 
        onClick={handleSubmit}
        className="submit-button"
      >
        Run Game
      </button>
    </div>
  );
}

export default GameSetup;