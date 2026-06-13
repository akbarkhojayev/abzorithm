import React, { useEffect, useRef, useState } from "react";
import "./Navbar.css";
import { FaCode, FaCoins, FaUserShield } from "react-icons/fa";
import { Link, NavLink, useNavigate } from "react-router-dom";
import { FaXmark } from "react-icons/fa6";
import { getProfilMe } from "../../pages/services/app.js";
import { IoExitOutline } from "react-icons/io5";
import { MdDarkMode, MdLightMode } from "react-icons/md";
import { useTheme } from "../../context/ThemeContext.jsx";

function Navbar({ tokens, setTokens, profilMe, setProfilMe }) {
  const navigate = useNavigate();
  const [showModal, setShowModal] = useState(false);
  const [dropdownPos, setDropdownPos] = useState({ top: 0, right: 0 });
  const { isDark, toggleTheme } = useTheme();

  useEffect(() => {
    if (tokens) {
      getProfilMe()?.then(setProfilMe);
    }
  }, [tokens, setProfilMe]);

  const panelRef = useRef(null);
  const buttonRef = useRef(null);

  const handleProfileClick = () => {
    if (buttonRef.current) {
      const rect = buttonRef.current.getBoundingClientRect();
      setDropdownPos({
        top: rect.bottom + 8,
        right: window.innerWidth - rect.right
      });
    }
    setShowModal(!showModal);
  };

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        panelRef.current &&
        !panelRef.current.contains(event.target) &&
        buttonRef.current &&
        !buttonRef.current.contains(event.target)
      ) {
        setShowModal(false);
      }
    };

    if (showModal) {
      document.addEventListener("click", handleClickOutside);
      return () => {
        document.removeEventListener("click", handleClickOutside);
      };
    }
  }, [showModal]);

  const handleLogout = () => {
    localStorage.clear();
    setTokens(null);
    setShowModal(false);
    navigate("/");
  };

  return (
    <div className={`navbar ${isDark ? "dark" : "light"}`}>
      <div className="container">
        {/* LOGO */}
        <Link to="/" className="logo">
          <p>
            <FaCode />
          </p>
          <h1>
            codial algo
            <span>Dasturlashni O'zlashtir</span>
          </h1>
        </Link>

        {/* NAVIGATION LINKS */}
        <ul className="links">
          <li>
            <NavLink to="/">Masalalar</NavLink>
          </li>
          <li>
            <NavLink to="/leaderboard">Reyting Taxtasi</NavLink>
          </li>
          {tokens && (
            <>
              <li>
                <NavLink to="/exams">Imtixonlar</NavLink>
              </li>
            </>
          )}
        </ul>

        {/* RIGHT SECTION */}
        <div className="icons">
          {/* THEME TOGGLE */}
          <button
            className="theme-toggle"
            onClick={toggleTheme}
            title={isDark ? "Yorug' rejim" : "Qorong'u rejim"}
            aria-label="Temani o'zgartirish"
          >
            {isDark ? <MdLightMode /> : <MdDarkMode />}
          </button>

          {/* AUTH BUTTONS */}
          {!tokens && (
            <>
              <button
                className="btnssubmitions"
                onClick={() => navigate("/create-account")}
              >
                Akkaunt Ochish
              </button>
              <button
                className="btnssubmitions"
                onClick={() => navigate("/signIn")}
              >
                Kirish
              </button>
            </>
          )}

          {/* COINS */}
          {tokens && (
            <div className="coins" title="Sizning Ballari">
              <span className="coins-count">
                {profilMe && !isNaN(profilMe?.score)
                  ? profilMe?.score * 10
                  : "0"}
              </span>
              <p className="coin_svg">
                <FaCoins />
              </p>
            </div>
          )}

          {/* USER PROFILE DROPDOWN */}
          {tokens && (
            <div className="profile-wrapper">
              <div
                className="userIcon"
                ref={buttonRef}
                onClick={handleProfileClick}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    handleProfileClick();
                  }
                }}
                title="Profil Menyu"
                role="button"
                tabIndex="0"
              >
                <img src={profilMe?.avatar || "/imgs/icons.png"} alt="User" />
              </div>

              {/* DROPDOWN MENU */}
              {showModal && (
                <div
                  ref={panelRef}
                  className="profile-dropdown"
                  style={{
                    top: `${dropdownPos.top}px`,
                    right: `${dropdownPos.right}px`
                  }}
                  onClick={(e) => e.stopPropagation()}
                >
                  <button
                    className="dropdown-close"
                    onClick={() => setShowModal(false)}
                    aria-label="Menyuni yopish"
                  >
                    <FaXmark />
                  </button>

                  {/* USER INFO */}
                  <div className="dropdown-user-info">
                    <div className="dropdown-user-avatar">
                      <img
                        src={profilMe?.avatar || "/imgs/icons.png"}
                        alt="User Avatar"
                      />
                    </div>
                    <h3>{profilMe?.username || "User"}</h3>
                  </div>

                  {/* MENU ITEMS */}
                  <Link
                    to="/profil"
                    className="dropdown-item"
                    onClick={() => setShowModal(false)}
                  >
                    <FaUserShield />
                    <span>Shaxsiy Ma'lumotlar</span>
                  </Link>

                  <button
                    className="dropdown-item logout-btn"
                    onClick={handleLogout}
                  >
                    <IoExitOutline />
                    <span>Chiqish</span>
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Navbar;
