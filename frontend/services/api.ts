import axios from 'axios';

const API_URL = process.env.API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface QueryResponse {
  response: string;
  sources: Vulnerability[];
}

export interface Vulnerability {
  id: string;
  package: string;
  severity: string;
  description: string;
  published_date: string;
  affected_versions?: string;
  remediation?: string;
}

export const queryVulnerabilities = async (query: string): Promise<QueryResponse> => {
  try {
    const response = await api.post('/api/query', { query });
    return response.data;
  } catch (error) {
    console.error('Error querying vulnerabilities:', error);
    throw error;
  }
};

export const getVulnerabilities = async (params: {
  package?: string;
  severity?: string;
  limit?: number;
  offset?: number;
}): Promise<Vulnerability[]> => {
  try {
    const response = await api.get('/api/vulnerabilities', { params });
    return response.data;
  } catch (error) {
    console.error('Error fetching vulnerabilities:', error);
    throw error;
  }
};

export const getVulnerability = async (id: string): Promise<Vulnerability> => {
  try {
    const response = await api.get(`/api/vulnerabilities/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching vulnerability ${id}:`, error);
    throw error;
  }
};

export const getPackages = async (): Promise<string[]> => {
  try {
    const response = await api.get('/api/vulnerabilities/packages');
    return response.data;
  } catch (error) {
    console.error('Error fetching packages:', error);
    throw error;
  }
};

export const getSeverities = async (): Promise<string[]> => {
  try {
    const response = await api.get('/api/vulnerabilities/severities');
    return response.data;
  } catch (error) {
    console.error('Error fetching severities:', error);
    throw error;
  }
};

export const getStatistics = async (): Promise<any> => {
  try {
    const response = await api.get('/api/vulnerabilities/statistics');
    return response.data;
  } catch (error) {
    console.error('Error fetching statistics:', error);
    throw error;
  }
};

export default api;