import { NextApiRequest, NextApiResponse } from 'next';
import axios from 'axios';

// This is a simple proxy to avoid CORS issues when connecting to the backend API
const handler = async (req: NextApiRequest, res: NextApiResponse) => {
  const { url, method } = req.query;
  
  if (!url || typeof url !== 'string') {
    return res.status(400).json({ error: 'URL query parameter is required' });
  }
  
  const API_URL = process.env.API_URL || 'http://localhost:8000';
  const targetUrl = `${API_URL}${url}`;
  
  try {
    const response = await axios({
      method: (method as string) || req.method,
      url: targetUrl,
      data: req.method !== 'GET' ? req.body : undefined,
      params: req.method === 'GET' ? req.body : undefined,
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    return res.status(response.status).json(response.data);
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      return res.status(error.response.status).json(error.response.data);
    }
    
    return res.status(500).json({ error: 'Internal server error', details: (error as Error).message });
  }
};

export default handler;