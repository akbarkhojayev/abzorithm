import axios from 'axios';

const API_URL = 'http://13.61.149.80';

class API {
  constructor() {
    this.client = axios.create({
      baseURL: API_URL,
    });

    this.client.interceptors.request.use((config) => {
      const token = localStorage.getItem('token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });
  }

  // Auth
  async login(username, password) {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);
    
    const response = await axios.post(`${API_URL}/token/`, formData);
    localStorage.setItem('token', response.data.access);
    return response.data;
  }

  async register(data) {
    const response = await axios.post(`${API_URL}/users/register/`, data);
    return response.data;
  }

  async getCurrentUser() {
    const response = await this.client.get('/users/me/');
    return response.data;
  }

  // Problems
  async getProblems() {
    const response = await this.client.get('/problems/');
    return response.data;
  }

  async getProblem(slug) {
    const response = await this.client.get(`/problems/${slug}/`);
    return response.data;
  }

  async getTestCases(problemId) {
    const response = await this.client.get(`/testcases/?problem=${problemId}`);
    return response.data;
  }

  async submitCode(data) {
    try {
      // Get current user
      const currentUser = await this.getCurrentUser();
      
      // Backend expects: { problem: number, code: string, user: number }
      const payload = {
        problem: parseInt(data.problem),
        code: data.code,
        user: currentUser.id,
        language: 'python'  // Default language
      };
      
      console.log('Submitting code:', payload);
      const response = await this.client.post('/submissions/create/', payload);
      console.log('Submission response:', response.data);
      return response.data;
    } catch (error) {
      console.error('Submit error:', error.response?.data);
      throw error;
    }
  }

  async getTemplate(problemId) {
    const response = await this.client.get(`/submissions/template/${problemId}/`);
    return response.data;
  }

  // Leaderboard
  async getLeaderboard() {
    const response = await this.client.get('/leaderboard/');
    return response.data;
  }

  // User submissions
  async getUserSubmissions(userId) {
    const response = await this.client.get(`/submissions/?user=${userId}`);
    return response.data;
  }
}

export const api = new API();
