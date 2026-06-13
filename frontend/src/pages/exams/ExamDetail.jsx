import React, { useEffect, useState, useRef } from "react";
import "./ExamDetail.css";
import { baseUrl } from "../services/config.js";
import { getToken } from "../services/token.js";
import { useParams, useNavigate } from "react-router-dom";
import { useTheme } from "../../context/ThemeContext";
import Editor from "@monaco-editor/react";
import { FaClock, FaCheck, FaTimes, FaChevronRight, FaChevronLeft, FaSync } from "react-icons/fa";

function ExamDetail() {
  const { examId } = useParams();
  const navigate = useNavigate();
  const { isDark } = useTheme();

  const [exam, setExam] = useState(null);
  const [statistics, setStatistics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [examCompleted, setExamCompleted] = useState(false);

  const [currentProblemIndex, setCurrentProblemIndex] = useState(0);
  const [submissions, setSubmissions] = useState({});
  const [submitting, setSubmitting] = useState(false);
  const [lastSubmissionResult, setLastSubmissionResult] = useState(null);

  const [timeLeft, setTimeLeft] = useState(null);
  const [examStartTime, setExamStartTime] = useState(null);

  const [tabSwitchCount, setTabSwitchCount] = useState(0);
  const [focusLossCount, setFocusLossCount] = useState(0);
  const [isCompletingExam, setIsCompletingExam] = useState(false);

  const [codeFontSize, setCodeFontSize] = useState(() => {
    const saved = localStorage.getItem("examCodeFontSize");
    return saved ? parseInt(saved) : 14;
  });

  const [editorHeightPercent, setEditorHeightPercent] = useState(() => {
    const saved = localStorage.getItem("examEditorHeightPercent");
    return saved ? parseFloat(saved) : 60;
  });

  const [isResizingEditor, setIsResizingEditor] = useState(false);
  const [showTestsTab, setShowTestsTab] = useState(true);

  const editorRef = useRef(null);
  const sessionIdRef = useRef(null);
  const panelRightRef = useRef(null);
  const dragRef = useRef({ startY: 0, startPercent: 0 });

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
          const savedCode = localStorage.getItem(`exam_${examId}_problem_${q.problem}`);
          const template = q.problem_detail?.template || "";

          initialSubmissions[q.problem] = {
            code: savedCode || template || "",
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

  useEffect(() => {
    if (currentProblemId) {
      const code = submissions[currentProblemId]?.code || "";
      localStorage.setItem(`exam_${examId}_problem_${currentProblemId}`, code);
    }
  }, [submissions, currentProblemId, examId]);

  useEffect(() => {
    localStorage.setItem("examCodeFontSize", codeFontSize.toString());
  }, [codeFontSize]);

  useEffect(() => {
    localStorage.setItem("examEditorHeightPercent", editorHeightPercent.toFixed(2));
  }, [editorHeightPercent]);

  // ==================== RESIZE EDITOR ====================
  const handleMouseDownEditorResize = (e) => {
    setIsResizingEditor(true);
    dragRef.current = { startY: e.clientY, startPercent: editorHeightPercent };
  };

  useEffect(() => {
    const handleMouseMove = (e) => {
      if (isResizingEditor && panelRightRef.current) {
        const containerHeight = panelRightRef.current.clientHeight;
        const delta = e.clientY - dragRef.current.startY;
        const deltaPercent = (delta / containerHeight) * 100;
        const newPercent = dragRef.current.startPercent + deltaPercent;

        const clampedPercent = Math.max(30, Math.min(newPercent, 70));
        setEditorHeightPercent(clampedPercent);
      }
    };

    const handleMouseUp = () => {
      setIsResizingEditor(false);
    };

    if (isResizingEditor) {
      document.addEventListener("mousemove", handleMouseMove);
      document.addEventListener("mouseup", handleMouseUp);
      document.body.style.cursor = "row-resize";
      document.body.style.userSelect = "none";

      return () => {
        document.removeEventListener("mousemove", handleMouseMove);
        document.removeEventListener("mouseup", handleMouseUp);
        document.body.style.cursor = "auto";
        document.body.style.userSelect = "auto";
      };
    }
  }, [isResizingEditor, editorHeightPercent]);

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
    alert("Vaqt tugadi!");
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
          alert("Tab tabdili 3 marta!");
          markExamAsCompleted('violation');
        } else {
          alert(`Tab tabdili: ${newCount}/3`);
        }
      }
    };

    const handleBlur = () => {
      if (isCompletingExam) return;

      const newCount = focusLossCount + 1;
      setFocusLossCount(newCount);
      if (newCount >= 3) {
        alert("Fokus 3 marta yo'qoti!");
        markExamAsCompleted('violation');
      } else {
        alert(`Fokus yo'qoti: ${newCount}/3`);
      }
    };

    document.addEventListener("visibilitychange", handleVisibilityChange);
    window.addEventListener("blur", handleBlur);

    return () => {
      document.removeEventListener("visibilitychange", handleVisibilityChange);
      window.removeEventListener("blur", handleBlur);
    };
  }, [tabSwitchCount, focusLossCount, examCompleted, exam, isCompletingExam]);

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

  const markExamAsCompleted = async (reason = 'manual') => {
    try {
      const response = await fetch(`${baseUrl}/exams/${examId}/complete/`, {
        method: "PATCH",
        headers: {
          Authorization: `Bearer ${getToken()}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ reason }),
      });

      const data = await response.json();

      if (response.ok) {
        if (data.statistics) {
          setStatistics(data.statistics);
        } else if (data) {
          setStatistics(data);
        }

        setTimeout(() => {
          setExamCompleted(true);
        }, 100);

        setTimeout(() => {
          navigate("/exams");
        }, 3000);
      } else {
        alert("Xato: " + (data.error || data.message || "Imtixonni yakunlay olmadi"));
      }
    } catch (err) {
      console.error("Complete error:", err);
      alert("Xato: " + err.message);
    }
  };

  const handleFinishExam = async () => {
    setIsCompletingExam(true);
    const confirmed = confirm("Imtixonni yakunlamoqchisiz? Bu amalni qaytara olmaysiz!");

    if (confirmed) {
      await markExamAsCompleted('manual');
    } else {
      setIsCompletingExam(false);
    }
  };

  const resetToTemplate = () => {
    const template = currentProblem?.template || "";
    setSubmissions(prev => ({
      ...prev,
      [currentProblemId]: {
        ...prev[currentProblemId],
        code: template
      }
    }));
  };

  const formatTime = (seconds) => {
    if (!seconds && seconds !== 0) return "00:00";
    const hours = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return hours > 0
      ? `${hours}:${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`
      : `${mins}:${secs.toString().padStart(2, "0")}`;
  };

  // ==================== RENDER ====================
  if (loading) {
    return (
      <div className="exam-layout">
        <div className="loading-state">Yuklanmoqda...</div>
      </div>
    );
  }

  if (error && !exam) {
    return (
      <div className="exam-layout">
        <div className="error-state">
          <h2>{error}</h2>
          <button className="btn-primary" onClick={() => navigate("/exams")}>
            Imtixonlarga qaytish
          </button>
        </div>
      </div>
    );
  }

  if (examCompleted) {
    return <ExamResultsPage exam={exam} statistics={statistics} />;
  }

  const timeColor = timeLeft < 300 ? '#ef4444' : timeLeft < 600 ? '#f59e0b' : '#10b981';

  return (
    <div className="exam-layout">
      {/* HEADER */}
      <header className="exam-top-header">
        <div className="header-left">
          <h1 className="exam-title">{exam?.title}</h1>
          <span className="exam-lang-badge">{exam?.language?.toUpperCase()}</span>
        </div>
        <div className="header-right">
          <div className="exam-counter">{currentProblemIndex + 1}/{exam?.questions?.length}</div>
          <div className="exam-timer-display" style={{ color: timeColor }}>
            <FaClock />
            <span>{formatTime(timeLeft)}</span>
          </div>
        </div>
      </header>

      {/* MAIN CONTENT */}
      <main className="exam-main-area">
        {/* LEFT PANEL - PROBLEM */}
        <div className="problem-panel">
          <div className="problem-content-scroll">
            <div className="problem-header-block">
              <div className="problem-title-block">
                <span className="problem-num-circle">{currentProblemIndex + 1}</span>
                <h2>{currentProblem?.title}</h2>
              </div>
              <span className={`difficulty-badge difficulty-${currentProblem?.difficulty?.toLowerCase()}`}>
                {currentProblem?.difficulty}
              </span>
            </div>

            <div className="problem-description-block">
              <p>{currentProblem?.description}</p>
            </div>

            {currentProblem?.input_example && (
              <div className="example-block">
                <h4>Kirish Misoli</h4>
                <pre>{currentProblem.input_example}</pre>
              </div>
            )}

            {currentProblem?.output_example && (
              <div className="example-block">
                <h4>Chiqish Misoli</h4>
                <pre>{currentProblem.output_example}</pre>
              </div>
            )}
          </div>

          <div className="problem-footer">
            <div className="problem-tabs-container">
              {exam?.questions?.map((q, idx) => (
                <button
                  key={q.id}
                  className={`problem-tab ${idx === currentProblemIndex ? 'active' : ''}`}
                  onClick={() => setCurrentProblemIndex(idx)}
                  title={q.problem_detail?.title}
                >
                  {idx + 1}
                </button>
              ))}
            </div>

            <div className="problem-buttons">
              <button
                className="btn-nav"
                onClick={() => setCurrentProblemIndex(Math.max(0, currentProblemIndex - 1))}
                disabled={currentProblemIndex === 0}
              >
                <FaChevronLeft /> Oldingi
              </button>
              <button
                className="btn-nav"
                onClick={() => setCurrentProblemIndex(Math.min(exam.questions.length - 1, currentProblemIndex + 1))}
                disabled={currentProblemIndex === exam.questions.length - 1}
              >
                Keyingi <FaChevronRight />
              </button>
            </div>
          </div>
        </div>

        {/* RIGHT PANEL - EDITOR + TESTS */}
        <div className="editor-panel" ref={panelRightRef}>
          {/* EDITOR SECTION */}
          <div className="editor-top-section" style={{ height: `${editorHeightPercent}%` }}>
            <div className="editor-top-bar">
              <div className="font-controls">
                <button
                  className="font-btn"
                  onClick={() => setCodeFontSize(Math.max(12, codeFontSize - 1))}
                >
                  −
                </button>
                <span className="font-size-display">{codeFontSize}</span>
                <button
                  className="font-btn"
                  onClick={() => setCodeFontSize(Math.min(22, codeFontSize + 1))}
                >
                  +
                </button>
                {currentProblem?.template && (
                  <button
                    className="template-reset-btn"
                    onClick={resetToTemplate}
                    title="Shablonga qaytarish"
                  >
                    <FaSync />
                  </button>
                )}
              </div>
            </div>

            <div className="editor-workspace">
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
                }}
              />
            </div>
          </div>

          {/* DIVIDER */}
          <div
            className={`editor-divider ${isResizingEditor ? 'active' : ''}`}
            onMouseDown={handleMouseDownEditorResize}
          />

          {/* TEST/RESULTS SECTION */}
          <div className="editor-bottom-section" style={{ height: `${100 - editorHeightPercent}%` }}>
            <div className="test-tabs">
              <button
                className={`test-tab ${showTestsTab ? 'active' : ''}`}
                onClick={() => setShowTestsTab(true)}
              >
                Natija
              </button>
              <button
                className={`test-tab ${!showTestsTab ? 'active' : ''}`}
                onClick={() => setShowTestsTab(false)}
              >
                Ma'lumot
              </button>
            </div>

            <div className="test-content">
              {showTestsTab && (
                <>
                  <div className="test-status-display">
                    {lastSubmissionResult ? (
                      <div className={`submission-status ${lastSubmissionResult.status}`}>
                        <div className="status-icon-block">
                          {lastSubmissionResult.status === 'Accepted' ? (
                            <FaCheck className="status-check-icon" />
                          ) : (
                            <FaTimes className="status-error-icon" />
                          )}
                        </div>
                        <div className="status-text-block">
                          <h3>{lastSubmissionResult.status === 'Accepted' ? 'To\'g\'ri!' : 'Xato!'}</h3>
                          <p>{lastSubmissionResult.message}</p>
                        </div>
                      </div>
                    ) : (
                      <div className="no-submission">
                        <p>📝 Kodingizni yuboring natijani ko'rish uchun</p>
                      </div>
                    )}
                  </div>

                  {lastSubmissionResult && (
                    <div className="test-details-block">
                      <div className="detail-item">
                        <label>Masala</label>
                        <span>{currentProblem?.title}</span>
                      </div>
                      <div className="detail-item">
                        <label>Qiynchiligi</label>
                        <span>{currentProblem?.difficulty}</span>
                      </div>
                      <div className="detail-item">
                        <label>Raqam</label>
                        <span>{currentProblemIndex + 1}/{exam?.questions?.length}</span>
                      </div>
                    </div>
                  )}
                </>
              )}

              {!showTestsTab && (
                <div className="test-info-panel">
                  <div className="info-header">📋 Masala Ma'lumotlari</div>
                  <div className="info-details">
                    <div className="info-row">
                      <span className="info-key">Nomi:</span>
                      <span className="info-val">{currentProblem?.title}</span>
                    </div>
                    <div className="info-row">
                      <span className="info-key">Qiynchiligi:</span>
                      <span className="info-val">{currentProblem?.difficulty}</span>
                    </div>
                    <div className="info-row">
                      <span className="info-key">Raqam:</span>
                      <span className="info-val">{currentProblemIndex + 1}/{exam?.questions?.length}</span>
                    </div>
                    <div className="info-row">
                      <span className="info-key">Til:</span>
                      <span className="info-val">{exam?.language?.toUpperCase()}</span>
                    </div>
                  </div>
                </div>
              )}
            </div>

            <div className="test-actions">
              <button
                className="btn-submit"
                onClick={submitProblem}
                disabled={submitting}
              >
                {submitting ? 'Yuborilmoqda...' : 'Yuborish'}
              </button>
              <button
                className="btn-finish-exam"
                onClick={handleFinishExam}
              >
                Imtixonni Yakunlash
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

function ExamResultsPage({ exam, statistics }) {
  const navigate = useNavigate();

  const total = exam?.questions?.length || 0;
  const solved = statistics?.solved_problems || 0;
  const score = statistics?.score || 0;
  const percent = total > 0 ? (solved / total) * 100 : 0;

  if (!statistics) {
    return (
      <div className="exam-layout">
        <div className="loading-state">Natijalar yuklanmoqda...</div>
      </div>
    );
  }

  return (
    <div className="exam-layout results-layout">
      <div className="results-content">
        <h1>Imtixon Yakunlandi!</h1>

        <div className="results-stats">
          <div className="stat-box">
            <span className="stat-label">Ball</span>
            <span className="stat-value">{score}/500</span>
          </div>
          <div className="stat-box">
            <span className="stat-label">Yechilgan</span>
            <span className="stat-value">{solved}/{total}</span>
          </div>
          <div className="stat-box">
            <span className="stat-label">Foiz</span>
            <span className="stat-value">{percent.toFixed(0)}%</span>
          </div>
          <div className="stat-box">
            <span className="stat-label">Status</span>
            <span className="stat-value">✓</span>
          </div>
        </div>

        <button className="btn-back-home" onClick={() => navigate("/exams")}>
          Imtixonlarga qaytish
        </button>
      </div>
    </div>
  );
}

export default ExamDetail;
