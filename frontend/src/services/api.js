import axios from 'axios';

// Use the local IP if running on a physical device, or localhost for web/simulators
const BASE_URL = 'http://localhost:8000/api/v1';

export const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const setAuthToken = (token) => {
  if (token) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  } else {
    delete api.defaults.headers.common['Authorization'];
  }
};
