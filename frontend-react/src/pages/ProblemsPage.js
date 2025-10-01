import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import LoadingSkeleton from '../components/LoadingSkeleton';
import EmptyState from '../components/EmptyState';
import './ProblemsPage.css';

function ProblemsPage() {
  const navigate = useNavigate();
  const [problems, setProblems] = useState([]);
  const [filter, setFilter] = useState('');
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [sortBy, setSortBy] = useState('title');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [problemsData, userData] = await Promise.all([
        api.getProblems(),
        api.getCurrentUser()
      ]);
      setProblems(problemsData);
      setUser(userData);
    } catch (error) {
      console.error('Failed to load data:', error);
    } finally {
      setLoading(false);
    }
  };

  // Filter, search and sort problems
  const filteredProblems = problems
    .filter(p => !filter || p.difficulty === filter)
    .filter(p => 
      !searchQuery || 
      p.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (p.tags && p.tags.toLowerCase().includes(searchQuery.toLowerCase()))
    )
    .sort((a, b) => {
      if (sortBy === 'title') return a.title.localeCompare(b.title);
      if (sortBy === 'difficulty') {
        const order = { 'Easy': 1, 'Medium': 2, 'Hard': 3 };
        return order[a.difficulty] - order[b.difficulty];
      }
      return 0;
    });

  const handleLogout = () => {
    localStorage.removeItem('token');
    window.location.href = '/login';
  };

  const handleClearFilters = () => {
    setSearchQuery('');
    setFilter('');
    setSortBy('title');
  };

  return (
    <div className="problems-page">
      <nav className="navbar">
        <div className="nav-brand">
          <i className="fas fa-code brand-icon"></i>
          <span className="brand-text">Abzorithm</span>
        </div>
        <div className="nav-menu">
          <button className="nav-link active">
            <i className="fas fa-list"></i>
            <span>Problems</span>
          </button>
          <button className="nav-link" onClick={() => navigate('/leaderboard')}>
            <i className="fas fa-trophy"></i>
            <span>Leaderboard</span>
          </button>
        </div>
        <div className="nav-user">
          <div className="user-score">
            <i className="fas fa-star"></i>
            <span className="score-value">{user?.score || 0}</span>
          </div>
          <button className="user-avatar" onClick={() => navigate('/profile')} title="Profile">
            {user?.username?.charAt(0).toUpperCase()}
          </button>
          <button onClick={handleLogout} className="btn-logout">
            <i className="fas fa-sign-out-alt"></i>
            <span>Logout</span>
          </button>
        </div>
      </nav>

      <div className="content">
        <div className="page-header">
          <div className="header-left">
            <h1><i className="fas fa-code"></i> Problems</h1>
            <p>Practice and improve your coding skills</p>
          </div>
          <div className="header-actions">
            <div className="search-box">
              <i className="fas fa-search"></i>
              <input 
                type="text" 
                placeholder="Search problems..." 
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
              {searchQuery && (
                <button className="clear-btn" onClick={() => setSearchQuery('')}>
                  <i className="fas fa-times"></i>
                </button>
              )}
            </div>
            <select value={sortBy} onChange={(e) => setSortBy(e.target.value)} className="filter">
              <option value="title">Sort by Title</option>
              <option value="difficulty">Sort by Difficulty</option>
            </select>
            <select value={filter} onChange={(e) => setFilter(e.target.value)} className="filter">
              <option value="">All Difficulties</option>
              <option value="Easy">Easy</option>
              <option value="Medium">Medium</option>
              <option value="Hard">Hard</option>
            </select>
          </div>
        </div>

        {loading ? (
          <LoadingSkeleton count={6} />
        ) : filteredProblems.length === 0 ? (
          <EmptyState
            icon={searchQuery || filter ? 'fa-search' : 'fa-inbox'}
            title={searchQuery || filter ? 'No problems found' : 'No problems available'}
            message={
              searchQuery || filter
                ? 'Try adjusting your search or filter criteria.'
                : 'There are no problems available at the moment.'
            }
            action={searchQuery || filter ? handleClearFilters : null}
            actionLabel={searchQuery || filter ? 'Clear Filters' : null}
          />
        ) : (
          <div className="problems-grid">
            {filteredProblems.map((problem, index) => (
            <div 
              key={problem.id} 
              className="problem-card"
              onClick={() => navigate(`/problem/${problem.id}`)}
            >
              <div className="card-header">
                <div className="problem-number">#{index + 1}</div>
                <span className={`difficulty-badge ${problem.difficulty}`}>
                  {problem.difficulty}
                </span>
              </div>
              
              <h3 className="problem-title">{problem.title}</h3>
              
              <p className="problem-description">
                {problem.description?.substring(0, 100)}...
              </p>
              
              {problem.tags && (
                <div className="problem-tags">
                  {problem.tags.split(',').slice(0, 3).map((tag, i) => (
                    <span key={i} className="tag">
                      <i className="fas fa-tag"></i>
                      {tag.trim()}
                    </span>
                  ))}
                </div>
              )}
              
              <div className="card-footer">
                <div className="problem-stats">
                  <span className="stat-item">
                    <i className="fas fa-check-circle"></i>
                    <span>0 solved</span>
                  </span>
                  <span className="stat-item">
                    <i className="fas fa-code"></i>
                    <span>Python</span>
                  </span>
                </div>
                <button className="solve-btn">
                  <span>Solve</span>
                  <i className="fas fa-arrow-right"></i>
                </button>
              </div>
            </div>
          ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default ProblemsPage;
