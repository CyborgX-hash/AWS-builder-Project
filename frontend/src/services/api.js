import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const client = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  // Health
  checkHealth: async () => {
    const res = await client.get('/health');
    return res.data;
  },

  // Location Geocoding
  getCoordinates: async (location) => {
    const res = await client.get(`/weather/coordinates`, { params: { location } });
    return res.data;
  },

  // Weather
  getCurrentWeather: async (location, lat, lon) => {
    const res = await client.get(`/weather/current`, { params: { location, lat, lon } });
    return res.data;
  },

  getWeatherForecast: async (location, lat, lon) => {
    const res = await client.get(`/weather/forecast`, { params: { location, lat, lon } });
    return res.data;
  },

  // Crops
  getCrops: async () => {
    const res = await client.get('/crops');
    return res.data;
  },

  getCropDetails: async (cropName) => {
    const res = await client.get(`/crops/${cropName}`);
    return res.data;
  },

  // Risk
  getRiskReport: async (crop, growthStage, location, lat, lon) => {
    const res = await client.get('/risk/report', {
      params: { crop, growth_stage: growthStage, location, lat, lon }
    });
    return res.data;
  },

  // Advisory Generation
  generateAdvisory: async (data) => {
    const res = await client.post('/advisory/generate', data);
    return res.data;
  },

  // Multi-Agent Chat
  sendChat: async (payload) => {
    const res = await client.post('/chat', payload);
    return res.data;
  },

  // Farmer Profile
  saveFarmerProfile: async (profile) => {
    const res = await client.post('/farmer/profile', profile);
    return res.data;
  },

  getFarmerHistory: async (farmerId) => {
    const res = await client.get('/farmer/history', { params: { farmer_id: farmerId } });
    return res.data;
  }
};

export default api;

