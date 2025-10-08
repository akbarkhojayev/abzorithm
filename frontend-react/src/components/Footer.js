import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/Footer.css';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-section">
          <h3 className="footer-heading">Abzorithm</h3>
          <p className="footer-description">
            Algorithm va dasturlash masalalarini yechish uchun professional platforma
          </p>
          <div className="social-links">
            <a href="https://t.me/abzorithm" target="_blank" rel="noopener noreferrer" className="social-icon">
              <i className="fab fa-telegram"></i>
            </a>
            <a href="https://github.com/abzorithm" target="_blank" rel="noopener noreferrer" className="social-icon">
              <i className="fab fa-github"></i>
            </a>
            <a href="https://youtube.com/abzorithm" target="_blank" rel="noopener noreferrer" className="social-icon">
              <i className="fab fa-youtube"></i>
            </a>
          </div>
        </div>

        <div className="footer-section">
          <h4 className="footer-title">Sahifalar</h4>
          <ul className="footer-links">
            <li><Link to="/problems" className="footer-link">Masalalar</Link></li>
            <li><Link to="/leaderboard" className="footer-link">Reyting</Link></li>
            <li><Link to="/profile" className="footer-link">Profil</Link></li>
            <li><Link to="/about" className="footer-link">Loyiha haqida</Link></li>
          </ul>
        </div>

        <div className="footer-section">
          <h4 className="footer-title">Yordam</h4>
          <ul className="footer-links">
            <li><a href="/help" className="footer-link">Foydalanish qo'llanmasi</a></li>
            <li><a href="/contact" className="footer-link">Bog'lanish</a></li>
            <li><a href="/privacy" className="footer-link">Maxfiylik siyosati</a></li>
            <li><a href="/terms" className="footer-link">Foydalanish shartlari</a></li>
          </ul>
        </div>
      </div>

      <div className="footer-bottom">
        <div className="container">
          <p>&copy; {currentYear} Abzorithm. Barcha huquqlar himoyalangan.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
