import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

// Shared axios instance: add JSON Content-Type so individual requests don't need to set it.
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json'
  }
});

export default api;