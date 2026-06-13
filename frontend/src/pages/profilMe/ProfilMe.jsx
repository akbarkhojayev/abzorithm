import React, { useEffect, useRef, useState } from "react";
import "./ProfilMe.css";
import { getProfilMe } from "../services/app.js";
import { GrCircleInformation } from "react-icons/gr";
import { AiOutlineEdit } from "react-icons/ai";
import Button from "@mui/material/Button";
import { baseUrl } from "../services/config.js";
import { getToken } from "../services/token.js";
import { FiCamera } from "react-icons/fi";
import { useTheme } from "../../context/ThemeContext";
import { FaChartBar, FaCheckCircle, FaFire, FaList } from "react-icons/fa";

function ProfilMe({ profil, setProfil, setProfilMe }) {
  const { isDark } = useTheme();
  const [editInformation, setEditInformation] = useState(false);
  const [activeTab, setActiveTab] = useState("info");
  const [bio, setBio] = useState("");
  const [avatarPreview, setAvatarPreview] = useState("");
  const [submissions, setSubmissions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [statsLoading, setStatsLoading] = useState(false);
  const fileInput = useRef();

  useEffect(() => {
    if (!getToken()) return;
    getProfilMe()?.then((data) => {
      setProfil(data);
      setBio(data?.bio || "");
      setAvatarPreview(data?.avatar || "/imgs/icons.png");
    });
  }, [setProfil]);

  useEffect(() => {
    if (activeTab === "statistics" || activeTab === "history") {
      fetchSubmissions();
    }
  }, [activeTab]);

  const fetchSubmissions = async () => {
    setStatsLoading(true);
    try {
      const token = getToken();
      let allSubmissions = [];
      let offset = 0;
      const limit = 100;
      let hasMore = true;

      while (hasMore) {
        const res = await fetch(
          `${baseUrl}/submissions/?limit=${limit}&offset=${offset}`,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );

        if (!res.ok) break;

        const data = await res.json();
        const results = Array.isArray(data.results) ? data.results : [];

        if (results.length === 0) {
          hasMore = false;
        } else {
          allSubmissions = [...allSubmissions, ...results];
          offset += limit;
          if (offset >= data.count) {
            hasMore = false;
          }
        }
      }

      setSubmissions(allSubmissions);
    } catch (error) {
      console.error("Error fetching submissions:", error);
      setSubmissions([]);
    } finally {
      setStatsLoading(false);
    }
  };

  const editProfil = () => {
    const myHeaders = new Headers();
    getToken() ? myHeaders.append("Authorization", `Bearer ${getToken()}`) : "";
    const formdata = new FormData();
    formdata.append("bio", bio);
    if (fileInput.current?.files[0]) {
      formdata.append("avatar", fileInput.current.files[0]);
    }

    const requestOptions = {
      method: "PUT",
      headers: myHeaders,
      body: formdata,
      redirect: "follow",
    };

    fetch(`${baseUrl}/users/me/update/`, requestOptions)
      .then((response) => response.json())
      .then((result) => {
        console.log(result);
        getProfilMe()?.then(setProfilMe);
        setEditInformation(false);
      })
      .catch((error) => console.error(error));
  };

  const handleAvatarChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setAvatarPreview(URL.createObjectURL(file));
    }
  };

  const calculateStats = () => {
    const total = submissions.length;
    const accepted = submissions.filter((s) => s.status === "Accepted").length;
    const wrong = submissions.filter((s) => s.status === "Wrong Answer").length;
    const runtime = submissions.filter(
      (s) => s.status === "Runtime Error"
    ).length;
    const tle = submissions.filter(
      (s) => s.status === "Time Limit Exceeded"
    ).length;

    return {
      total,
      accepted,
      wrong,
      runtime,
      tle,
      acceptanceRate: total > 0 ? Math.round((accepted / total) * 100) : 0,
    };
  };

  const getDifficultyStats = () => {
    const difficulties = { easy: 0, medium: 0, hard: 0 };
    submissions
      .filter((s) => s.status === "Accepted")
      .forEach((s) => {
        if (s.difficulty) {
          const difficultyKey = s.difficulty.toLowerCase();
          if (difficultyKey in difficulties) {
            difficulties[difficultyKey]++;
          }
        }
      });
    return difficulties;
  };

  const getLanguageStats = () => {
    const languages = {};
    submissions.forEach((s) => {
      if (s.language) {
        const lang = s.language.toLowerCase();
        languages[lang] = (languages[lang] || 0) + 1;
      }
    });
    return languages;
  };

  const stats_ = calculateStats();
  const difficultyStats = getDifficultyStats();
  const languageStats = getLanguageStats();

  return (
    <div className={`profil-me ${isDark ? "dark" : "light"}`}>
      <div className="avatar-lines">
        <div className="container">
          <div className="avatar-box">
            <img
              src={avatarPreview || "/imgs/icons.png"}
              alt="Avatar"
              className="avatar-img"
            />
            {editInformation && (
              <div
                className="avatar-edit-overlay"
                onClick={() => fileInput.current.click()}
              >
                <FiCamera className="camera-icon" />
                <span>Change photo</span>
              </div>
            )}

            <input
              type="file"
              accept="image/*"
              ref={fileInput}
              onChange={handleAvatarChange}
              style={{ display: "none" }}
            />
          </div>

          <div className="users-infos">
            <h2>{profil?.username}</h2>
            <p>Profil - {profil?.email}</p>
          </div>
        </div>
      </div>

      <div className="profil-information">
        <div className="container">
          <ul className="profile-tabs">
            <li
              className={activeTab === "info" ? "active" : ""}
              onClick={() => {
                setActiveTab("info");
                setEditInformation(false);
              }}
            >
              <GrCircleInformation />
              Ma'lumotlar
            </li>
            <li
              className={activeTab === "statistics" ? "active" : ""}
              onClick={() => setActiveTab("statistics")}
            >
              <FaChartBar />
              Statistika
            </li>
            <li
              className={activeTab === "history" ? "active" : ""}
              onClick={() => setActiveTab("history")}
            >
              <FaList />
              Yechimlar
            </li>
          </ul>

          <div className="profile-content">
            {/* Info Tab */}
            {activeTab === "info" && (
              <>
                <div className={`info-section ${editInformation ? "hidden" : ""}`}>
                  <div className="edit-header">
                    <h4>Ma'lumotlarim</h4>
                    <button
                      className="btn-edit-profile"
                      onClick={() => setEditInformation(true)}
                    >
                      <AiOutlineEdit /> Tahrirlash
                    </button>
                  </div>

                  <div className="edit-info-cards">
                    <div className="info-card-static">
                      <div className="card-label">Foydalanuvchi Nomi</div>
                      <div className="card-value-static">{profil?.username}</div>
                    </div>

                    <div className="info-card-static">
                      <div className="card-label">Elektron Pochta</div>
                      <div className="card-value-static">{profil?.email}</div>
                    </div>

                    <div className="info-card-static highlight-static">
                      <div className="card-label">Ball</div>
                      <div className="card-value-large-static">{profil?.score || 0}</div>
                    </div>
                  </div>

                  <div className="form-group">
                    <label>Biografiya</label>
                    <div className="bio-display">
                      {bio ? bio : <span className="bio-empty">Hali biografiya yo'q</span>}
                    </div>
                  </div>
                </div>

                {editInformation && (
                  <form
                    onSubmit={(e) => {
                      e.preventDefault();
                      editProfil();
                    }}
                    className="edit-section"
                  >
                    <div className="edit-header">
                      <h4>Ma'lumotlarni Tahrirlash</h4>
                      <p>Faqat biografiyangizni o'zgartirishingiz mumkin</p>
                    </div>

                    <div className="edit-info-cards">
                      <div className="info-card-static">
                        <div className="card-label">Foydalanuvchi Nomi</div>
                        <div className="card-value-static">{profil?.username}</div>
                      </div>

                      <div className="info-card-static">
                        <div className="card-label">Elektron Pochta</div>
                        <div className="card-value-static">{profil?.email}</div>
                      </div>
                    </div>

                    <div className="form-group">
                      <label>Biografiya</label>
                      <textarea
                        value={bio}
                        onChange={(e) => setBio(e.target.value)}
                        placeholder="O'zingiz haqida yozing... (maksimal 500 belgi)"
                        maxLength="500"
                      ></textarea>
                      <div className="char-count">{bio.length}/500</div>
                    </div>

                    <div className="form-buttons">
                      <button
                        type="button"
                        className="btn-cancel"
                        onClick={() => setEditInformation(false)}
                      >
                        Bekor qilish
                      </button>
                      <button type="submit" className="btn-save">
                        Saqlash
                      </button>
                    </div>
                  </form>
                )}
              </>
            )}

            {/* Statistics Tab */}
            {activeTab === "statistics" && (
              <div className="statistics-section">
                {statsLoading ? (
                  <div className="loading">Yuklanmoqda...</div>
                ) : submissions.length === 0 ? (
                  <div className="empty-state">
                    <FaChartBar />
                    <h3>Statistika yo'q</h3>
                    <p>Masalalarni yechib, statistikangizni to'ldiring</p>
                  </div>
                ) : (
                  <>
                    <div className="stats-grid">
                      <div className="stat-card">
                        <div className="stat-label">Jami Yechimlar</div>
                        <div className="stat-value">{stats_.total}</div>
                      </div>
                      <div className="stat-card accent">
                        <div className="stat-label">Qabul Qilingan</div>
                        <div className="stat-value">{stats_.accepted}</div>
                      </div>
                      <div className="stat-card">
                        <div className="stat-label">Xato Javoblar</div>
                        <div className="stat-value">{stats_.wrong}</div>
                      </div>
                      <div className="stat-card">
                        <div className="stat-label">Muvaffaqiyat %</div>
                        <div className="stat-value">{stats_.acceptanceRate}%</div>
                      </div>
                    </div>

                    <div className="charts-container">
                      <div className="chart-card">
                        <h5>Qiyinlik Bo'yicha</h5>
                        <div className="chart-bars">
                          <div className="bar-item">
                            <span className="bar-label">Easy</span>
                            <div className="bar-bg">
                              <div
                                className="bar-fill"
                                style={{
                                  width: `${
                                    difficultyStats.easy > 0
                                      ? (difficultyStats.easy /
                                          (difficultyStats.easy +
                                            difficultyStats.medium +
                                            difficultyStats.hard)) *
                                        100
                                      : 0
                                  }%`,
                                  background: "#58a6ff",
                                }}
                              ></div>
                            </div>
                            <span className="bar-value">{difficultyStats.easy}</span>
                          </div>
                          <div className="bar-item">
                            <span className="bar-label">Medium</span>
                            <div className="bar-bg">
                              <div
                                className="bar-fill"
                                style={{
                                  width: `${
                                    difficultyStats.medium > 0
                                      ? (difficultyStats.medium /
                                          (difficultyStats.easy +
                                            difficultyStats.medium +
                                            difficultyStats.hard)) *
                                        100
                                      : 0
                                  }%`,
                                  background: "#f59e0b",
                                }}
                              ></div>
                            </div>
                            <span className="bar-value">{difficultyStats.medium}</span>
                          </div>
                          <div className="bar-item">
                            <span className="bar-label">Hard</span>
                            <div className="bar-bg">
                              <div
                                className="bar-fill"
                                style={{
                                  width: `${
                                    difficultyStats.hard > 0
                                      ? (difficultyStats.hard /
                                          (difficultyStats.easy +
                                            difficultyStats.medium +
                                            difficultyStats.hard)) *
                                        100
                                      : 0
                                  }%`,
                                  background: "#ef4444",
                                }}
                              ></div>
                            </div>
                            <span className="bar-value">{difficultyStats.hard}</span>
                          </div>
                        </div>
                      </div>

                      <div className="chart-card">
                        <h5>Tillarga Ko'ra</h5>
                        <div className="language-list">
                          {Object.entries(languageStats).length > 0 ? (
                            Object.entries(languageStats).map(([lang, count]) => (
                              <div key={lang} className="lang-item">
                                <span className="lang-name">{lang.toUpperCase()}</span>
                                <span className="lang-count">{count} ta</span>
                              </div>
                            ))
                          ) : (
                            <p className="empty-text">Ma'lumot yo'q</p>
                          )}
                        </div>
                      </div>
                    </div>
                  </>
                )}
              </div>
            )}

            {/* History Tab */}
            {activeTab === "history" && (
              <div className="history-section">
                {statsLoading ? (
                  <div className="loading">Yuklanmoqda...</div>
                ) : submissions.length === 0 ? (
                  <div className="empty-state">
                    <FaList />
                    <h3>Yechimlar yo'q</h3>
                    <p>Masalalarni yechib, yechimlar tarixini to'ldiring</p>
                  </div>
                ) : (
                  <div className="history-table">
                    <div className="table-header">
                      <div className="col-problem">Masala</div>
                      <div className="col-status">Status</div>
                      <div className="col-difficulty">Qiyinlik</div>
                      <div className="col-time">Vaqt</div>
                    </div>
                    <div className="table-body">
                      {submissions.map((sub) => (
                        <div key={sub.id} className="table-row">
                          <div className="col-problem">
                            <div className="problem-title">
                              {sub.problem_title || `Masala #${sub.problem}`}
                            </div>
                            <div className="problem-lang">
                              {sub.language?.toUpperCase()}
                            </div>
                          </div>
                          <div className="col-status">
                            <span className={`status-badge status-${sub.status?.toLowerCase().replace(/\s+/g, "-")}`}>
                              {sub.status}
                            </span>
                          </div>
                          <div className="col-difficulty">
                            <span className={`difficulty-badge difficulty-${sub.difficulty?.toLowerCase()}`}>
                              {sub.difficulty}
                            </span>
                          </div>
                          <div className="col-time">
                            {new Date(sub.submitted_at).toLocaleDateString("uz-UZ")}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default ProfilMe;
