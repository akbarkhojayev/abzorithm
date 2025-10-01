import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import './LeaderboardPage.css';

function LeaderboardPage() {
  const navigate = useNavigate();
  const [leaders, setLeaders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadLeaderboard();
  }, []);

  const loadLeaderboard = async () => {
    try {
      const data = await api.getLeaderboard();
      setLeaders(data);
    } catch (error) {
      console.error('Failed to load leaderboard:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Loading...</div>;

  return (
    <div className="leaderboard-page">
      <nav className="navbar">
        <div className="nav-brand">
          <i className="fas fa-code brand-icon"></i>
          <span className="brand-text">Abzorithm</span>
        </div>
        <div className="nav-menu">
          <button className="nav-link" onClick={() => navigate('/problems')}>
            <i className="fas fa-list"></i>
            <span>Problems</span>
          </button>
          <button className="nav-link active">
            <i className="fas fa-trophy"></i>
            <span>Leaderboard</span>
          </button>
          <button className="nav-link" onClick={() => navigate('/profile')}>
            <i className="fas fa-user"></i>
            <span>Profile</span>
          </button>
        </div>
        <div className="nav-user">
          <button onClick={() => {localStorage.removeItem('token'); navigate('/login');}} className="btn-logout">
            <i className="fas fa-sign-out-alt"></i>
            <span>Logout</span>
          </button>
        </div>
      </nav>

      <div className="content">
        <div className="page-header">
          <h1><i className="fas fa-trophy"></i> Leaderboard</h1>
          <p>Top performers this month</p>
        </div>

        <div className="leaderboard-list">
          {leaders.map((user, index) => {
            const rank = index + 1;
            const getMedalIcon = () => {
              if (rank === 1) return <i className="fas fa-medal gold-medal"></i>;
              if (rank === 2) return <i className="fas fa-medal silver-medal"></i>;
              if (rank === 3) return <i className="fas fa-medal bronze-medal"></i>;
              return rank;
            };
            
            return (
              <div key={user.id} className="leader-item">
                <div className="rank">{getMedalIcon()}</div>
                <div className="avatar">
                  {user.username?.charAt(0).toUpperCase()}
                </div>
                <div className="info">
                  <div className="name">{user.username}</div>
                  <div className="country">{user.country || 'Unknown'}</div>
                </div>
                <div className="score">{user.score || 0}</div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

export default LeaderboardPage;
