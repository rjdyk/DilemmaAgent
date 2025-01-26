import axios from 'axios';

const BASE_URL = 'http://localhost:5001/api';

const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  },
  withCredentials: false,
  crossDomain: true
});

export const getStrategies = async () => {
  console.log('Fetching strategies from:', BASE_URL + '/strategies');
  try {
    const response = await api.get('/strategies');
    console.log('Response:', response);
    return response.data.strategies;
  } catch (error) {
    console.error('Error fetching strategies:', error.response || error);
    throw error;
  }
};

export const createGame = async (params) => {
  const { player1Strategy, player2Strategy, rounds } = params;
  const response = await api.post('/game/new', {
    player1Strategy,
    player2Strategy,
    rounds
  });
  return response.data;
};

export const getGameState = async (gameId) => {
  const response = await api.get(`/game/${gameId}/state`);
  return response.data;
};

export const makeMove = async (gameId, move, reasoning) => {
  const response = await api.post(`/game/${gameId}/move`, { move, reasoning });
  return response.data;
};

export const completeGame = async (gameId) => {
  console.log(`Completing game ${gameId}`)
  try {
    const response = await api.post(`/game/${gameId}/complete`);
    return response.data;
  } catch (error) {
    throw error.response?.data?.error || 'Failed to complete game';
  }
};

export const getGameHistory = async (gameId) => {
  const response = await api.get(`/game/${gameId}/history`);
  return response.data;
};