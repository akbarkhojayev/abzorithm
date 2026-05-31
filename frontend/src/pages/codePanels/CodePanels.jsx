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

  // Layout state - percentage-based, zoom-safe
  const [leftWidthPercent, setLeftWidthPercent] = useState(() => {
    const saved = localStorage.getItem("leftWidthPercent");
    return saved ? parseFloat(saved) : 33; // Default: 33% for left panel
  });

  const [topHeightPercent, setTopHeightPercent] = useState(() => {
    const saved = localStorage.getItem("topHeightPercent");
    return saved ? parseFloat(saved) : 50; // Default: 50% for editor
  });

  const [isResizingVertical, setIsResizingVertical] = useState(false);
  const [isResizingHorizontal, setIsResizingHorizontal] = useState(false);

  const containerRef = useRef(null);
  const dragRef = useRef({ startX: 0, startY: 0, startWidth: 0, startHeight: 0 });

  // Save to localStorage
  useEffect(() => {
    localStorage.setItem("leftWidthPercent", leftWidthPercent.toFixed(2));
  }, [leftWidthPercent]);

  useEffect(() => {
    localStorage.setItem("topHeightPercent", topHeightPercent.toFixed(2));
  }, [topHeightPercent]);

  // Window resize handler - percentages are zoom-immune
  useEffect(() => {
    const handleWindowResize = () => {
      // With percentage-based layout, no action needed on window resize
      // Percentages automatically scale with zoom changes
    };

    window.addEventListener("resize", handleWindowResize);
    return () => window.removeEventListener("resize", handleWindowResize);
  }, []);

  // Vertical resize
  const handleMouseDownVertical = useCallback((e) => {
    setIsResizingVertical(true);
    dragRef.current = { startX: e.clientX, startPercent: leftWidthPercent };
  }, [leftWidthPercent]);

  // Horizontal resize
  const handleMouseDownHorizontal = useCallback((e) => {
    setIsResizingHorizontal(true);
    dragRef.current = { startY: e.clientY, startPercent: topHeightPercent };
  }, [topHeightPercent]);

  // Global mouse events - percentage-based
  useEffect(() => {
    const handleMouseMove = (e) => {
      if (isResizingVertical && containerRef.current) {
        const containerWidth = containerRef.current.clientWidth;
        const delta = e.clientX - dragRef.current.startX;
        const deltaPercent = (delta / containerWidth) * 100;
        const newPercent = dragRef.current.startPercent + deltaPercent;

        // Constraints: left panel between 20-70% of container
        const clampedPercent = Math.max(20, Math.min(newPercent, 70));
        setLeftWidthPercent(clampedPercent);
      }

      if (isResizingHorizontal && containerRef.current) {
        const panelTop = containerRef.current.querySelector(".panel-top");
        const panelRight = containerRef.current.querySelector(".panel-right");
        if (panelRight) {
          const containerHeight = panelRight.clientHeight;
          const delta = e.clientY - dragRef.current.startY;
          const deltaPercent = (delta / containerHeight) * 100;
          const newPercent = dragRef.current.startPercent + deltaPercent;

          // Constraints: editor between 30-70% of right panel
          const clampedPercent = Math.max(30, Math.min(newPercent, 70));
          setTopHeightPercent(clampedPercent);
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
        <div className="panel-left" style={{ width: `${leftWidthPercent}%` }}>
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
          <div className="panel-top" style={{ height: `${topHeightPercent}%` }}>
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
                      {/* Passed/Accepted State */}
                      {output.status === "Accepted" || output.status === "Passed" ? (
                        <div className="judge-result">
                          <div className="judge-header">
                            <div className="judge-status passed">
                              <span className="status-icon">✓</span>
                              <span className="status-text">To'g'ri javob</span>
                            </div>
                            <div className="judge-meta">
                              <span className="test-case">Barcha testlar o'tdi</span>
                              <span className="runtime">⏱ {output.time}s</span>
                            </div>
                          </div>
                          <div className="judge-celebration">
                            <p>🎉 Tabriklaymiz! Sizning yechimingiz to'g'ri!</p>
                          </div>
                        </div>
                      ) : (
                        <>
                      <div
                        className="status-box"
                        style={output.color ? { borderLeftColor: output.color } : {}}
                      >
                        <p>
                          Status: <strong style={{ color: output.color }}>
                            {output.status}
                          </strong>
                        </p>
                        <p>⏱ {output.time}s</p>
                      </div>

                      {output.failed_test && output.failed_test !== "-" && (
                        <div className="judge-result">
                          {/* Input Section */}
                          <div className="judge-section">
                            <div className="section-label">Input:</div>
                            <div className="section-code">
                              {output.error_input && output.error_input !== "-" && (
                                output.error_input
                              )}
                            </div>
                          </div>

                          {/* Your Output Section */}
                          <div className="judge-section">
                            <div className="section-label">Sizning natijangiz:</div>
                            <div className="section-code your-output">
                              {output.error_output && output.error_output !== "-" && (
                                output.error_output.includes("Got:")
                                  ? output.error_output.split("Got:")[1].trim()
                                  : output.error_output
                              )}
                            </div>
                          </div>

                          {/* Expected Output Section */}
                          <div className="judge-section">
                            <div className="section-label">Kutilgan natija:</div>
                            <div className="section-code expected-output">
                              {output.error_expected && output.error_expected !== "-" && (
                                output.error_expected
                              )}
                            </div>
                          </div>
                        </div>
                      )}
                      </>
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
