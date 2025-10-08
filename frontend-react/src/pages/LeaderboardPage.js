import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import './LeaderboardPage.css';

function LeaderboardPage() {
  const navigate = useNavigate();
  const [leaders, setLeaders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState(null);
  const [showProfileMenu, setShowProfileMenu] = useState(false);

  useEffect(() => {
    loadLeaderboard();
  }, []);

  const loadLeaderboard = async () => {
    try {
      const [leaderboardData, userData] = await Promise.all([
        api.getLeaderboard(),
        api.getCurrentUser()
      ]);
      setLeaders(leaderboardData);
      setUser(userData);
    } catch (error) {
      console.error('Failed to load leaderboard:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
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
          <div className="profile-dropdown">
            <button 
              className="user-avatar-btn" 
              onClick={() => setShowProfileMenu(!showProfileMenu)}
              title={user?.username}
            >
              <div className="user-avatar">
                {user?.avatar ? (
                  <img src={user.avatar} alt={user.username} />
                ) : (
                  user?.username?.charAt(0).toUpperCase()
                )}
              </div>
              <span className="user-name">{user?.username}</span>
              <i className={`fas fa-chevron-${showProfileMenu ? 'up' : 'down'}`}></i>
            </button>
            
            {showProfileMenu && (
              <div className="dropdown-menu">
                <button className="dropdown-item" onClick={() => { navigate('/profile'); setShowProfileMenu(false); }}>
                  <i className="fas fa-user"></i>
                  <span>My Profile</span>
                </button>
                <div className="dropdown-divider"></div>
                <button className="dropdown-item logout" onClick={handleLogout}>
                  <i className="fas fa-sign-out-alt"></i>
                  <span>Logout</span>
                </button>
              </div>
            )}
          </div>
        </div>
      </nav>

      <div className="content">
        <div className="page-header">
          <h1><i className="fas fa-trophy"></i> Leaderboard</h1>
          <p>Top performers this month</p>
        </div>

        <div className="leaderboard-container">
          <div className="leaderboard-header">
            <div className="header-rank">#</div>
            <div className="header-user">Foydalanuvchi</div>
            <div className="header-score">Ballar</div>
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
                  <div className="user-info">
                    <div className="avatar">
                      {user.username?.charAt(0).toUpperCase()}
                    </div>
                    <div className="info">
                      <div className="name">{user.username}</div>
                      <div className="country">{user.country || 'Noma\'lum'}</div>
                    </div>
                  </div>
                  <div className="score">{user.score || 0}</div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}

export default LeaderboardPage;
