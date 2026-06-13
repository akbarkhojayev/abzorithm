import React, { useEffect, useState, useRef } from "react";
import "./ExamDetail.css";
import { baseUrl } from "../services/config.js";
import { getToken } from "../services/token.js";
import { useParams, useNavigate } from "react-router-dom";
import { useTheme } from "../../context/ThemeContext";
import Editor from "@monaco-editor/react";

function ExamDetail() {
  const { examId } = useParams();
  const navigate = useNavigate();
  const { isDark } = useTheme();

  // Main states
  const [exam, setExam] = useState(null);
  const [statistics, setStatistics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [examCompleted, setExamCompleted] = useState(false);

  // Exam session
  const [currentProblemIndex, setCurrentProblemIndex] = useState(0);
  const [submissions, setSubmissions] = useState({});
  const [submitting, setSubmitting] = useState(false);
  const [lastSubmissionResult, setLastSubmissionResult] = useState(null);

  // Timer
  const [timeLeft, setTimeLeft] = useState(null);
  const [examStartTime, setExamStartTime] = useState(null);

  // Security
  const [tabSwitchCount, setTabSwitchCount] = useState(0);
  const [focusLossCount, setFocusLossCount] = useState(0);
  const [isCompletingExam, setIsCompletingExam] = useState(false);

  // UI
  const [codeFontSize, setCodeFontSize] = useState(() => {
    const saved = localStorage.getItem("examCodeFontSize");
    return saved ? parseInt(saved) : 13;
  });
  const [showProblemPanel, setShowProblemPanel] = useState(true);

  // Refs
  const editorRef = useRef(null);
  const sessionIdRef = useRef(null);

  const currentQuestion = exam?.questions[currentProblemIndex];
  const currentProblem = currentQuestion?.problem_detail;
  const currentProblemId = currentQuestion?.problem;

  // ==================== LOAD ====================
  useEffect(() => {
    const loadExam = async () => {
      try {
        const examResponse = await fetch(`${baseUrl}/exams/${examId}/`, {
          headers: { Authorization: `Bearer ${getToken()}` },
        });

        if (!examResponse.ok) throw new Error("Imtixon yuklanmadi");

        const examData = await examResponse.json();
        setExam(examData);

        try {
          const statsResponse = await fetch(`${baseUrl}/exam-statistics/user/`, {
            headers: { Authorization: `Bearer ${getToken()}` },
          });

          if (statsResponse.ok) {
            const statsData = await statsResponse.json();
            const examStats = statsData.find(s => s.exam === examData.id);
            setStatistics(examStats);

            if (examStats && examStats.is_completed) {
              setExamCompleted(true);
              return;
            }

            if (examStats && examStats.status === 'in_progress') {
              const sessionKey = `exam_${examId}_session`;
              const existingSession = localStorage.getItem(sessionKey);

              if (existingSession) {
                const session = JSON.parse(existingSession);
                setExamStartTime(session.startTime);
                sessionIdRef.current = session.sessionId;
              } else {
                const startTime = Date.now();
                const sessionId = `${examId}_${Date.now()}`;
                sessionIdRef.current = sessionId;
                localStorage.setItem(sessionKey, JSON.stringify({ startTime, sessionId }));
                setExamStartTime(startTime);
              }
            }
          }
        } catch (err) {
          console.log("Stats fetch error");
        }

        if (!statistics) {
          const startTime = Date.now();
          const sessionId = `${examId}_${Date.now()}`;
          sessionIdRef.current = sessionId;
          localStorage.setItem(`exam_${examId}_session`, JSON.stringify({ startTime, sessionId }));
          setExamStartTime(startTime);
        }

        const initialSubmissions = {};
        examData.questions.forEach(q => {
          initialSubmissions[q.problem] = {
            code: localStorage.getItem(`exam_${examId}_problem_${q.problem}`) || "",
            language: examData.language || "python",
          };
        });
        setSubmissions(initialSubmissions);

      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    if (getToken()) {
      loadExam();
    } else {
      setError("Tizimga kiring");
      setLoading(false);
    }
  }, [examId]);

  // Save code
  useEffect(() => {
    if (currentProblemId) {
      const code = submissions[currentProblemId]?.code || "";
      localStorage.setItem(`exam_${examId}_problem_${currentProblemId}`, code);
    }
  }, [submissions, currentProblemId, examId]);

  // Save font size
  useEffect(() => {
    localStorage.setItem("examCodeFontSize", codeFontSize.toString());
  }, [codeFontSize]);

  // ==================== TIMER ====================
  useEffect(() => {
    if (!examStartTime) return;

    const timer = setInterval(() => {
      const elapsed = Math.floor((Date.now() - examStartTime) / 1000);
      const durationSeconds = (exam?.duration_minutes || 60) * 60;
      const remaining = Math.max(0, durationSeconds - elapsed);

      setTimeLeft(remaining);

      if (remaining === 0) {
        clearInterval(timer);
        handleTimeExpired();
      }
    }, 1000);

    return () => clearInterval(timer);
  }, [examStartTime, exam?.duration_minutes]);

  const handleTimeExpired = async () => {
    alert("⏰ Vaqt tugadi!");
    await markExamAsCompleted('timeout');
  };

  // ==================== SECURITY ====================
  useEffect(() => {
    if (!exam || examCompleted || isCompletingExam) return;

    const handleVisibilityChange = () => {
      if (document.hidden && !isCompletingExam) {
        const newCount = tabSwitchCount + 1;
        setTabSwitchCount(newCount);
        if (newCount >= 3) {
          alert("⚠️ Tab tabdili 3 marta!");
          markExamAsCompleted('violation');
        } else {
          alert(`⚠️ Tab tabdili: ${newCount}/3`);
        }
      }
    };

    const handleBlur = () => {
      if (isCompletingExam) return; // Ignore blur when completing

      const newCount = focusLossCount + 1;
      setFocusLossCount(newCount);
      if (newCount >= 3) {
        alert("⚠️ Fokus 3 marta yo'qoti!");
        markExamAsCompleted('violation');
      } else {
        alert(`⚠️ Fokus yo'qoti: ${newCount}/3`);
      }
    };

    document.addEventListener("visibilitychange", handleVisibilityChange);
    window.addEventListener("blur", handleBlur);

    return () => {
      document.removeEventListener("visibilitychange", handleVisibilityChange);
      window.removeEventListener("blur", handleBlur);
    };
  }, [tabSwitchCount, focusLossCount, examCompleted, exam, isCompletingExam]);

  // Keyboard blocking
  useEffect(() => {
    if (!exam || examCompleted) return;

    const handleKeyDown = (e) => {
      const blockedKeys = ['F12', 'F11'];
      const isCtrlCmd = e.ctrlKey || e.metaKey;

      if (blockedKeys.includes(e.key)) {
        e.preventDefault();
        return false;
      }

      if (isCtrlCmd && ['c', 'v', 'x', 'a'].includes(e.key.toLowerCase())) {
        e.preventDefault();
        return false;
      }

      if (e.key === 'Tab' && e.target !== editorRef.current?.getDomNode()) {
        e.preventDefault();
        return false;
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [examCompleted, exam]);

  // ==================== SUBMIT ====================
  const submitProblem = async () => {
    if (!exam || !currentProblemId) return;

    setSubmitting(true);
    try {
      const response = await fetch(`${baseUrl}/exams/submit/`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${getToken()}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          exam: exam.id,
          problem: currentProblemId,
          code: submissions[currentProblemId]?.code || "",
          language: exam.language,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        if (data.exam_completed) {
          setExamCompleted(true);
          setError("Bu imtixon yakunlangan!");
          return;
        }
        setLastSubmissionResult({
          status: "error",
          message: data.error || "Xato!",
        });
      } else {
        setLastSubmissionResult({
          status: data.status,
          message: data.message || `${data.status}!`,
        });
      }
    } catch (err) {
      console.error("Submit error:", err);
      setLastSubmissionResult({
        status: "error",
        message: "Serverga ulanib bo'lmadi",
      });
    } finally {
      setSubmitting(false);
    }
  };

  // ==================== COMPLETE ====================
  const markExamAsCompleted = async (reason = 'manual') => {
    try {
      console.log("Exam completing with reason:", reason);
      const response = await fetch(`${baseUrl}/exams/${examId}/complete/`, {
        method: "PATCH",
        headers: {
          Authorization: `Bearer ${getToken()}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ reason }),
      });

      const data = await response.json();
      console.log("Completion response:", response.status, data);

      if (response.ok) {
        console.log("Exam completed successfully, stats:", data.statistics);

        // Clean up session
        localStorage.removeItem(`exam_${examId}_session`);

        // Update state - this should trigger results page to show
        if (data.statistics) {
          setStatistics(data.statistics);
        } else if (data) {
          setStatistics(data);
        }

        // Set exam completed after a tiny delay to ensure state updates
        setTimeout(() => {
          setExamCompleted(true);
        }, 100);

        // Navigate after results show for 3 seconds
        setTimeout(() => {
          console.log("Navigating to exams");
          navigate("/exams");
        }, 3000);
      } else {
        console.error("Completion failed:", response.status, data);
        alert("❌ Xato: " + (data.error || data.message || "Imtixonni yakunlay olmadi"));
      }
    } catch (err) {
      console.error("Complete error:", err);
      alert("❌ Xato: " + err.message);
    }
  };

  const handleFinishExam = async () => {
    setIsCompletingExam(true); // Disable security checks during completion
    const confirmed = confirm("Imtixonni yakunlamoqchisiz? Bu amalni qaytara olmaysiz!");

    if (confirmed) {
      console.log("Exam finish confirmed");
      await markExamAsCompleted('manual');
    } else {
      // User cancelled, re-enable security checks
      setIsCompletingExam(false);
    }
  };

  // ==================== FORMAT ====================
  const formatTime = (seconds) => {
    if (!seconds) return "00:00";
    const hours = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return hours > 0
      ? `${hours}:${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`
      : `${mins}:${secs.toString().padStart(2, "0")}`;
  };

  // ==================== RENDER ====================
  if (loading) return <div className="exam-loading">Yuklanmoqda...</div>;

  if (error && !exam) {
    return (
      <div className={`exam-error-page ${isDark ? "dark" : "light"}`}>
        <div className="error-content">
          <h2>❌ {error}</h2>
          <button onClick={() => navigate("/exams")}>Imtixonlarga qaytish</button>
        </div>
      </div>
    );
  }

  if (examCompleted) {
    return <ExamResultsPage exam={exam} statistics={statistics} isDark={isDark} />;
  }

  return (
    <div className={`exam-panel ${isDark ? "dark" : "light"}`}>
      {/* Top Bar */}
      <div className="exam-topbar">
        <div className="exam-info">
          <h1>{exam?.title}</h1>
          <span className="exam-lang">
            {exam?.language === 'python' && 'Python'}
            {exam?.language === 'javascript' && 'JavaScript'}
            {exam?.language === 'dart' && 'Dart'}
          </span>
        </div>
        <div className="exam-stats">
          <div className="stat">
            <span className="label">{currentProblemIndex + 1}/{exam?.questions.length}</span>
          </div>
          <div className="timer-badge" style={{ color: timeLeft < 300 ? '#ef4444' : '#10b981' }}>
            {formatTime(timeLeft)}
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="exam-content">
        {/* Left Panel - Problem */}
        {showProblemPanel && (
          <div className="problem-panel">
            <div className="panel-header">
              <h2>{currentProblem?.title}</h2>
              <span className={`difficulty ${currentProblem?.difficulty?.toLowerCase()}`}>
                {currentProblem?.difficulty}
              </span>
            </div>

            <div className="panel-body">
              <p className="description">{currentProblem?.description}</p>

              {currentProblem?.input_example && (
                <div className="example">
                  <h4>Kirish</h4>
                  <code>{currentProblem.input_example}</code>
                </div>
              )}

              {currentProblem?.output_example && (
                <div className="example">
                  <h4>Chiqish</h4>
                  <code>{currentProblem.output_example}</code>
                </div>
              )}
            </div>

            <div className="panel-tabs">
              {exam?.questions.map((q, idx) => (
                <button
                  key={q.id}
                  className={`tab ${idx === currentProblemIndex ? 'active' : ''}`}
                  onClick={() => setCurrentProblemIndex(idx)}
                >
                  <span className="tab-num">{idx + 1}</span>
                  <span className="tab-name">{q.problem_detail?.title}</span>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Right Panel - Editor */}
        <div className="editor-panel">
          <div className="editor-header">
            <div className="editor-title">
              <span>Kod</span>
            </div>
            <div className="editor-tools">
              <button
                className="tool-btn toggle-btn"
                onClick={() => setShowProblemPanel(!showProblemPanel)}
                title="Savol panelini ko'rsatish/yashirish"
              >
                {showProblemPanel ? '◀' : '▶'}
              </button>
              <div className="font-size-control">
                <button
                  className="tool-btn"
                  onClick={() => setCodeFontSize(Math.max(12, codeFontSize - 1))}
                >
                  −
                </button>
                <span className="font-size">{codeFontSize}</span>
                <button
                  className="tool-btn"
                  onClick={() => setCodeFontSize(Math.min(22, codeFontSize + 1))}
                >
                  +
                </button>
              </div>
            </div>
          </div>

          <div className="editor-wrapper">
            <Editor
              height="100%"
              language={exam?.language === 'javascript' ? 'javascript' : exam?.language === 'dart' ? 'dart' : 'python'}
              value={submissions[currentProblemId]?.code || ""}
              onChange={(value) => {
                setSubmissions(prev => ({
                  ...prev,
                  [currentProblemId]: {
                    ...prev[currentProblemId],
                    code: value || ""
                  }
                }));
              }}
              onMount={(editor) => (editorRef.current = editor)}
              theme={isDark ? "vs-dark" : "vs-light"}
              options={{
                fontSize: codeFontSize,
                minimap: { enabled: false },
                wordWrap: 'on',
                scrollBeyondLastLine: false,
                padding: { top: 16, bottom: 16 },
              }}
            />
          </div>

          <div className="editor-footer">
            {lastSubmissionResult && (
              <div className={`result-indicator ${lastSubmissionResult.status}`}>
                <span className="result-icon">
                  {lastSubmissionResult.status === 'Accepted' ? '✓' : '✗'}
                </span>
                <span className="result-text">{lastSubmissionResult.message}</span>
                {lastSubmissionResult.status === 'Accepted' ? (
                  <button
                    className="result-action"
                    onClick={() => {
                      if (currentProblemIndex + 1 >= exam.questions.length) {
                        handleFinishExam();
                      } else {
                        setCurrentProblemIndex(prev => prev + 1);
                        setLastSubmissionResult(null);
                      }
                    }}
                  >
                    {currentProblemIndex + 1 >= exam.questions.length ? 'Yakunlash' : 'Keyingi'}
                  </button>
                ) : (
                  <button
                    className="result-action"
                    onClick={() => setLastSubmissionResult(null)}
                  >
                    Yopish
                  </button>
                )}
              </div>
            )}
            <div className="editor-actions">
              <button
                className="action-btn submit"
                onClick={submitProblem}
                disabled={submitting}
              >
                {submitting ? '⏳ Yuborilmoqda...' : '▶ Yuborish'}
              </button>
              <button
                className="action-btn finish"
                onClick={handleFinishExam}
              >
                ✓ Yakunlash
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// Results Page
function ExamResultsPage({ exam, statistics, isDark }) {
  const navigate = useNavigate();

  // Debugging
  console.log("ExamResultsPage render, statistics:", statistics);

  const total = exam?.questions?.length || 0;
  const solved = statistics?.solved_problems || 0;
  const score = statistics?.score || 0;
  const percent = total > 0 ? (solved / total) * 100 : 0;

  // If no statistics, show loading
  if (!statistics) {
    return (
      <div className={`results-page ${isDark ? "dark" : "light"}`}>
        <div className="results-wrapper">
          <div className="results-box">
            <h1>📊 Natijalari yuklanmoqda...</h1>
          </div>
        </div>
      </div>
    );
  }

  const getStatus = () => {
    return '✅ Yakunlangan';
  };

  return (
    <div className={`results-page ${isDark ? "dark" : "light"}`}>
      <div className="results-wrapper">
        <div className="results-box">
          <h1>Natijalari</h1>

          <div className="results-stats">
            <div className="result-stat">
              <span className="result-label">Ball</span>
              <span className="result-value">{score} / 500</span>
            </div>

            <div className="result-stat">
              <span className="result-label">Yechilgan</span>
              <span className="result-value">{solved} / {total}</span>
            </div>

            <div className="result-stat">
              <span className="result-label">Foiz</span>
              <span className="result-value">{percent.toFixed(0)}%</span>
            </div>

            <div className="result-stat">
              <span className="result-label">Status</span>
              <span className="result-value">{getStatus()}</span>
            </div>
          </div>

          <button className="back-btn" onClick={() => navigate("/exams")}>
            Imtixonlarga qaytish
          </button>
        </div>
      </div>
    </div>
  );
}

export default ExamDetail;
