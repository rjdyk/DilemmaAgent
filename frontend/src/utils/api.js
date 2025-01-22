// src/utils/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000/api',
  headers: {
    'Content-Type': 'application/json'
  }
});

export const getStrategies = () => api.get('/strategies');
export const createGame = (strategy) => api.post('/game/new', { strategy });
export const getGameState = (gameId) => api.get(`/game/${gameId}/state`);
export const makeMove = (gameId, move, reasoning) => 
  api.post(`/game/${gameId}/move`, { move, reasoning });
export const getGameHistory = (gameId) => api.get(`/game/${gameId}/history`);