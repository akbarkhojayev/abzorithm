import React, { useEffect, useState, useRef } from "react";
import "./ExamDetail.css";
import { baseUrl } from "../services/config.js";
import { getToken } from "../services/token.js";
import { useParams, useNavigate } from "react-router-dom";
import { useTheme } from "../../context/ThemeContext";
import Editor from "@monaco-editor/react";
import { FaClock, FaCheck, FaTimes, FaChevronRight, FaChevronLeft, FaSync, FaCode, FaMoon, FaSun } from "react-icons/fa";

function ExamDetail() {
  const { examId } = useParams();
  const navigate = useNavigate();
  const { isDark } = useTheme();

  const [exam, setExam] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [currentProblemIndex, setCurrentProblemIndex] = useState(0);
  const [submissions, setSubmissions] = useState({});
  const [submitting, setSubmitting] = useState(false);
  const [lastResult, setLastResult] = useState(null);
  const [solvedProblems, setSolvedProblems] = useState(() => {
    const saved = localStorage.getItem(`exam_${examId}_solved`);
    return saved ? new Set(JSON.parse(saved)) : new Set();
  });

  const [timeLeft, setTimeLeft] = useState(null);
  const [codeFontSize, setCodeFontSize] = useState(() =>
    parseInt(localStorage.getItem("examCodeFontSize") || "14")
  );
  const [leftPanelWidthPercent, setLeftPanelWidthPercent] = useState(() =>
    parseFloat(localStorage.getItem("examLeftPanelWidth") || "35")
  );

  const [isResizingVertical, setIsResizingVertical] = useState(false);
  const containerRef = useRef(null);
  const editorRef = useRef(null);
  const dragRef = useRef({ startX: 0, startPercent: 0 });

  const currentQuestion = exam?.questions[currentProblemIndex];
  const currentProblem = currentQuestion?.problem_detail;
  const currentProblemId = currentQuestion?.problem;
  const isSolved = solvedProblems.has(currentProblemId);

  useEffect(() => {
    const loadExam = async () => {
      try {
        const response = await fetch(`${baseUrl}/exams/${examId}/`, {
          headers: { Authorization: `Bearer ${getToken()}` },
        });

        if (!response.ok) throw new Error("Imtixon yuklanmadi");

        const data = await response.json();
        setExam(data);

        const initialSubmissions = {};
        data.questions.forEach(q => {
          const saved = localStorage.getItem(`exam_${examId}_problem_${q.problem}`);
          const template = q.template_code || "";
          initialSubmissions[q.problem] = {
            code: saved || template,
            language: data.language || "python",
          };
        });
        setSubmissions(initialSubmissions);

        const savedIndex = localStorage.getItem(`exam_${examId}_currentIndex`);
        if (savedIndex) {
          setCurrentProblemIndex(parseInt(savedIndex));
        }
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
    localStorage.setItem("examCodeFontSize", codeFontSize.toString());
  }, [codeFontSize]);

  useEffect(() => {
    localStorage.setItem("examLeftPanelWidth", leftPanelWidthPercent.toFixed(2));
  }, [leftPanelWidthPercent]);

  useEffect(() => {
    if (currentProblemId) {
      const code = submissions[currentProblemId]?.code || "";
      localStorage.setItem(`exam_${examId}_problem_${currentProblemId}`, code);
    }
  }, [submissions, currentProblemId, examId]);

  useEffect(() => {
    localStorage.setItem(`exam_${examId}_solved`, JSON.stringify(Array.from(solvedProblems)));
  }, [solvedProblems, examId]);

  useEffect(() => {
    localStorage.setItem(`exam_${examId}_currentIndex`, currentProblemIndex.toString());
  }, [currentProblemIndex, examId]);

  useEffect(() => {
    if (!exam) return;

    const startKey = `exam_${examId}_start`;
    const startTime = localStorage.getItem(startKey);

    if (!startTime) {
      localStorage.setItem(startKey, Date.now().toString());
    }

    const timer = setInterval(() => {
      const start = parseInt(localStorage.getItem(startKey) || Date.now());
      const elapsed = Math.floor((Date.now() - start) / 1000);
      const total = (exam.duration_minutes || 60) * 60;
      const remaining = Math.max(0, total - elapsed);

      setTimeLeft(remaining);

      if (remaining === 0) {
        clearInterval(timer);
        handleAutoFinish();
      }
    }, 1000);

    return () => clearInterval(timer);
  }, [exam, examId]);

  useEffect(() => {
    const handleMouseMove = (e) => {
      if (isResizingVertical && containerRef.current) {
        const containerWidth = containerRef.current.clientWidth;
        const delta = e.clientX - dragRef.current.startX;
        const deltaPercent = (delta / containerWidth) * 100;
        const newPercent = dragRef.current.startPercent + deltaPercent;
        const clampedPercent = Math.max(20, Math.min(newPercent, 70));
        setLeftPanelWidthPercent(clampedPercent);
      }
    };

    const handleMouseUp = () => setIsResizingVertical(false);

    if (isResizingVertical) {
      document.addEventListener("mousemove", handleMouseMove);
      document.addEventListener("mouseup", handleMouseUp);
      document.body.style.cursor = "col-resize";
      document.body.style.userSelect = "none";
      return () => {
        document.removeEventListener("mousemove", handleMouseMove);
        document.removeEventListener("mouseup", handleMouseUp);
        document.body.style.cursor = "auto";
        document.body.style.userSelect = "auto";
      };
    }
  }, [isResizingVertical]);

  const formatTime = (seconds) => {
    if (!seconds && seconds !== 0) return "00:00";
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = seconds % 60;
    return h > 0
      ? `${h}:${m.toString().padStart(2, "0")}:${s.toString().padStart(2, "0")}`
      : `${m}:${s.toString().padStart(2, "0")}`;
  };

  const resetTemplate = () => {
    if (currentQuestion?.template_code) {
      if (confirm("Kod template-ga qaytarish kerakmi?")) {
        setSubmissions(prev => ({
          ...prev,
          [currentProblemId]: {
            ...prev[currentProblemId],
            code: currentQuestion.template_code
          }
        }));
      }
    }
  };

  const formatCode = () => {
    if (editorRef.current) {
      editorRef.current.getAction('editor.action.formatDocument')?.run();
    }
  };

  const undoCode = () => {
    if (editorRef.current) {
      editorRef.current.trigger('keyboard', 'undo', null);
    }
  };

  const redoCode = () => {
    if (editorRef.current) {
      editorRef.current.trigger('keyboard', 'redo', null);
    }
  };

  const handleSubmit = async () => {
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
      const status = data.status || "error";

      setLastResult({
        status,
        message: data.message || "Xato",
      });

      if (status === "Accepted" || status === "Passed") {
        setSolvedProblems(prev => new Set([...prev, currentProblemId]));
      }
    } catch (err) {
      setLastResult({ status: "error", message: "Yuborish xatosi" });
    } finally {
      setSubmitting(false);
    }
  };

  const handleAutoFinish = async () => {
    try {
      await fetch(`${baseUrl}/exams/${examId}/complete/`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${getToken()}`,
          "Content-Type": "application/json",
        },
      });
    } catch (err) {
      console.error("Auto-finish error:", err);
    }
    navigate("/exams");
  };

  const handleFinishExam = () => {
    if (confirm("Imtixonni tugatishga ishonchingiz komilmi?")) {
      handleAutoFinish();
    }
  };

  if (loading) return <div className="exam-layout"><div className="loading-state">Yuklanmoqda...</div></div>;
  if (error && !exam) return <div className="exam-layout"><div className="error-state"><h2>{error}</h2></div></div>;

  const timeColor = timeLeft < 300 ? '#c53030' : timeLeft < 600 ? '#f59e0b' : '#38a169';

  return (
    <div className="exam-layout">
      {/* HEADER */}
      <header className="exam-header">
        {/* Top Bar */}
        <div className="header-top">
          <div className="header-left">
            <h1 className="exam-title">{exam?.title}</h1>
            <span className="exam-lang">{exam?.language?.toUpperCase()}</span>
          </div>

          <div className="header-right">
            <div className={`timer ${timeLeft < 300 ? 'critical' : ''}`} style={{ color: timeColor }}>
              <FaClock />
              <span>{formatTime(timeLeft)}</span>
            </div>
            <button
              onClick={handleSubmit}
              disabled={submitting || timeLeft === 0}
              className="btn-submit"
              title={timeLeft === 0 ? "Vaqt tugadi" : "Kodni yuborish"}
            >
              {submitting ? "Yuborilmoqda..." : timeLeft === 0 ? "Vaqt tugadi" : "Yuborish"}
            </button>
            <button
              onClick={handleFinishExam}
              className="btn-finish"
              title="Imtixonni tugatish"
            >
              Tugatish
            </button>
          </div>
        </div>

        {/* Bottom Navigation Bar */}
        <div className="header-bottom">
          <div className="problem-nav">
            <button
              onClick={() => setCurrentProblemIndex(Math.max(0, currentProblemIndex - 1))}
              disabled={currentProblemIndex === 0}
              className="nav-btn"
              title="Oldingi masala"
            >
              <FaChevronLeft />
            </button>

            <div className="problem-tabs">
              {exam?.questions?.map((q, idx) => {
                const problemSolved = solvedProblems.has(q.problem);
                return (
                  <button
                    key={q.id}
                    onClick={() => setCurrentProblemIndex(idx)}
                    className={`problem-tab ${idx === currentProblemIndex ? 'active' : ''} ${problemSolved ? 'solved' : ''}`}
                    title={q.problem_detail?.title}
                  >
                    {idx + 1}
                    {problemSolved && <FaCheck className="tab-check" />}
                  </button>
                );
              })}
            </div>

            <button
              onClick={() => setCurrentProblemIndex(Math.min(exam.questions.length - 1, currentProblemIndex + 1))}
              disabled={currentProblemIndex === exam.questions.length - 1}
              className="nav-btn"
              title="Keyingi masala"
            >
              <FaChevronRight />
            </button>
          </div>
        </div>
      </header>

      {/* MAIN AREA */}
      <main className="exam-main-area" ref={containerRef}>
        {/* PROBLEM PANEL */}
        <div className="problem-panel" style={{ width: `${leftPanelWidthPercent}%` }}>
          <div className="problem-scroll">
            <div className="problem-heading">
              <div className="problem-header">
                <span className="problem-num">{currentProblemIndex + 1}</span>
                <h2>{currentProblem?.title}</h2>
              </div>
              {currentProblem?.difficulty && (
                <span className={`badge-difficulty badge-${currentProblem.difficulty.toLowerCase()}`}>
                  {currentProblem.difficulty}
                </span>
              )}
            </div>

            {currentProblem?.description && (
              <div className="problem-section">
                <h3>Tavsif</h3>
                <p>{currentProblem.description}</p>
              </div>
            )}

            {currentProblem?.input_example && (
              <div className="problem-section">
                <h3>Kirish Misoli</h3>
                <pre className="code-block">{currentProblem.input_example}</pre>
              </div>
            )}

            {currentProblem?.output_example && (
              <div className="problem-section">
                <h3>Chiqish Misoli</h3>
                <pre className="code-block">{currentProblem.output_example}</pre>
              </div>
            )}
          </div>
        </div>

        {/* DIVIDER */}
        <div
          className={`exam-divider ${isResizingVertical ? "active" : ""}`}
          onMouseDown={(e) => {
            setIsResizingVertical(true);
            dragRef.current = { startX: e.clientX, startPercent: leftPanelWidthPercent };
          }}
        />

        {/* EDITOR PANEL */}
        <div className="editor-panel" style={{ width: `${100 - leftPanelWidthPercent}%` }}>
          <div className="editor-toolbar">
            <div className="toolbar-section">
              <button
                onClick={undoCode}
                className="toolbar-btn"
                title="Orqaga qaytarish (Ctrl+Z)"
              >
                ↶
              </button>
              <button
                onClick={redoCode}
                className="toolbar-btn"
                title="Oldinga qaytarish (Ctrl+Y)"
              >
                ↷
              </button>
              <div className="toolbar-divider" />
              <button
                onClick={formatCode}
                className="toolbar-btn"
                title="Kodni formatlash (Shift+Alt+F)"
              >
                <FaCode />
              </button>
              <div className="toolbar-divider" />
              {currentQuestion?.template_code && (
                <button
                  onClick={resetTemplate}
                  className="toolbar-btn"
                  title="Template-ga qaytarish"
                >
                  <FaSync />
                </button>
              )}
            </div>

            <div className="toolbar-section">
              <div className="font-controls">
                <button
                  onClick={() => setCodeFontSize(Math.max(12, codeFontSize - 1))}
                  className="font-btn"
                  title="Shrift o'lchamini kamaytirish"
                >
                  −
                </button>
                <span className="font-size">{codeFontSize}px</span>
                <button
                  onClick={() => setCodeFontSize(Math.min(22, codeFontSize + 1))}
                  className="font-btn"
                  title="Shrift o'lchamini oshirish"
                >
                  +
                </button>
              </div>
            </div>

            <div className="toolbar-section">
              <span className="lang-badge">{exam?.language?.toUpperCase()}</span>
            </div>
          </div>

          <Editor
            height="100%"
            language={exam?.language === 'javascript' ? 'javascript' : exam?.language === 'dart' ? 'dart' : 'python'}
            value={submissions[currentProblemId]?.code || ""}
            onChange={(value) => setSubmissions(prev => ({
              ...prev,
              [currentProblemId]: { ...prev[currentProblemId], code: value || "" }
            }))}
            onMount={(editor) => (editorRef.current = editor)}
            theme={isDark ? "vs-dark" : "vs-light"}
            options={{
              fontSize: codeFontSize,
              minimap: { enabled: false },
              wordWrap: 'on',
              scrollBeyondLastLine: false,
              automaticLayout: true,
              formatOnPaste: true,
              formatOnType: true,
            }}
          />

          {lastResult && (
            <div className={`result-popup ${lastResult.status === 'Accepted' || lastResult.status === 'Passed' ? 'success' : 'error'}`}>
              <div className="result-icon">
                {lastResult.status === 'Accepted' || lastResult.status === 'Passed' ? <FaCheck /> : <FaTimes />}
              </div>
              <div className="result-text">
                <strong>{lastResult.status === 'Accepted' || lastResult.status === 'Passed' ? 'To\'g\'ri!' : 'Xato'}</strong>
                <p>{lastResult.message}</p>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default ExamDetail;
