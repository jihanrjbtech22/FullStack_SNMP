/**
 * API service for fetching engine data from the SNMP backend
 */

import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:5003/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`🔄 API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('❌ API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('❌ API Response Error:', error.response?.status, error.message);
    return Promise.reject(error);
  }
);

/**
 * Fetch data for all engines
 * @returns {Promise<Object>} All engines data
 */
export const fetchAllEngines = async () => {
  try {
    const response = await api.get('/engines');
    return response.data;
  } catch (error) {
    console.error('Error fetching all engines:', error);
    throw new Error(`Failed to fetch engines data: ${error.message}`);
  }
};

/**
 * Fetch data for a specific engine
 * @param {string} engineId - Engine ID (e.g., 'Engine-1')
 * @returns {Promise<Object>} Engine data
 */
export const fetchEngine = async (engineId) => {
  try {
    const response = await api.get(`/engines/${engineId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching engine ${engineId}:`, error);
    throw new Error(`Failed to fetch engine ${engineId}: ${error.message}`);
  }
};

/**
 * Fetch summary statistics for all engines
 * @returns {Promise<Object>} Summary data
 */
export const fetchSummary = async () => {
  try {
    const response = await api.get('/summary');
    return response.data;
  } catch (error) {
    console.error('Error fetching summary:', error);
    throw new Error(`Failed to fetch summary: ${error.message}`);
  }
};

/**
 * Check API health
 * @returns {Promise<Object>} Health status
 */
export const checkHealth = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    console.error('Error checking health:', error);
    throw new Error(`Health check failed: ${error.message}`);
  }
};

/**
 * Create a polling function that fetches data at regular intervals
 * @param {Function} callback - Function to call with new data
 * @param {number} interval - Polling interval in milliseconds (default: 2000)
 * @returns {Function} Function to stop polling
 */
export const startPolling = (callback, interval = 2000) => {
  let isPolling = false;
  let pollInterval = null;

  const poll = async () => {
    if (isPolling) {
      try {
        const data = await fetchAllEngines();
        callback(data);
      } catch (error) {
        console.error('Polling error:', error);
        callback({ success: false, error: error.message });
      }
    }
  };

  const start = () => {
    if (!isPolling) {
      isPolling = true;
      poll(); // Initial fetch
      pollInterval = setInterval(poll, interval);
      console.log(`🔄 Started polling every ${interval}ms`);
    }
  };

  const stop = () => {
    if (isPolling) {
      isPolling = false;
      if (pollInterval) {
        clearInterval(pollInterval);
        pollInterval = null;
      }
      console.log('🛑 Stopped polling');
    }
  };

  start();
  return stop;
};

export default api;
