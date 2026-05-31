import React, { useState, useEffect, useRef, useCallback } from "react";
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

  // UI State
  const [testCaseWatch, setTestCaseWatch] = useState(true);
  const [runTimeWatch, setRunTimeWatch] = useState(false);
  const [loaderRunTime, setLoaderRunTime] = useState(false);

  // Layout State - Percentage based for responsiveness
  const [panelRatio, setPanelRatio] = useState(() => {
    const saved = localStorage.getItem("panelRatio");
    return saved ? parseFloat(saved) : 0.35; // 35% default for left panel
  });

  const [editorRatio, setEditorRatio] = useState(() => {
    const saved = localStorage.getItem("editorRatio");
    return saved ? parseFloat(saved) : 0.5; // 50% default for editor
  });

  // Resize State
  const [isResizingPanels, setIsResizingPanels] = useState(false);
  const [isResizingEditor, setIsResizingEditor] = useState(false);

  // Refs
  const containerRef = useRef(null);
  const dragStartRef = useRef({ x: 0, y: 0, ratio: 0 });

  // Persist layout preferences
  useEffect(() => {
    localStorage.setItem("panelRatio", panelRatio.toFixed(2));
  }, [panelRatio]);

  useEffect(() => {
    localStorage.setItem("editorRatio", editorRatio.toFixed(2));
  }, [editorRatio]);

  // Handle vertical divider resize (left panel width)
  const handleMouseDownVertical = useCallback((e) => {
    setIsResizingPanels(true);
    dragStartRef.current = {
      x: e.clientX,
      ratio: panelRatio,
    };
  }, [panelRatio]);

  // Handle horizontal divider resize (editor height)
  const handleMouseDownHorizontal = useCallback((e) => {
    setIsResizingEditor(true);
    dragStartRef.current = {
      y: e.clientY,
      ratio: editorRatio,
    };
  }, [editorRatio]);

  // Global mouse move and up events
  useEffect(() => {
    if (!containerRef.current) return;

    const handleMouseMove = (e) => {
      if (!isResizingPanels && !isResizingEditor) return;

      if (isResizingPanels) {
        const container = containerRef.current;
        const rect = container.getBoundingClientRect();
        const delta = e.clientX - dragStartRef.current.x;
        const deltaRatio = delta / rect.width;
        const newRatio = dragStartRef.current.ratio + deltaRatio;

        // Constrain between 25% and 60%
        if (newRatio >= 0.25 && newRatio <= 0.6) {
          setPanelRatio(newRatio);
        }
      }

      if (isResizingEditor) {
        const container = containerRef.current;
        const rect = container.getBoundingClientRect();
        const delta = e.clientY - dragStartRef.current.y;
        const deltaRatio = delta / (rect.height / 2); // Only apply to right panel height
        const newRatio = dragStartRef.current.ratio + deltaRatio;

        // Constrain between 30% and 70%
        if (newRatio >= 0.3 && newRatio <= 0.7) {
          setEditorRatio(newRatio);
        }
      }
    };

    const handleMouseUp = () => {
      setIsResizingPanels(false);
      setIsResizingEditor(false);
    };

    if (isResizingPanels || isResizingEditor) {
      document.addEventListener("mousemove", handleMouseMove);
      document.addEventListener("mouseup", handleMouseUp);
      document.body.style.cursor = isResizingEditor ? "row-resize" : "col-resize";
      document.body.style.userSelect = "none";

      return () => {
        document.removeEventListener("mousemove", handleMouseMove);
        document.removeEventListener("mouseup", handleMouseUp);
        document.body.style.cursor = "auto";
        document.body.style.userSelect = "auto";
      };
    }
  }, [isResizingPanels, isResizingEditor]);

  if (error) {
    return (
      <div className="code-panels">
        <div className="error-container">
          <div className="error-message" role="alert">
            <span className="error-icon">❌</span>
            <p>{error}</p>
            <button onClick={() => window.location.reload()}>
              Qayta yukla
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Calculate pixel widths/heights from ratios
  const containerHeight = typeof window !== "undefined" ? window.innerHeight : 600;
  const editorHeight = containerHeight * editorRatio;
  const resultsHeight = containerHeight * (1 - editorRatio);

  return (
    <div className="code-panels">
      <div
        className="container"
        ref={containerRef}
        style={{
          gridTemplateColumns: `${panelRatio * 100}% 6px 1fr`,
          gridTemplateRows: `${editorHeight}px 6px ${resultsHeight}px`,
        }}
      >
        {/* ========== LEFT PANEL: PROBLEM DESCRIPTION ========== */}
        <div className="problem-panel">
          {loadingCoding ? (
            <div className="skeleton-loader" aria-busy="true">
              {[...Array(8)].map((_, i) => (
                <div key={i} className="skeleton-line" />
              ))}
            </div>
          ) : (
            <div className="problem-content">
              {/* Problem Header */}
              <div className="problem-header">
                <h1 className="problem-title">
                  <span className="problem-number">{index}</span>
                  <span>{details?.title}</span>
                </h1>

                <div className="problem-meta">
                  <span
                    className={`difficulty-badge difficulty-${
                      details?.difficulty?.toLowerCase() || "easy"
                    }`}
                  >
                    {details?.difficulty}
                  </span>
                </div>
              </div>

              {/* Problem Description */}
              {details?.description && (
                <div className="description-box">
                  <p>{details.description}</p>
                </div>
              )}

              {/* Examples */}
              {details?.examples && details.examples.length > 0 && (
                <div className="examples-section">
                  <h3 className="examples-title">Misollar</h3>
                  {details.examples.map((example, idx) => (
                    <div key={idx} className="example-item">
                      <div className="example-label">
                        Misol <span>{idx + 1}</span>
                      </div>
                      <div className="example-data">
                        <div className="example-input">
                          <strong>Input:</strong>
                          <code>{example?.ex_input}</code>
                        </div>
                        <div className="example-output">
                          <strong>Output:</strong>
                          <code>{example?.ex_output}</code>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>

        {/* ========== VERTICAL DIVIDER ========== */}
        <div
          className={`divider divider-vertical ${isResizingPanels ? "active" : ""}`}
          onMouseDown={handleMouseDownVertical}
          title="Kenglikni o'zgartirish uchun surish"
        />

        {/* ========== RIGHT PANEL: CODE EDITOR + RESULTS ========== */}
        <div className="right-panel">
          {/* CODE EDITOR SECTION */}
          <div className="editor-section">
            <div className="editor-wrapper">
              <CodeEditor
                codeBy={codeBy}
                setCodeBy={setCodeBy}
                profil={profil}
                setProfil={setProfil}
                setOutput={setOutput}
                setTestCaseWatch={setTestCaseWatch}
                setRunTimeWatch={setRunTimeWatch}
                setLoaderRunTime={setLoaderRunTime}
                problemId={details?.id}
              />
            </div>
          </div>

          {/* ========== HORIZONTAL DIVIDER ========== */}
          <div
            className={`divider divider-horizontal ${isResizingEditor ? "active" : ""}`}
            onMouseDown={handleMouseDownHorizontal}
            title="Balandligini o'zgartirish uchun surish"
          />

          {/* RESULTS SECTION */}
          <div className="results-section">
            {/* Tabs */}
            <div className="results-tabs">
              <button
                className={`tab ${testCaseWatch ? "active" : ""}`}
                onClick={() => {
                  setTestCaseWatch(true);
                  setRunTimeWatch(false);
                }}
                aria-selected={testCaseWatch}
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
              >
                <GiSandsOfTime className="tab-icon" />
                Natija
              </button>
            </div>

            {/* Test Cases Panel */}
            {testCaseWatch && (
              <div className="tab-content">
                <div className="test-cases-list">
                  {filteredCases && filteredCases.length > 0 ? (
                    filteredCases.map((testCase, idx) => (
                      <button
                        key={testCase.id}
                        className={`test-button ${
                          activeCaseId === testCase.id ? "active" : ""
                        }`}
                        onClick={() => changeTestCase(testCase.id)}
                      >
                        Test {idx + 1}
                      </button>
                    ))
                  ) : (
                    <div className="empty-state">Test case yoq</div>
                  )}
                </div>

                {activeCase && (
                  <div className="test-details">
                    <div className="test-item">
                      <label>Input:</label>
                      <code>{activeCase.input_data}</code>
                    </div>
                    <div className="test-item">
                      <label>Kutilgan Natija:</label>
                      <code>{activeCase.expected_output}</code>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Output Panel */}
            {runTimeWatch && (
              <div className="tab-content">
                {loaderRunTime ? (
                  <div className="output-loader">
                    <div className="spinner" />
                    <p>Yuborilmoqda...</p>
                  </div>
                ) : output && Object.keys(output).length > 0 ? (
                  <div className="output-result">
                    <div
                      className="result-status"
                      style={{ borderLeftColor: output.color || "#3b82f6" }}
                    >
                      <p className="status-text">
                        Status:{" "}
                        <strong style={{ color: output.color || "#3b82f6" }}>
                          {output.status || "Unknown"}
                        </strong>
                      </p>
                      <p className="execution-time">⏱ Vaqt: {output.time || "0"}s</p>
                    </div>

                    {output.failed_test && output.failed_test !== "-" && (
                      <div className="error-box">
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
                ) : (
                  <div className="empty-state">
                    📝 Kodni yuborish uchun "YUBORISH" tugmasini bosing
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
