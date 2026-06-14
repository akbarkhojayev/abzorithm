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
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [examCompleted, setExamCompleted] = useState(false);

  const [currentProblemIndex, setCurrentProblemIndex] = useState(0);
  const [submissions, setSubmissions] = useState({});
  const [submitting, setSubmitting] = useState(false);
  const [lastResult, setLastResult] = useState(null);

  const [timeLeft, setTimeLeft] = useState(null);
  const [codeFontSize, setCodeFontSize] = useState(() =>
    parseInt(localStorage.getItem("examCodeFontSize") || "14")
  );
  const [editorHeightPercent, setEditorHeightPercent] = useState(() =>
    parseFloat(localStorage.getItem("examEditorHeightPercent") || "60")
  );

  const [isResizingEditor, setIsResizingEditor] = useState(false);
  const editorRef = useRef(null);
  const panelRightRef = useRef(null);
  const dragRef = useRef({ startY: 0, startPercent: 0 });

  const currentQuestion = exam?.questions[currentProblemIndex];
  const currentProblem = currentQuestion?.problem_detail;
  const currentProblemId = currentQuestion?.problem;

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
          initialSubmissions[q.problem] = {
            code: saved || q.template_code || "",
            language: data.language || "python",
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
    localStorage.setItem("examCodeFontSize", codeFontSize.toString());
  }, [codeFontSize]);

  useEffect(() => {
    localStorage.setItem("examEditorHeightPercent", editorHeightPercent.toFixed(2));
  }, [editorHeightPercent]);

  useEffect(() => {
    if (currentProblemId) {
      const code = submissions[currentProblemId]?.code || "";
      localStorage.setItem(`exam_${examId}_problem_${currentProblemId}`, code);
    }
  }, [submissions, currentProblemId, examId]);

  // Timer
  useEffect(() => {
    if (!exam) return;
    const timer = setInterval(() => {
      const start = parseInt(localStorage.getItem(`exam_${examId}_start`) || Date.now());
      const elapsed = Math.floor((Date.now() - start) / 1000);
      const total = (exam.duration_minutes || 60) * 60;
      setTimeLeft(Math.max(0, total - elapsed));
    }, 1000);
    return () => clearInterval(timer);
  }, [exam, examId]);

  // Editor resize
  useEffect(() => {
    const handleMouseMove = (e) => {
      if (!isResizingEditor || !panelRightRef.current) return;
      const height = panelRightRef.current.clientHeight;
      const delta = e.clientY - dragRef.current.startY;
      const deltaPercent = (delta / height) * 100;
      const newPercent = Math.max(30, Math.min(70, dragRef.current.startPercent + deltaPercent));
      setEditorHeightPercent(newPercent);
    };

    const handleMouseUp = () => setIsResizingEditor(false);

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
  }, [isResizingEditor]);

  const formatTime = (seconds) => {
    if (!seconds && seconds !== 0) return "00:00";
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = seconds % 60;
    return h > 0
      ? `${h}:${m.toString().padStart(2, "0")}:${s.toString().padStart(2, "0")}`
      : `${m}:${s.toString().padStart(2, "0")}`;
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
      setLastResult({
        status: data.status || "error",
        message: data.message || "Xato",
      });
    } catch (err) {
      setLastResult({ status: "error", message: "Yuborish xatosi" });
    } finally {
      setSubmitting(false);
    }
  };

  const handleFinishExam = () => {
    if (confirm("Imtixonni tugatishga ishonchingiz komilmi?")) {
      navigate("/exams");
    }
  };

  if (loading) return <div className="exam-layout"><div className="loading-state">Yuklanmoqda...</div></div>;
  if (error && !exam) return <div className="exam-layout"><div className="error-state"><h2>{error}</h2></div></div>;
  if (examCompleted) return <div className="exam-layout"><div className="loading-state">Imtixon yakunlandi</div></div>;

  const timeColor = timeLeft < 300 ? '#c53030' : timeLeft < 600 ? '#f59e0b' : '#38a169';

  return (
    <div className="exam-layout">
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

      <main className="exam-main-area">
        {/* LEFT PANEL */}
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
            <div className="problem-tabs-nav">
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

            <div className="problem-nav-buttons">
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

        {/* RIGHT PANEL */}
        <div className="editor-panel" ref={panelRightRef}>
          <div className="editor-top" style={{ height: `${editorHeightPercent}%` }}>
            <div className="editor-toolbar">
              <div className="font-size-control">
                <button className="font-btn" onClick={() => setCodeFontSize(Math.max(12, codeFontSize - 1))}>−</button>
                <span className="font-display">{codeFontSize}</span>
                <button className="font-btn" onClick={() => setCodeFontSize(Math.min(22, codeFontSize + 1))}>+</button>
                {currentProblem?.template && (
                  <button className="reset-template-btn" onClick={() => {
                    setSubmissions(prev => ({
                      ...prev,
                      [currentProblemId]: {
                        ...prev[currentProblemId],
                        code: currentProblem.template
                      }
                    }));
                  }}>
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
                }}
              />
            </div>
          </div>

          <div
            className={`editor-divider ${isResizingEditor ? 'active' : ''}`}
            onMouseDown={(e) => {
              setIsResizingEditor(true);
              dragRef.current = { startY: e.clientY, startPercent: editorHeightPercent };
            }}
          />

          <div className="editor-bottom" style={{ height: `${100 - editorHeightPercent}%` }}>
            <div className="test-tabs">
              <button className="test-tab active">Natija</button>
            </div>

            <div className="test-content">
              {lastResult && (
                <div className="test-status-display">
                  <div className={`submission-status ${lastResult.status === 'Accepted' ? '' : 'error'}`}>
                    <div className="status-icon-block">
                      {lastResult.status === 'Accepted' ? <FaCheck className="status-check-icon" /> : <FaTimes className="status-error-icon" />}
                    </div>
                    <div className="status-text-block">
                      <h3>{lastResult.status === 'Accepted' ? 'To\'g\'ri!' : 'Xato'}</h3>
                      <p>{lastResult.message}</p>
                    </div>
                  </div>
                </div>
              )}
              {!lastResult && <div className="empty-results">Kod yuborib natijasini ko'ring</div>}
            </div>

            <div className="editor-bottom-actions">
              <button className="btn-submit" onClick={handleSubmit} disabled={submitting}>
                {submitting ? 'Yuborilmoqda...' : 'Yuborish'}
              </button>
              <button className="btn-finish" onClick={handleFinishExam}>Tugatish</button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default ExamDetail;
