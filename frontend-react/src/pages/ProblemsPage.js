import React, { useState, useEffect, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import LoadingSkeleton from '../components/LoadingSkeleton';
import EmptyState from '../components/EmptyState';
import './ProblemsPage.css';

function ProblemsPage() {
  const [problems, setProblems] = useState([]);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showProfileMenu, setShowProfileMenu] = useState(false);

  // Filters and search
  const [searchQuery, setSearchQuery] = useState('');
  const [difficultyFilter, setDifficultyFilter] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [sortBy, setSortBy] = useState('id');
  const [sortOrder, setSortOrder] = useState('asc');

  // Filter and sort problems
  const filteredAndSortedProblems = useMemo(() => {
    let filtered = problems.filter(problem => {
      const matchesSearch = problem.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                           (problem.tags && problem.tags.toLowerCase().includes(searchQuery.toLowerCase()));
      const matchesDifficulty = !difficultyFilter || problem.difficulty === difficultyFilter;
      const matchesStatus = !statusFilter ||
        (statusFilter === 'solved' && problem.is_solved) ||
        (statusFilter === 'unsolved' && !problem.is_solved);

      return matchesSearch && matchesDifficulty && matchesStatus;
    });

    // Sort problems
    filtered.sort((a, b) => {
      let aVal, bVal;

      switch (sortBy) {
        case 'title':
          aVal = a.title.toLowerCase();
          bVal = b.title.toLowerCase();
          break;
        case 'difficulty':
          const diffOrder = { 'Easy': 1, 'Medium': 2, 'Hard': 3 };
          aVal = diffOrder[a.difficulty] || 0;
          bVal = diffOrder[b.difficulty] || 0;
          break;
        case 'acceptance':
          aVal = a.acceptance_rate || 0;
          bVal = b.acceptance_rate || 0;
          break;
        default:
          aVal = a.id;
          bVal = b.id;
      }

      if (sortOrder === 'asc') {
        return aVal > bVal ? 1 : -1;
      } else {
        return aVal < bVal ? 1 : -1;
      }
    });

    return filtered;
  }, [problems, searchQuery, difficultyFilter, statusFilter, sortBy, sortOrder]);

  // Calculate tag statistics
  const tagStats = useMemo(() => {
    const stats = {};
    problems.forEach(problem => {
      if (problem.tags) {
        problem.tags.split(',').forEach(tag => {
          const trimmedTag = tag.trim();
          if (trimmedTag) {
            stats[trimmedTag] = (stats[trimmedTag] || 0) + 1;
          }
        });
      }
    });
    return Object.entries(stats).sort((a, b) => b[1] - a[1]);
  }, [problems]);

  useEffect(() => {
    loadProblems();
    loadUser();
  }, []);

  const loadProblems = async () => {
    try {
      const problemsData = await api.getProblems();
      setProblems(problemsData);
    } catch (error) {
      console.error('Failed to load problems:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadUser = async () => {
    try {
      const userData = await api.getCurrentUser();
      setUser(userData);
    } catch (error) {
      console.error('Failed to load user:', error);
    }
  };

  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    window.location.href = '/login';
  };

  const handleClearFilters = () => {
    setSearchQuery('');
    setDifficultyFilter('');
    setStatusFilter('');
    setSortBy('id');
    setSortOrder('asc');
  };

  return (
    <div className="problems-page">
      <nav className="navbar">
        <div className="nav-brand">
          <i className="fas fa-code brand-icon"></i>
          <span className="brand-text">Abzorithm</span>
        </div>
        <div className="nav-menu">
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
        <div className="main-content">
          <div className="search-section">
            <div className="search-header">
              <h1><i className="fas fa-code"></i> Problems</h1>
              <p>Found {filteredAndSortedProblems.length} problems</p>
            </div>
            <div className="search-input-container">
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
            </div>
          </div>

          <div className="filters-section">
            <div className="header-actions">
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="filter"
              >
                <option value="id">Sort by ID</option>
                <option value="title">Sort by Title</option>
                <option value="difficulty">Sort by Difficulty</option>
                <option value="acceptance">Sort by Acceptance</option>
              </select>

              <select
                value={difficultyFilter}
                onChange={(e) => setDifficultyFilter(e.target.value)}
                className="filter"
              >
                <option value="">All Difficulties</option>
                <option value="Easy">Easy</option>
                <option value="Medium">Medium</option>
                <option value="Hard">Hard</option>
              </select>

              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="filter"
              >
                <option value="">All Status</option>
                <option value="solved">Solved</option>
                <option value="unsolved">Unsolved</option>
                <option value="attempted">Attempted</option>
              </select>

              {(searchQuery || difficultyFilter || statusFilter) && (
                <button className="clear-filters-btn" onClick={handleClearFilters}>
                  <i className="fas fa-times"></i>
                  Clear Filters
                </button>
              )}
            </div>
          </div>

          {loading ? (
            <LoadingSkeleton count={6} />
          ) : filteredAndSortedProblems.length === 0 ? (
            <EmptyState
              icon={searchQuery || difficultyFilter || statusFilter ? 'fa-search' : 'fa-inbox'}
              title={searchQuery || difficultyFilter || statusFilter ? 'No problems found' : 'No problems available'}
              message={
                searchQuery || difficultyFilter || statusFilter
                  ? 'Try adjusting your search or filter criteria.'
                  : 'There are no problems available at the moment.'
              }
              action={searchQuery || difficultyFilter || statusFilter ? handleClearFilters : null}
              actionLabel={searchQuery || difficultyFilter || statusFilter ? 'Clear Filters' : null}
            />
          ) : (
            <div className="problems-container">
              <div className="table-header">
                <div className="header-title">Title</div>
                <div className="header-difficulty">Difficulty</div>
                <div className="header-solved">Status</div>
              </div>
              <div className="problems-list">
                {filteredAndSortedProblems.map((problem, index) => (
                  <div
                    key={problem.id}
                    className={`problem-item ${(index % 2 === 0) ? 'even-item' : 'odd-item'}`}
                    onClick={() => navigate(`/problem/${problem.slug}`)}
                  >
                    <div className="item-title">
                      <span className="problem-number">{index + 1}.</span>
                      {problem.title}
                    </div>
                    <div className="item-difficulty">
                      <span className={`difficulty-badge ${problem.difficulty}`}>
                        {problem.difficulty}
                      </span>
                    </div>
                    <div className="item-solved">
                      {problem.is_solved && (
                        <span className="solved-indicator" title="Solved">
                          <i className="fas fa-check-circle"></i>
                        </span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Tags Summary - Moved to right side */}
        {tagStats && tagStats.length > 0 && (
          <div className="tags-summary">
            <h3><i className="fas fa-tags"></i> Tags Overview</h3>
            <div className="tags-stats">
              {tagStats.map(([tag, count]) => (
                <div key={tag} className="tag-stat">
                  <span className="tag-name">{tag}</span>
                  <span className="tag-count">{count}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default ProblemsPage;
