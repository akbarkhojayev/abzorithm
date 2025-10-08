import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import './ProfilePage.css';

function ProfilePage() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [activeTab, setActiveTab] = useState('profile');
  const [message, setMessage] = useState({ type: '', text: '' });
  
  const [profileData, setProfileData] = useState({
    username: '',
    email: '',
    bio: '',
    country: '',
    avatar: null
  });
  
  const [avatarPreview, setAvatarPreview] = useState(null);
  const [recentSubmissions, setRecentSubmissions] = useState([]);

  const [passwordData, setPasswordData] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  });

  useEffect(() => {
    loadUser();
  }, []);

  const loadUser = async () => {
    try {
      const userData = await api.getCurrentUser();
      setUser(userData);
      setProfileData({
        username: userData.username || '',
        email: userData.email || '',
        bio: userData.bio || '',
        country: userData.country || '',
        avatar: null
      });
      setAvatarPreview(userData.avatar);
      
      // Load recent submissions
      try {
        const submissions = await api.getUserSubmissions(userData.id);
        setRecentSubmissions(submissions.slice(0, 5));
      } catch (err) {
        console.error('Failed to load submissions:', err);
      }
    } catch (error) {
      console.error('Failed to load user:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAvatarChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setProfileData({...profileData, avatar: file});
      setAvatarPreview(URL.createObjectURL(file));
    }
  };

  const handleProfileUpdate = async (e) => {
    e.preventDefault();
    setSaving(true);
    setMessage({ type: '', text: '' });

    try {
      const formData = new FormData();
      formData.append('bio', profileData.bio);
      formData.append('country', profileData.country);
      if (profileData.avatar) {
        formData.append('avatar', profileData.avatar);
      }
      
      await api.client.patch('/users/me/update/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      setMessage({ type: 'success', text: 'Profile updated successfully!' });
      await loadUser();
    } catch (error) {
      setMessage({ type: 'error', text: error.response?.data?.detail || 'Failed to update profile' });
    } finally {
      setSaving(false);
    }
  };

  const handlePasswordChange = async (e) => {
    e.preventDefault();
    
    if (passwordData.newPassword !== passwordData.confirmPassword) {
      setMessage({ type: 'error', text: 'Passwords do not match!' });
      return;
    }

    if (passwordData.newPassword.length < 6) {
      setMessage({ type: 'error', text: 'Password must be at least 6 characters!' });
      return;
    }

    setSaving(true);
    setMessage({ type: '', text: '' });

    try {
      // Note: Backend needs password change endpoint
      await api.client.post('/users/change-password/', {
        old_password: passwordData.currentPassword,
        new_password: passwordData.newPassword
      });
      
      setMessage({ type: 'success', text: 'Password changed successfully!' });
      setPasswordData({ currentPassword: '', newPassword: '', confirmPassword: '' });
    } catch (error) {
      setMessage({ type: 'error', text: error.response?.data?.detail || 'Failed to change password' });
    } finally {
      setSaving(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="profile-page">
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
          <button className="nav-link" onClick={() => navigate('/leaderboard')}>
            <i className="fas fa-trophy"></i>
            <span>Leaderboard</span>
          </button>
          <button className="nav-link active">
            <i className="fas fa-user"></i>
            <span>Profile</span>
          </button>
        </div>
        <div className="nav-user">
          <button onClick={handleLogout} className="btn-logout-simple">
            <i className="fas fa-sign-out-alt"></i>
            <span>Logout</span>
          </button>
        </div>
      </nav>

      <div className="profile-main-container">
        <div className="profile-container">
        <div className="profile-sidebar">
          <div className="profile-card">
            <div className="profile-avatar">
              {user?.avatar ? (
                <img src={user.avatar} alt={user.username} />
              ) : (
                user?.username?.charAt(0).toUpperCase()
              )}
            </div>
            <h2 className="profile-name">{user?.username}</h2>
            <p className="profile-email">{user?.email}</p>
            
            <div className="profile-stats">
              <div className="stat-box">
                <div className="stat-icon">
                  <i className="fas fa-star"></i>
                </div>
                <div className="stat-info">
                  <div className="stat-value">{user?.score || 0}</div>
                  <div className="stat-label">Score</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="profile-content">
          <div className="profile-tabs">
            <button 
              className={`profile-tab ${activeTab === 'profile' ? 'active' : ''}`}
              onClick={() => setActiveTab('profile')}
            >
              <i className="fas fa-user"></i>
              <span>Profile Info</span>
            </button>
            <button 
              className={`profile-tab ${activeTab === 'password' ? 'active' : ''}`}
              onClick={() => setActiveTab('password')}
            >
              <i className="fas fa-lock"></i>
              <span>Change Password</span>
            </button>
          </div>

          {message.text && (
            <div className={`message ${message.type}`}>
              <i className={`fas fa-${message.type === 'success' ? 'check-circle' : 'exclamation-circle'}`}></i>
              <span>{message.text}</span>
            </div>
          )}

          {activeTab === 'profile' && (
            <form onSubmit={handleProfileUpdate} className="profile-form">
              <div className="form-section">
                <h3>Personal Information</h3>
                
                <div className="form-group avatar-upload">
                  <label>Profile Picture</label>
                  <div className="avatar-upload-container">
                    <div className="avatar-preview">
                      {avatarPreview ? (
                        <img src={avatarPreview} alt="Avatar preview" />
                      ) : (
                        <div className="avatar-placeholder">
                          {user?.username?.charAt(0).toUpperCase()}
                        </div>
                      )}
                    </div>
                    <div className="avatar-upload-actions">
                      <h4>Upload Your Photo</h4>
                      <p>Choose a photo that represents you</p>
                      <input
                        type="file"
                        id="avatar-input"
                        accept="image/*"
                        onChange={handleAvatarChange}
                        style={{ display: 'none' }}
                      />
                      <label htmlFor="avatar-input" className="btn-upload">
                        <i className="fas fa-camera"></i>
                        <span>Choose Photo</span>
                      </label>
                      <small>JPG, PNG or GIF (Max 5MB)</small>
                    </div>
                  </div>
                </div>
                
                <div className="form-group">
                  <label>Username</label>
                  <input
                    type="text"
                    value={profileData.username}
                    disabled
                    className="disabled"
                  />
                  <small>Username cannot be changed</small>
                </div>

                <div className="form-group">
                  <label>Email</label>
                  <input
                    type="email"
                    value={profileData.email}
                    disabled
                    className="disabled"
                  />
                  <small>Email cannot be changed</small>
                </div>

                <div className="form-group">
                  <label>Country</label>
                  <input
                    type="text"
                    value={profileData.country}
                    onChange={(e) => setProfileData({...profileData, country: e.target.value})}
                    placeholder="Enter your country"
                  />
                </div>

                <div className="form-group">
                  <label>Bio</label>
                  <textarea
                    value={profileData.bio}
                    onChange={(e) => setProfileData({...profileData, bio: e.target.value})}
                    placeholder="Tell us about yourself..."
                    rows="4"
                  />
                </div>
              </div>

              <button type="submit" className="btn-save" disabled={saving}>
                {saving ? (
                  <>
                    <i className="fas fa-spinner fa-spin"></i>
                    <span>Saving...</span>
                  </>
                ) : (
                  <>
                    <i className="fas fa-save"></i>
                    <span>Save Changes</span>
                  </>
                )}
              </button>
            </form>
          )}

          {activeTab === 'password' && (
            <form onSubmit={handlePasswordChange} className="profile-form">
              <div className="form-section">
                <h3>Change Password</h3>
                
                <div className="form-group">
                  <label>Current Password</label>
                  <input
                    type="password"
                    value={passwordData.currentPassword}
                    onChange={(e) => setPasswordData({...passwordData, currentPassword: e.target.value})}
                    required
                  />
                </div>

                <div className="form-group">
                  <label>New Password</label>
                  <input
                    type="password"
                    value={passwordData.newPassword}
                    onChange={(e) => setPasswordData({...passwordData, newPassword: e.target.value})}
                    required
                  />
                  <small>At least 6 characters</small>
                </div>

                <div className="form-group">
                  <label>Confirm New Password</label>
                  <input
                    type="password"
                    value={passwordData.confirmPassword}
                    onChange={(e) => setPasswordData({...passwordData, confirmPassword: e.target.value})}
                    required
                  />
                </div>
              </div>

              <button type="submit" className="btn-save" disabled={saving}>
                {saving ? (
                  <>
                    <i className="fas fa-spinner fa-spin"></i>
                    <span>Changing...</span>
                  </>
                ) : (
                  <>
                    <i className="fas fa-key"></i>
                    <span>Change Password</span>
                  </>
                )}
              </button>
            </form>
          )}
        </div>
        </div>

        {/* Recent Submissions Sidebar */}
        <aside className="activity-sidebar">
          <div className="activity-card">
            <h3>
              <i className="fas fa-history"></i>
              Recent Submissions
            </h3>
            
            {recentSubmissions.length === 0 ? (
              <div className="empty-activity">
                <i className="fas fa-inbox"></i>
                <p>No submissions yet</p>
                <button onClick={() => navigate('/problems')} className="btn-start">
                  <i className="fas fa-code"></i>
                  Start Solving
                </button>
              </div>
            ) : (
              <div className="activity-list">
                {recentSubmissions.map((submission) => (
                  <div key={submission.id} className="activity-item">
                    <div className="activity-icon">
                      <i className={`fas fa-${submission.status === 'Accepted' ? 'check-circle' : 'times-circle'}`}></i>
                    </div>
                    <div className="activity-info">
                      <div className="activity-title">{submission.problem_title || `Problem #${submission.problem}`}</div>
                      <div className="activity-meta">
                        <span className={`status-badge ${submission.status.toLowerCase().replace(' ', '-')}`}>
                          {submission.status}
                        </span>
                        <span className="activity-time">
                          {new Date(submission.submitted_at).toLocaleDateString()}
                        </span>
                      </div>
                      {submission.execution_time && (
                        <div className="activity-stats">
                          <i className="fas fa-bolt"></i>
                          {submission.execution_time.toFixed(2)}ms
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </aside>
      </div>
    </div>
  );
}

export default ProfilePage;
