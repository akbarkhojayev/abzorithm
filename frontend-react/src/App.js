import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import ProblemsPage from './pages/ProblemsPage';
import ProblemSolverPage from './pages/ProblemSolverPage';
import LeaderboardPage from './pages/LeaderboardPage';
import ProfilePage from './pages/ProfilePage';
import Footer from './components/Footer';
import { api } from './services/api';
import './styles/Footer.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        await api.getCurrentUser();
        setIsAuthenticated(true);
      } catch (error) {
        localStorage.removeItem('token');
        setIsAuthenticated(false);
      }
    }
    setLoading(false);
  };

  if (loading) {
    return (
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100vh' }}>
        <div>Loading...</div>
      </div>
    );
  }

  return (
    <Router>
      <Routes>
        <Route 
          path="/login" 
          element={!isAuthenticated ? <LoginPage onLogin={() => setIsAuthenticated(true)} /> : <Navigate to="/problems" />} 
        />
        <Route 
          path="/problems" 
          element={
            isAuthenticated ? (
              <div className="app-container">
                <main className="main-content">
                  <ProblemsPage />
                </main>
                <Footer />
              </div>
            ) : (
              <Navigate to="/login" />
            )
          } 
        />
        <Route 
          path="/problem/:slug" 
          element={isAuthenticated ? <ProblemSolverPage /> : <Navigate to="/login" />} 
        />
        <Route 
          path="/leaderboard" 
          element={isAuthenticated ? <LeaderboardPage /> : <Navigate to="/login" />} 
        />
        <Route 
          path="/profile" 
          element={isAuthenticated ? <ProfilePage /> : <Navigate to="/login" />} 
        />
        <Route path="/" element={<Navigate to="/problems" />} />
      </Routes>
    </Router>
  );
}

export default App;
