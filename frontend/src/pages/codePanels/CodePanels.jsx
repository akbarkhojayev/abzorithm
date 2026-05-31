import React, { useState, useEffect, useRef } from "react";
import "./CodePanels.css";
import { FaNoteSticky } from "react-icons/fa6";
import { GiSandsOfTime } from "react-icons/gi";
import CodeEditor from "../../components/codeEditor/CodeEditor.jsx";
import { useCodePanel } from "../../hooks/useCodePanel.js";

function CodePanels({ profil, setProfil, setProblemData }) {
  const {
    details,
    index,
    codeBy,
    setCodeBy,
    activeCaseId,
    changeTestCase,
    activeCase,
    filteredCases,
    output,
    setOutput,
    loadingCoding,
    error,
  } = useCodePanel();

  const [testCaseWatch, setTestCaseWatch] = useState(true);
  const [runTimeWatch, setRunTimeWatch] = useState(false);
  const [loaderRunTime, setLoaderRunTime] = useState(false);
  const [problemWidth, setProblemWidth] = useState(() => {
    const saved = localStorage.getItem("problemPanelWidth");
    if (saved) return parseInt(saved);
    // 40% of window width
    return Math.max(250, window.innerWidth * 0.4);
  });
  const [isResizingProblem, setIsResizingProblem] = useState(false);
  const [editorHeight, setEditorHeight] = useState(() => {
    const saved = localStorage.getItem("editorPanelHeight");
    if (saved) return parseInt(saved);
    // 50% of available height
    return Math.max(150, window.innerHeight * 0.5 - 50);
  });
  const [isResizingEditor, setIsResizingEditor] = useState(false);
  const dragStartRef = useRef({ x: 0, y: 0, width: 0, height: 0 });
  const containerRef = useRef(null);
  const rightPanelRef = useRef(null);

  useEffect(() => {
    localStorage.setItem("problemPanelWidth", problemWidth.toString());
  }, [problemWidth]);

  useEffect(() => {
    localStorage.setItem("editorPanelHeight", editorHeight.toString());
  }, [editorHeight]);

  useEffect(() => {
    const handleWindowResize = () => {
      // Adjust editor height based on viewport height
      setEditorHeight((prev) => {
        const newHeight = Math.max(150, window.innerHeight * 0.5 - 50);
        return newHeight;
      });

      // Adjust problem width based on viewport width
      setProblemWidth((prev) => {
        const newWidth = Math.max(250, window.innerWidth * 0.4);
        return newWidth;
      });
    };

    window.addEventListener("resize", handleWindowResize);
    return () => window.removeEventListener("resize", handleWindowResize);
  }, []);

  const handleMouseDownProblem = (e) => {
    dragStartRef.current = { x: e.clientX, y: 0, width: problemWidth, height: 0 };
    setIsResizingProblem(true);
    e.preventDefault();
  };

  const handleMouseDownEditor = (e) => {
    dragStartRef.current = { x: 0, y: e.clientY, width: 0, height: editorHeight };
    setIsResizingEditor(true);
    e.preventDefault();
  };

  useEffect(() => {
    const handleMouseMove = (e) => {
      const { x, y, width, height } = dragStartRef.current;

      if (isResizingProblem) {
        const delta = e.clientX - x;
        const newWidth = width + delta;
        if (newWidth > 250 && newWidth < 1400) {
          setProblemWidth(newWidth);
        }
      }

      if (isResizingEditor) {
        const delta = e.clientY - y;
        const newHeight = height + delta;
        if (newHeight > 150 && newHeight < 700) {
          setEditorHeight(newHeight);
        }
      }
    };

    const handleMouseUp = () => {
      setIsResizingProblem(false);
      setIsResizingEditor(false);
    };

    if (isResizingProblem || isResizingEditor) {
      document.addEventListener("mousemove", handleMouseMove);
      document.addEventListener("mouseup", handleMouseUp);
      document.body.style.cursor = isResizingEditor ? "row-resize" : "col-resize";
      document.body.style.userSelect = "none";
    }

    return () => {
      document.removeEventListener("mousemove", handleMouseMove);
      document.removeEventListener("mouseup", handleMouseUp);
      document.body.style.cursor = "auto";
      document.body.style.userSelect = "auto";
    };
  }, [isResizingProblem, isResizingEditor]);

  if (error) {
    return (
      <div className="code-panels">
        <div className="container">
          <div className="error-message" role="alert">
            <p>❌ {error}</p>
            <button onClick={() => window.location.reload()}>
              Qayta yukla
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="code-panels">
      <div
        className="container"
        ref={containerRef}
        style={{
          gridTemplateColumns: `${problemWidth}px 8px 1fr`
        }}
      >
        {/* Problem Description */}
        <div className="problem-description">
          {loadingCoding ? (
            <div className="skeleton-loader" aria-busy="true">
              {[...Array(7)].map((_, i) => (
                <div key={i} className="skeleton-line"></div>
              ))}
            </div>
          ) : (
            <div className="problem-content">
              <h1 className="problem-title">
                <span className="problem-number">{index}.</span> {details?.title}
              </h1>

              <div className="problem-meta">
                <span
                  className={`difficulty-badge difficulty-${
                    details?.difficulty?.toLowerCase() || "easy"
                  }`}
                  aria-label={`Qiyinlik darajasi: ${details?.difficulty}`}
                >
                  {details?.difficulty}
                </span>
              </div>

              <p className="problem-description-text">{details?.description}</p>

              {details?.examples && details.examples.length > 0 && (
                <div className="examples-section">
                  {details.examples.map((example, idx) => (
                    <div key={idx} className="example-block">
                      <h3>
                        Misol <span className="example-number">{idx + 1}</span>
                      </h3>
                      <div className="example-content">
                        <p>
                          <strong>Input:</strong>
                          <code>{example?.ex_input}</code>
                        </p>
                        <p>
                          <strong>Output:</strong>
                          <code>{example?.ex_output}</code>
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>

        {/* Divider */}
        <div
          className={`resize-divider ${isResizingProblem ? "active" : ""}`}
          onMouseDown={handleMouseDownProblem}
          title="Dragging yo'li bilan o'lchamini o'zgartiring"
        >
          <span className="resize-handle"></span>
        </div>

        {/* Right Panel - Code Editor + Results */}
        <div
          className="right-panel"
          ref={rightPanelRef}
        >
          {/* Code Editor Section */}
          <div
            className="code-editor-wrapper"
            style={{ height: `${editorHeight}px` }}
          >
            <div className="editor-wrapper">
              <CodeEditor
                codeBy={codeBy}
                setCodeBy={setCodeBy}
                profil={profil}
                setProfil={setProfil}
                setOutput={setOutput}
                setRunTimeWatch={setRunTimeWatch}
                setTestCaseWatch={setTestCaseWatch}
                setLoaderRunTime={setLoaderRunTime}
                problemId={details?.id}
              />
            </div>
          </div>

          {/* Horizontal Divider */}
          <div
            className={`resize-divider horizontal ${isResizingEditor ? "active" : ""}`}
            onMouseDown={handleMouseDownEditor}
            title="Dragging yo'li bilan o'lchamini o'zgartiring"
          >
            <span className="resize-handle"></span>
          </div>

          {/* Test Results Panel */}
          <div className="results-panel">
            <div className="results-tabs">
              <button
                className={`tab ${testCaseWatch ? "active" : ""}`}
                onClick={() => {
                  setTestCaseWatch(true);
                  setRunTimeWatch(false);
                }}
                aria-selected={testCaseWatch}
                role="tab"
              >
                <FaNoteSticky className="tab-icon" />
                Test Cases
              </button>
              <button
                className={`tab ${runTimeWatch ? "active" : ""}`}
                onClick={() => {
                  setRunTimeWatch(true);
                  setTestCaseWatch(false);
                }}
                aria-selected={runTimeWatch}
                role="tab"
              >
                <GiSandsOfTime className="tab-icon" />
                Natija
              </button>
            </div>

            {/* Test Cases Panel */}
            {testCaseWatch && (
              <div className="test-cases-panel" role="tabpanel">
                <div className="test-cases-list">
                  {filteredCases.length > 0 ? (
                    filteredCases.map((testCase, idx) => (
                      <button
                        key={testCase.id}
                        className={`test-case-button ${
                          activeCaseId === testCase.id ? "active" : ""
                        }`}
                        onClick={() => changeTestCase(testCase.id)}
                        aria-pressed={activeCaseId === testCase.id}
                      >
                        Test {idx + 1}
                      </button>
                    ))
                  ) : (
                    <div className="empty-state">Test case yoq</div>
                  )}
                </div>

                {activeCase && (
                  <div className="test-case-details">
                    <div className="test-detail">
                      <strong>Input:</strong>
                      <code>{activeCase.input_data}</code>
                    </div>
                    <div className="test-detail">
                      <strong>Kutilgan Natija:</strong>
                      <code>{activeCase.expected_output}</code>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Output Panel */}
            {runTimeWatch && (
              <div className="output-panel" role="tabpanel">
                {loaderRunTime ? (
                  <div className="output-loader" aria-busy="true">
                    <div className="spinner"></div>
                    <p>Yuborilmoqda...</p>
                  </div>
                ) : output.length === 0 ? (
                  <div className="empty-output">
                    <p>📝 Kodni yuborish uchun yuqoridagi "Yuborish" tugmasini bosing</p>
                  </div>
                ) : (
                  <div className="output-result">
                    <div
                      className="result-status"
                      style={{ borderLeft: `4px solid ${output.color}` }}
                    >
                      <p className="status-text">
                        Status: <strong style={{ color: output.color }}>
                          {output.status}
                        </strong>
                      </p>
                      <p className="execution-time">⏱ Vaqt: {output.time}s</p>
                    </div>

                    {output.failed_test && output.failed_test !== "-" && (
                      <div className="error-details">
                        <p>❌ Xato test: {output.failed_test}</p>
                        {output.error_input && output.error_input !== "-" && (
                          <p>📥 Input: <code>{output.error_input}</code></p>
                        )}
                        {output.error_expected &&
                          output.error_expected !== "-" && (
                            <p>✓ Kutilgan: <code>{output.error_expected}</code></p>
                          )}
                        {output.error_output &&
                          output.error_output !== "-" && (
                            <p>❌ Olingan: <code>{output.error_output}</code></p>
                          )}
                      </div>
                    )}
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

export default CodePanels;
