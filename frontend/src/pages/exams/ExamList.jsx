import React, { useEffect, useState } from "react";
import "./ExamList.css";
import { baseUrl } from "../services/config.js";
import { getToken } from "../services/token.js";
import { useNavigate } from "react-router-dom";
import { useTheme } from "../../context/ThemeContext";
import { FaClock, FaBook, FaCalendarAlt, FaCheckCircle, FaPlayCircle, FaArrowRight } from "react-icons/fa";

function ExamList() {
  const [exams, setExams] = useState([]);
  const [statistics, setStatistics] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const { isDark } = useTheme();

  const fetchExamsAndStats = async () => {
    try {
      const timestamp = Date.now();
      const examResponse = await fetch(`${baseUrl}/exams/?t=${timestamp}`, {
        headers: { Authorization: `Bearer ${getToken()}` },
        cache: 'no-store',
      });

      if (!examResponse.ok) throw new Error("Imtixonlar yuklanmadi");

      const examData = await examResponse.json();
      setExams(examData);

      // Always fetch fresh stats, don't use cache
      const statsResponse = await fetch(`${baseUrl}/exam-statistics/user/?t=${timestamp}`, {
        headers: { Authorization: `Bearer ${getToken()}` },
        cache: 'no-store',
      }).catch(() => null);

      if (statsResponse?.ok) {
        const statsData = await statsResponse.json();
        const statsMap = {};

        if (Array.isArray(statsData)) {
          statsData.forEach((stat) => {
            statsMap[stat.exam] = stat;
          });
        }

        setStatistics(statsMap);
        console.log("Updated statistics:", statsMap);
      } else {
        console.warn("Stats fetch failed:", statsResponse?.status);
        setStatistics({});
      }

      setError(null);
    } catch (err) {
      console.error("Fetch error:", err);
      setError(err.message);
      setExams([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (getToken()) {
      fetchExamsAndStats();
    } else {
      setLoading(false);
      setError("Tizimga kirish kerak");
    }
  }, []);

  useEffect(() => {
    const handleVisibilityChange = () => {
      if (document.visibilityState === 'visible') {
        setLoading(true);
        fetchExamsAndStats();
      }
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);
    return () => document.removeEventListener('visibilitychange', handleVisibilityChange);
  }, []);

  if (loading) {
    return (
      <div className="exam-list-container">
        <div className="loading">Yuklanmoqda...</div>
      </div>
    );
  }

  const getStatusInfo = (status) => {
    const statusMap = {
      'not_started': { label: 'Boshlash', class: 'not-started' },
      'in_progress': { label: 'Davom Et', class: 'in-progress' },
      'completed': { label: 'Yechilgan', class: 'completed' }
    };
    return statusMap[status] || statusMap['not_started'];
  };

  const getLanguageLabel = (lang) => {
    const langMap = {
      'javascript': 'JavaScript',
      'python': 'Python',
      'dart': 'Dart',
    };
    return langMap[lang] || lang;
  };

  return (
    <div className="exam-list-container">
      <header className="exam-list-header">
        <h1>Imtixonlar</h1>
        <p>Sizga tayinlangan imtixonlar ro'yxati</p>
      </header>

      {error && (
        <div className="error-message">
          <p>{error}</p>
        </div>
      )}

      {exams.length === 0 ? (
        <div className="empty-state">
          <h2>Imtixon topilmadi</h2>
          <p>Hozircha sizga tayinlangan imtixon yo'q</p>
        </div>
      ) : (
        <div className="exam-grid">
          {exams.map((exam) => {
            const stat = statistics[exam.id];
            const status = stat?.status || 'not_started';
            const statusInfo = getStatusInfo(status);

            return (
              <div key={exam.id} className="exam-card">
                <div className="exam-card-header">
                  <div className="exam-card-title-block">
                    <h3 className="exam-card-title">{exam.title}</h3>
                    <span className="exam-card-lang">{getLanguageLabel(exam.language)}</span>
                  </div>
                  <span className={`exam-status ${statusInfo.class}`}>
                    {statusInfo.label}
                  </span>
                </div>

                <div className="exam-card-body">
                  {exam.description && (
                    <p className="exam-desc">{exam.description}</p>
                  )}

                  <div className="exam-meta">
                    <div className="exam-meta-item">
                      <FaClock className="exam-meta-icon" />
                      <span className="exam-meta-label">Vaqt</span>
                      <span className="exam-meta-value">{exam.duration_minutes} min</span>
                    </div>
                    <div className="exam-meta-item">
                      <FaBook className="exam-meta-icon" />
                      <span className="exam-meta-label">Masalalar</span>
                      <span className="exam-meta-value">{exam.question_count}</span>
                    </div>
                  </div>

                  <div className="exam-dates">
                    <FaCalendarAlt />
                    <span>
                      {new Date(exam.start_time).toLocaleDateString("uz-UZ")} — {new Date(exam.end_time).toLocaleDateString("uz-UZ")}
                    </span>
                  </div>
                </div>

                <div className="exam-card-footer">
                  <button
                    className={`exam-btn ${statusInfo.class}`}
                    onClick={() => navigate(`/exam/${exam.id}`)}
                  >
                    {status === 'completed' ? (
                      <>
                        <FaCheckCircle /> Natijasini ko'rish
                      </>
                    ) : status === 'in_progress' ? (
                      <>
                        <FaArrowRight /> Davom Et
                      </>
                    ) : (
                      <>
                        <FaPlayCircle /> Boshlash
                      </>
                    )}
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

export default ExamList;
