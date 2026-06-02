import React, { useEffect, useState } from "react";
import "./Statistics.css";
import { baseUrl } from "../services/config.js";
import { getToken } from "../services/token.js";
import { getProfilMe } from "../services/app.js";
import { FaChartBar, FaCheckCircle, FaFire, FaStar } from "react-icons/fa";
import { MdErrorOutline, MdAccessTime, MdPublic } from "react-icons/md";

function Statistics() {
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

      const [profilRes, submissionsRes] = await Promise.all([
        fetch(`${baseUrl}/users/me/`, {
          headers: { Authorization: `Bearer ${token}` },
        }),
        fetch(`${baseUrl}/submissions/`, {
          headers: { Authorization: `Bearer ${token}` },
        }),
      ]);

      if (!profilRes.ok || !submissionsRes.ok) {
        throw new Error("Failed to fetch data");
      }

      const profil = await profilRes.json();
      const submissions = await submissionsRes.json();

      setStats(profil);
      setSubmissions(Array.isArray(submissions) ? submissions : []);
    } catch (error) {
      console.error("Error:", error);
      setSubmissions([]);
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
        const difficulty = s.difficulty?.toLowerCase() || "easy";
        difficulties[difficulty]++;
      });
    return difficulties;
  };

  const getLanguageStats = () => {
    const languages = {};
    submissions.forEach((s) => {
      const lang = s.language || "other";
      languages[lang] = (languages[lang] || 0) + 1;
    });
    return languages;
  };

  const getStreakDays = () => {
    if (submissions.length === 0) return 0;

    const submissionDates = new Set();
    submissions.forEach((s) => {
      const date = new Date(s.submitted_at);
      submissionDates.add(
        `${date.getFullYear()}-${date.getMonth()}-${date.getDate()}`
      );
    });

    const sortedDates = Array.from(submissionDates).sort().reverse();
    let streak = 0;
    const today = new Date();

    for (let i = 0; i < sortedDates.length; i++) {
      const currentDate = new Date(sortedDates[i]);
      const expectedDate = new Date(today);
      expectedDate.setDate(expectedDate.getDate() - i);

      if (
        currentDate.toDateString() === expectedDate.toDateString() ||
        (i === 0 && currentDate < expectedDate)
      ) {
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
        color: "#3b82f6",
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
    <div className="statistics">
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
