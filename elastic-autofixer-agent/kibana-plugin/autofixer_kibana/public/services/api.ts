import axios from 'axios';

// Base URL for our Kibana Server Routes
const API_BASE = '/api/autofixer';

export const AutoFixerAPI = {
  
  // 1. Get List of Problems
  diagnoseCluster: async () => {
    try {
      const response = await axios.get(`${API_BASE}/diagnose`);
      return response.data;
    } catch (e) {
      console.error("Diagnosis failed", e);
      return [];
    }
  },

  // 2. Ask AI to Generate a Fix
  generateFix: async (diagnostic: any) => {
    try {
      const response = await axios.post(`${API_BASE}/generate_fix`, diagnostic);
      return response.data;
    } catch (e) {
      console.error("Fix generation failed", e);
      return null;
    }
  },

  // 3. Apply the Fix
  applyFix: async (proposal: any) => {
    try {
      const response = await axios.post(`${API_BASE}/apply_fix`, proposal);
      return response.data;
    } catch (e) {
      console.error("Apply fix failed", e);
      return { status: "error", message: "Network Error" };
    }
  },

  // 4. Benchmark Performance
  benchmarkFix: async (proposal: any) => {
    try {
      const response = await axios.post(`${API_BASE}/benchmark`, proposal);
      return response.data;
    } catch (e) {
      console.error("Benchmark failed", e);
      return null;
    }
  }
};