import React, { useEffect, useState } from "react";
import "./ExamList.css";
import { baseUrl } from "../services/config.js";
import { getToken } from "../services/token.js";
import { useNavigate } from "react-router-dom";
import { useTheme } from "../../context/ThemeContext";
import { FaClock, FaQuestion, FaCalendar, FaCheckCircle, FaPauseCircle, FaPlayCircle } from "react-icons/fa";

function ExamList() {
  const [exams, setExams] = useState([]);
  const [statistics, setStatistics] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const { isDark } = useTheme();

  useEffect(() => {
    const fetchExamsAndStats = async () => {
      try {
        // Fetch exams
        const examResponse = await fetch(`${baseUrl}/exams/`, {
          headers: {
            Authorization: `Bearer ${getToken()}`,
          },
        });

        if (!examResponse.ok) {
          throw new Error("Failed to fetch exams");
        }

        const examData = await examResponse.json();
        console.log("Exams loaded:", examData.length);
        setExams(examData);

        // Fetch statistics (non-blocking)
        const statsResponse = await fetch(`${baseUrl}/exam-statistics/user/`, {
          headers: {
            Authorization: `Bearer ${getToken()}`,
          },
        }).catch(err => {
          console.log("Stats fetch error:", err);
          return null;
        });

        if (statsResponse && statsResponse.ok) {
          try {
            const statsData = await statsResponse.json();
            console.log("Statistics loaded:", statsData.length);
            const statsMap = {};
            statsData.forEach((stat) => {
              statsMap[stat.exam] = stat;
            });
            setStatistics(statsMap);
          } catch (parseErr) {
            console.log("Could not parse statistics:", parseErr);
          }
        }

        setError(null);
      } catch (err) {
        console.error("Error:", err);
        setError(err.message);
        setExams([]);
      } finally {
        setLoading(false);
      }
    };

    if (getToken()) {
      fetchExamsAndStats();
    } else {
      setLoading(false);
      setError("Please log in to view exams");
    }
  }, []);

  if (loading) {
    return (
      <div className="exam-list-container">
        <div className="loading">Loading exams...</div>
      </div>
    );
  }

  return (
    <div className={`exam-list-container ${isDark ? "dark" : "light"}`}>
      <div className="exam-list-header">
        <h1>Imtixonlar</h1>
        <p>Sizga tayinlangan imtixonlar ro'yxati</p>
      </div>

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
            const statusTexts = {
              'not_started': 'Boshlash',
              'in_progress': 'Davom etyapti',
              'completed': 'Yechilgan',
            };

            return (
              <div key={exam.id} className={`exam-card ${stat?.status || 'not_started'}`}>
                <div className="exam-card-header">
                  <div className="exam-title-section">
                    <h3>{exam.title}</h3>
                    <span className="exam-language">
                      {exam.language === 'javascript' && 'JavaScript'}
                      {exam.language === 'dart' && 'Dart'}
                      {exam.language === 'python' && 'Python'}
                    </span>
                  </div>
                  <span className={`exam-status-badge ${stat?.status || 'not_started'}`}>
                    {statusTexts[stat?.status || 'not_started']}
                  </span>
                </div>

                <div className="exam-card-body">
                  {exam.description && (
                    <p className="exam-description">{exam.description}</p>
                  )}

                  <div className="exam-info">
                    <div className="info-item">
                      <FaClock className="info-icon" />
                      <span className="info-value">{exam.duration_minutes} min</span>
                    </div>
                    <div className="info-item">
                      <FaQuestion className="info-icon" />
                      <span className="info-value">{exam.question_count} ta</span>
                    </div>
                  </div>


                  <div className="exam-dates">
                    <FaCalendar className="date-icon" />
                    <small>
                      {new Date(exam.start_time).toLocaleDateString("uz-UZ")} - {new Date(exam.end_time).toLocaleDateString("uz-UZ")}
                    </small>
                  </div>
                </div>

                <div className="exam-card-footer">
                  <button
                    className={`btn-take-exam ${stat?.status || 'not_started'}`}
                    onClick={() => navigate(`/exam/${exam.id}`)}
                  >
                    {stat?.status === 'completed' && (
                      <>
                        <FaCheckCircle /> Yechilgan
                      </>
                    )}
                    {stat?.status === 'in_progress' && (
                      <>
                        <FaPauseCircle /> Davom Et
                      </>
                    )}
                    {(!stat || stat?.status === 'not_started') && (
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
