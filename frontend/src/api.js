import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const answerQuestion = async (query, topK = 5) => {
  try {
    const response = await apiClient.post('/qa', {
      query,
      top_k: topK,
    });
    return response.data;
  } catch (error) {
    throw new Error(`Failed to answer question: ${error.message}`);
  }
};

export const indexPdf = async (filePath) => {
  try {
    const response = await apiClient.post('/index-pdf', {
      file_path: filePath,
    });
    return response.data;
  } catch (error) {
    throw new Error(`Failed to index PDF: ${error.message}`);
  }
};

export const getSystemInfo = async () => {
  try {
    const response = await apiClient.get('/info');
    return response.data;
  } catch (error) {
    throw new Error(`Failed to get system info: ${error.message}`);
  }
};
