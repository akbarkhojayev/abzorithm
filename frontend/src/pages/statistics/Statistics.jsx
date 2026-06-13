import React, { useEffect, useState } from "react";
import "./Statistics.css";
import { baseUrl } from "../services/config.js";
import { getToken } from "../services/token.js";
import { getProfilMe } from "../services/app.js";
import { FaChartBar, FaCheckCircle, FaFire, FaStar } from "react-icons/fa";
import { MdErrorOutline, MdAccessTime, MdPublic } from "react-icons/md";
import { useTheme } from "../../context/ThemeContext";

function Statistics() {
  const { isDark } = useTheme();
  const [stats, setStats] = useState(null);
  const [submissions, setSubmissions] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const token = getToken();

      // Fetch user profile
      const profilRes = await fetch(`${baseUrl}/users/me/`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (!profilRes.ok) {
        throw new Error("Failed to fetch profile");
      }

      const profil = await profilRes.json();
      setStats(profil);

      // Fetch all submissions with large limit
      // For statistics, we need all submissions to calculate accurate stats
      let allSubmissions = [];
      let offset = 0;
      const limit = 100;
      let hasMore = true;

      while (hasMore) {
        const submissionsRes = await fetch(
          `${baseUrl}/submissions/?limit=${limit}&offset=${offset}`,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );

        if (!submissionsRes.ok) {
          console.warn("Failed to fetch submissions page");
          break;
        }

        const data = await submissionsRes.json();
        const results = Array.isArray(data.results) ? data.results : [];

        if (results.length === 0) {
          hasMore = false;
        } else {
          allSubmissions = [...allSubmissions, ...results];
          offset += limit;

          // Stop if we've fetched all
          if (offset >= data.count) {
            hasMore = false;
          }
        }
      }

      setSubmissions(allSubmissions);
    } catch (error) {
      console.error("Error fetching statistics:", error);
      setSubmissions([]);
      setStats(null);
    } finally {
      setLoading(false);
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
      acceptanceRate:
        total > 0 ? Math.round((accepted / total) * 100) : 0,
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
    return Object.keys(languages).length > 0 ? languages : { python: 0 };
  };

  const getStreakDays = () => {
    if (submissions.length === 0) return 0;

    // Get unique submission dates
    const submissionDates = new Set();
    submissions.forEach((s) => {
      if (s.submitted_at) {
        const date = new Date(s.submitted_at);
        const dateString = date.toISOString().split('T')[0]; // YYYY-MM-DD
        submissionDates.add(dateString);
      }
    });

    if (submissionDates.size === 0) return 0;

    const sortedDates = Array.from(submissionDates).sort().reverse();
    let streak = 1;
    const today = new Date().toISOString().split('T')[0];

    // Check if most recent submission is today or yesterday
    const mostRecentDate = new Date(sortedDates[0]);
    const todayDate = new Date();
    const dayDiff = Math.floor(
      (todayDate - mostRecentDate) / (1000 * 60 * 60 * 24)
    );

    // If last submission is more than 1 day ago, streak is 0
    if (dayDiff > 1) return 0;

    // Count consecutive days
    for (let i = 1; i < sortedDates.length; i++) {
      const prevDate = new Date(sortedDates[i - 1]);
      const currDate = new Date(sortedDates[i]);

      const daysDiff = Math.floor(
        (prevDate - currDate) / (1000 * 60 * 60 * 24)
      );

      if (daysDiff === 1) {
        streak++;
      } else {
        break;
      }
    }

    return streak;
  };

  const stats_ = calculateStats();
  const difficultyStats = getDifficultyStats();
  const languageStats = getLanguageStats();
  const streak = getStreakDays();

  const chartData = {
    difficulty: [
      {
        name: "Easy",
        value: difficultyStats.easy,
        color: "#58a6ff",
      },
      {
        name: "Medium",
        value: difficultyStats.medium,
        color: "#f59e0b",
      },
      {
        name: "Hard",
        value: difficultyStats.hard,
        color: "#ef4444",
      },
    ],
    status: [
      { name: "Accepted", value: stats_.accepted, color: "#22c55e" },
      { name: "Wrong", value: stats_.wrong, color: "#ef4444" },
      { name: "Runtime", value: stats_.runtime, color: "#f59e0b" },
      { name: "TLE", value: stats_.tle, color: "#8b5cf6" },
    ],
  };

  return (
    <div className={`statistics ${isDark ? "dark" : "light"}`}>
      <div className="container">
        <div className="stats-header">
          <div>
            <h1>Statistika</h1>
            <p>Sizning taraqqiy va statistikasi</p>
          </div>
        </div>

        {loading ? (
          <div className="stats-loader">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="loader-card"></div>
            ))}
          </div>
        ) : submissions.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">📊</div>
            <h2>Hali statistika yo'q</h2>
            <p>Masalalarni yechib, statistikangizni to'ldiring</p>
          </div>
        ) : (
          <>
            {/* Main Stats */}
            <div className="main-stats-grid">
              <div className="stat-card large">
                <div className="stat-header">
                  <span className="stat-icon"><FaChartBar /></span>
                  <span className="stat-title">Jami Yechimlar</span>
                </div>
                <div className="stat-content">
                  <div className="stat-big-value">{stats_.total}</div>
                  <div className="stat-subtitle">yuborigan yechim</div>
                </div>
              </div>

              <div className="stat-card large success">
                <div className="stat-header">
                  <span className="stat-icon"><FaCheckCircle /></span>
                  <span className="stat-title">Qabul Qilingan</span>
                </div>
                <div className="stat-content">
                  <div className="stat-big-value">{stats_.accepted}</div>
                  <div className="stat-subtitle">
                    {stats_.acceptanceRate}% acceptance rate
                  </div>
                </div>
              </div>

              <div className="stat-card large">
                <div className="stat-header">
                  <span className="stat-icon"><FaFire /></span>
                  <span className="stat-title">Streyk</span>
                </div>
                <div className="stat-content">
                  <div className="stat-big-value">{streak}</div>
                  <div className="stat-subtitle">kun davomida</div>
                </div>
              </div>

              <div className="stat-card large">
                <div className="stat-header">
                  <span className="stat-icon"><FaStar /></span>
                  <span className="stat-title">Ball</span>
                </div>
                <div className="stat-content">
                  <div className="stat-big-value">{stats?.score || 0}</div>
                  <div className="stat-subtitle">jami ball</div>
                </div>
              </div>
            </div>

            {/* Secondary Stats */}
            <div className="secondary-stats-grid">
              <div className="stat-card">
                <div className="stat-header">
                  <span className="stat-icon"><MdErrorOutline /></span>
                  <span className="stat-title">Xato Javob</span>
                </div>
                <div className="stat-value">{stats_.wrong}</div>
              </div>

              <div className="stat-card">
                <div className="stat-header">
                  <span className="stat-icon"><MdErrorOutline /></span>
                  <span className="stat-title">Runtime Xatosi</span>
                </div>
                <div className="stat-value">{stats_.runtime}</div>
              </div>

              <div className="stat-card">
                <div className="stat-header">
                  <span className="stat-icon"><MdAccessTime /></span>
                  <span className="stat-title">Vaqt Limiti</span>
                </div>
                <div className="stat-value">{stats_.tle}</div>
              </div>

              <div className="stat-card">
                <div className="stat-header">
                  <span className="stat-icon"><MdPublic /></span>
                  <span className="stat-title">Mamlakat</span>
                </div>
                <div className="stat-value">{stats?.country || "-"}</div>
              </div>
            </div>

            {/* Charts */}
            <div className="charts-grid">
              {/* Difficulty Chart */}
              <div className="chart-card">
                <h3>Qiyinlik Bo'yicha</h3>
                <div className="chart-container">
                  {chartData.difficulty.map((item) => (
                    <div key={item.name} className="chart-bar-item">
                      <div className="chart-bar-header">
                        <span className="chart-label">{item.name}</span>
                        <span className="chart-value">{item.value}</span>
                      </div>
                      <div className="chart-bar-bg">
                        <div
                          className="chart-bar-fill"
                          style={{
                            width:
                              Math.max(
                                (item.value /
                                  Math.max(
                                    ...chartData.difficulty.map((x) => x.value),
                                    1
                                  )) *
                                  100,
                                5
                              ) + "%",
                            backgroundColor: item.color,
                          }}
                        ></div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Status Chart */}
              <div className="chart-card">
                <h3>Status Bo'yicha</h3>
                <div className="chart-container">
                  {chartData.status.map((item) => (
                    <div key={item.name} className="chart-bar-item">
                      <div className="chart-bar-header">
                        <span className="chart-label">{item.name}</span>
                        <span className="chart-value">{item.value}</span>
                      </div>
                      <div className="chart-bar-bg">
                        <div
                          className="chart-bar-fill"
                          style={{
                            width:
                              Math.max(
                                (item.value /
                                  Math.max(...chartData.status.map((x) => x.value), 1)) *
                                  100,
                                5
                              ) + "%",
                            backgroundColor: item.color,
                          }}
                        ></div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Language Chart */}
              <div className="chart-card">
                <h3>Tillar Bo'yicha</h3>
                <div className="chart-container language-list">
                  {Object.entries(languageStats).map(([lang, count]) => (
                    <div key={lang} className="language-item">
                      <span className="lang-badge">
                        {lang.toUpperCase()}
                      </span>
                      <span className="lang-count">{count} ta</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default Statistics;
