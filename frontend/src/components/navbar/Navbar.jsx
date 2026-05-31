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
  const { isDark, toggleTheme } = useTheme();

  useEffect(() => {
    if (tokens) {
      getProfilMe()?.then(setProfilMe);
    }
  }, [tokens, setProfilMe]);

  const panelRef = useRef(null);
  const buttonRef = useRef(null);

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

    document.addEventListener("click", handleClickOutside);
    return () => {
      document.removeEventListener("click", handleClickOutside);
    };
  }, []);

  const handleLogout = () => {
    localStorage.clear();
    setTokens(null);
    setShowModal(false);
    navigate("/");
  };

  return (
    <div className="navbar">
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
            <>
              <div
                className="userIcon"
                ref={buttonRef}
                onClick={(e) => {
                  e.stopPropagation();
                  setShowModal(!showModal);
                }}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' || e.key === ' ') {
                    e.stopPropagation();
                    setShowModal(!showModal);
                  }
                }}
                title="Profil Menyu"
                role="button"
                tabIndex="0"
              >
                <img src={profilMe?.avatar || "/imgs/icons.png"} alt="User" />
              </div>

              {/* DROPDOWN MENU */}
              <div
                ref={panelRef}
                className={`modal ${showModal ? "active" : ""}`}
              >
                <button
                  className="xmark"
                  onClick={() => setShowModal(false)}
                  aria-label="Menyuni yopish"
                >
                  <FaXmark />
                </button>

                {/* USER INFO */}
                <div className="user-profil-status">
                  <div className="status-img">
                    <img
                      src={profilMe?.avatar || "/imgs/icons.png"}
                      alt="User Avatar"
                    />
                  </div>
                  <h2>{profilMe?.username || "User"}</h2>
                </div>

                {/* MENU ITEMS */}
                <Link
                  to="/profil"
                  className="list-profil"
                  onClick={() => setShowModal(false)}
                >
                  <FaUserShield />
                  Shaxsiy Ma'lumotlar
                </Link>

                <button
                  className="list-profil"
                  onClick={handleLogout}
                >
                  <IoExitOutline />
                  Chiqish
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default Navbar;
