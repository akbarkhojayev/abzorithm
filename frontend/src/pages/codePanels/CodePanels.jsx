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

  const [testCaseWatch, setTestCaseWatch] = useState(true);
  const [runTimeWatch, setRunTimeWatch] = useState(false);
  const [loaderRunTime, setLoaderRunTime] = useState(false);

  // Layout state - using pixel values that respond to window resize
  const [leftWidth, setLeftWidth] = useState(() => {
    const saved = localStorage.getItem("leftWidth");
    if (saved) return parseInt(saved);
    return Math.max(300, Math.min(window.innerWidth * 0.35, 600));
  });

  const [topHeight, setTopHeight] = useState(() => {
    const saved = localStorage.getItem("topHeight");
    if (saved) return parseInt(saved);
    return Math.max(200, Math.min(window.innerHeight * 0.5, 700));
  });

  const [isResizingVertical, setIsResizingVertical] = useState(false);
  const [isResizingHorizontal, setIsResizingHorizontal] = useState(false);

  const containerRef = useRef(null);
  const dragRef = useRef({ startX: 0, startY: 0, startWidth: 0, startHeight: 0 });

  // Save to localStorage
  useEffect(() => {
    localStorage.setItem("leftWidth", leftWidth);
  }, [leftWidth]);

  useEffect(() => {
    localStorage.setItem("topHeight", topHeight);
  }, [topHeight]);

  // Window resize handler
  useEffect(() => {
    const handleWindowResize = () => {
      // Recalculate sizes as percentage of new window
      setLeftWidth((prev) => {
        const ratio = prev / window.innerWidth;
        return Math.max(300, Math.min(window.innerWidth * Math.min(ratio, 0.6), 900));
      });

      setTopHeight((prev) => {
        const ratio = prev / window.innerHeight;
        return Math.max(200, Math.min(window.innerHeight * Math.min(ratio, 0.7), 900));
      });
    };

    window.addEventListener("resize", handleWindowResize);
    return () => window.removeEventListener("resize", handleWindowResize);
  }, []);

  // Vertical resize
  const handleMouseDownVertical = useCallback((e) => {
    setIsResizingVertical(true);
    dragRef.current = { startX: e.clientX, startWidth: leftWidth };
  }, [leftWidth]);

  // Horizontal resize
  const handleMouseDownHorizontal = useCallback((e) => {
    setIsResizingHorizontal(true);
    dragRef.current = { startY: e.clientY, startHeight: topHeight };
  }, [topHeight]);

  // Global mouse events
  useEffect(() => {
    const handleMouseMove = (e) => {
      if (isResizingVertical) {
        const delta = e.clientX - dragRef.current.startX;
        const newWidth = dragRef.current.startWidth + delta;
        if (newWidth >= 250 && newWidth <= 900) {
          setLeftWidth(newWidth);
        }
      }

      if (isResizingHorizontal) {
        const delta = e.clientY - dragRef.current.startY;
        const newHeight = dragRef.current.startHeight + delta;
        if (newHeight >= 150 && newHeight <= 900) {
          setTopHeight(newHeight);
        }
      }
    };

    const handleMouseUp = () => {
      setIsResizingVertical(false);
      setIsResizingHorizontal(false);
    };

    if (isResizingVertical || isResizingHorizontal) {
      document.addEventListener("mousemove", handleMouseMove);
      document.addEventListener("mouseup", handleMouseUp);
      document.body.style.cursor = isResizingHorizontal ? "row-resize" : "col-resize";
      document.body.style.userSelect = "none";

      return () => {
        document.removeEventListener("mousemove", handleMouseMove);
        document.removeEventListener("mouseup", handleMouseUp);
        document.body.style.cursor = "auto";
        document.body.style.userSelect = "auto";
      };
    }
  }, [isResizingVertical, isResizingHorizontal]);

  if (error) {
    return (
      <div className="app-error">
        <div className="error-box">
          <p>{error}</p>
          <button onClick={() => window.location.reload()}>Qayta yukla</button>
        </div>
      </div>
    );
  }

  return (
    <div className="app-root">
      <div className="app-container" ref={containerRef}>
        {/* LEFT PANEL - PROBLEM DESCRIPTION */}
        <div className="panel-left" style={{ width: `${leftWidth}px` }}>
          {loadingCoding ? (
            <div className="skeleton-container">
              {[...Array(10)].map((_, i) => (
                <div key={i} className="skeleton-line" />
              ))}
            </div>
          ) : (
            <div className="problem-scroll">
              <div className="problem-inner">
                {/* Title */}
                <div className="problem-header">
                  <h1>
                    <span className="problem-index">{index}</span>
                    {details?.title}
                  </h1>
                  {details?.difficulty && (
                    <span className={`badge badge-${details.difficulty.toLowerCase()}`}>
                      {details.difficulty}
                    </span>
                  )}
                </div>

                {/* Description */}
                {details?.description && (
                  <div className="section">
                    <h2>Tavsif</h2>
                    <p>{details.description}</p>
                  </div>
                )}

                {/* Examples */}
                {details?.examples && details.examples.length > 0 && (
                  <div className="section">
                    <h2>Misollar</h2>
                    {details.examples.map((ex, idx) => (
                      <div key={idx} className="example-box">
                        <h3>Misol {idx + 1}</h3>
                        <div className="example-row">
                          <div>
                            <strong>Kirish:</strong>
                            <pre>{ex.ex_input}</pre>
                          </div>
                          <div>
                            <strong>Chiqish:</strong>
                            <pre>{ex.ex_output}</pre>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        {/* VERTICAL DIVIDER */}
        <div
          className={`divider-v ${isResizingVertical ? "active" : ""}`}
          onMouseDown={handleMouseDownVertical}
        />

        {/* RIGHT PANEL */}
        <div className="panel-right">
          {/* TOP: CODE EDITOR */}
          <div className="panel-top" style={{ height: `${topHeight}px` }}>
            <div className="editor-container">
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

          {/* HORIZONTAL DIVIDER */}
          <div
            className={`divider-h ${isResizingHorizontal ? "active" : ""}`}
            onMouseDown={handleMouseDownHorizontal}
          />

          {/* BOTTOM: RESULTS */}
          <div className="panel-bottom">
            {/* Tabs */}
            <div className="tabs">
              <button
                className={`tab ${testCaseWatch ? "active" : ""}`}
                onClick={() => {
                  setTestCaseWatch(true);
                  setRunTimeWatch(false);
                }}
              >
                <FaNoteSticky />
                Test Cases
              </button>
              <button
                className={`tab ${runTimeWatch ? "active" : ""}`}
                onClick={() => {
                  setRunTimeWatch(true);
                  setTestCaseWatch(false);
                }}
              >
                <GiSandsOfTime />
                Natija
              </button>
            </div>

            {/* Content */}
            <div className="results-content">
              {testCaseWatch && (
                <div className="test-panel">
                  <div className="test-buttons">
                    {filteredCases && filteredCases.length > 0 ? (
                      filteredCases.map((tc, idx) => (
                        <button
                          key={tc.id}
                          className={`test-btn ${activeCaseId === tc.id ? "active" : ""}`}
                          onClick={() => changeTestCase(tc.id)}
                        >
                          Test {idx + 1}
                        </button>
                      ))
                    ) : (
                      <div className="empty">Test yoq</div>
                    )}
                  </div>

                  {activeCase && (
                    <div className="test-details">
                      <div className="test-row">
                        <strong>Input:</strong>
                        <code>{activeCase.input_data}</code>
                      </div>
                      <div className="test-row">
                        <strong>Expected:</strong>
                        <code>{activeCase.expected_output}</code>
                      </div>
                    </div>
                  )}
                </div>
              )}

              {runTimeWatch && (
                <div className="output-panel">
                  {loaderRunTime ? (
                    <div className="loading">
                      <div className="spinner" />
                      <p>Yuborilmoqda...</p>
                    </div>
                  ) : output && Object.keys(output).length > 0 ? (
                    <div className="output-content">
                      <div
                        className="status-box"
                        style={{ borderLeftColor: output.color || "#3b82f6" }}
                      >
                        <p>
                          Status: <strong style={{ color: output.color }}>
                            {output.status}
                          </strong>
                        </p>
                        <p>⏱ {output.time}s</p>
                      </div>

                      {output.failed_test && output.failed_test !== "-" && (
                        <div className="error-box">
                          <div className="error-title">
                            <p>❌ {output.failed_test}</p>
                          </div>
                          <div className="error-details">
                            {output.error_input && output.error_input !== "-" && (
                              <div className="error-row">
                                <span className="error-label">Kirish:</span>
                                <span className="error-value">{output.error_input}</span>
                              </div>
                            )}
                            {output.error_expected && output.error_expected !== "-" && (
                              <div className="error-row">
                                <span className="error-label">Kutilgan:</span>
                                <span className="error-value">{output.error_expected}</span>
                              </div>
                            )}
                            {output.error_output && output.error_output !== "-" && (
                              <div className="error-row">
                                <span className="error-label">Asl natija:</span>
                                <span className="error-value error-wrong">{output.error_output}</span>
                              </div>
                            )}
                          </div>
                        </div>
                      )}
                    </div>
                  ) : (
                    <div className="empty">Kod yuboring</div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default CodePanels;
