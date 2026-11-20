import axios from 'axios';

const api = axios.create({
  baseURL: '/api/v1', // Using Vite proxy
});

export default api;
