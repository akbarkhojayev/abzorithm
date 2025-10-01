import React, { useState } from 'react';
import { api } from '../services/api';
import './LoginPage.css';

function LoginPage({ onLogin }) {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (isLogin) {
        await api.login(formData.username, formData.password);
        onLogin();
      } else {
        await api.register(formData);
        alert('Registration successful! Please login.');
        setIsLogin(true);
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Operation failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-left">
        <div className="hero">
          <h1><i className="fas fa-rocket"></i> Abzorithm</h1>
          <p className="hero-subtitle">Master Algorithms, Land Your Dream Job</p>
          <div className="features-list">
            <div className="feature-item">
              <i className="fas fa-bullseye feature-icon"></i>
              <span>500+ Curated Problems</span>
            </div>
            <div className="feature-item">
              <i className="fas fa-users feature-icon"></i>
              <span>10K+ Active Users</span>
            </div>
            <div className="feature-item">
              <i className="fas fa-bolt feature-icon"></i>
              <span>Real-time Code Execution</span>
            </div>
            <div className="feature-item">
              <i className="fas fa-trophy feature-icon"></i>
              <span>Global Leaderboard</span>
            </div>
          </div>
          <div className="stats">
            <div className="stat">
              <div className="stat-icon"><i className="fas fa-fire"></i></div>
              <div className="stat-number">500+</div>
              <div className="stat-label">Problems</div>
            </div>
            <div className="stat">
              <div className="stat-icon"><i className="fas fa-user-friends"></i></div>
              <div className="stat-number">10K+</div>
              <div className="stat-label">Users</div>
            </div>
            <div className="stat">
              <div className="stat-icon"><i className="fas fa-code"></i></div>
              <div className="stat-number">100K+</div>
              <div className="stat-label">Submissions</div>
            </div>
          </div>
        </div>
      </div>

      <div className="login-right">
        <div className="login-card">
          <div className="tabs">
            <button 
              className={isLogin ? 'active' : ''} 
              onClick={() => setIsLogin(true)}
            >
              Sign In
            </button>
            <button 
              className={!isLogin ? 'active' : ''} 
              onClick={() => setIsLogin(false)}
            >
              Sign Up
            </button>
          </div>

          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Username</label>
              <input
                type="text"
                value={formData.username}
                onChange={(e) => setFormData({...formData, username: e.target.value})}
                required
              />
            </div>

            {!isLogin && (
              <div className="form-group">
                <label>Email</label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({...formData, email: e.target.value})}
                  required
                />
              </div>
            )}

            <div className="form-group">
              <label>Password</label>
              <input
                type="password"
                value={formData.password}
                onChange={(e) => setFormData({...formData, password: e.target.value})}
                required
              />
            </div>

            {error && <div className="error">{error}</div>}

            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? 'Loading...' : (isLogin ? 'Sign In' : 'Sign Up')}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;
