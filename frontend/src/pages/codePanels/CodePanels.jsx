import React, { useState, useEffect, useRef, useCallback } from "react";
import "./CodePanels.css";
import CodeEditor from "../../components/codeEditor/CodeEditor.jsx";
import AISolution from "../../components/aiSolution/AISolution.jsx";
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
  const [showAISolution, setShowAISolution] = useState(false);

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
                {/* Title Section */}
                <div className="problem-header">
                  <div className="title-wrapper">
                    <span className="problem-index">{index}</span>
                    <div className="title-content">
                      <h1>{details?.title}</h1>
                      {details?.difficulty && (
                        <span className={`badge badge-${details.difficulty.toLowerCase()}`}>
                          {details.difficulty}
                        </span>
                      )}
                    </div>
                  </div>
                </div>

                {/* Description */}
                {details?.description && (
                  <div className="section">
                    <h2 className="section-title">Tavsif</h2>
                    <p className="description-text">{details.description}</p>
                  </div>
                )}

                {/* Examples */}
                {details?.examples && details.examples.length > 0 && (
                  <div className="section">
                    <h2 className="section-title">Misollar</h2>
                    <div className="examples-grid">
                      {details.examples.map((ex, idx) => (
                        <div key={idx} className="example-box">
                          <div className="example-title">Misol {idx + 1}</div>
                          <div className="example-content">
                            <div className="example-item">
                              <div className="example-label">Kirish</div>
                              <pre className="example-code">{ex.ex_input}</pre>
                            </div>
                            <div className="example-item">
                              <div className="example-label">Chiqish</div>
                              <pre className="example-code">{ex.ex_output}</pre>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
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

          {/* BOTTOM: RESULTS PANEL */}
          <div className="panel-bottom">
            {/* Tab Navigation */}
            <div className="bottom-tabs">
              <button
                className={`tab-item ${testCaseWatch ? "active" : ""}`}
                onClick={() => {
                  setTestCaseWatch(true);
                  setRunTimeWatch(false);
                }}
              >
                <span className="tab-icon">📝</span>
                <span>Testlar</span>
              </button>
              <button
                className={`tab-item ${runTimeWatch ? "active" : ""}`}
                onClick={() => {
                  setRunTimeWatch(true);
                  setTestCaseWatch(false);
                }}
              >
                <span className="tab-icon">✓</span>
                <span>Natija</span>
              </button>
              <button
                className="tab-item ai-tab"
                onClick={() => setShowAISolution(true)}
                title="AI yordamchisidan yechim so'rab ko'ring"
              >
                <span className="tab-icon">✨</span>
                <span>AI Yechim</span>
              </button>
            </div>

            {/* Tab Content */}
            <div className="tab-content">
              {/* Tests Tab */}
              {testCaseWatch && (
                <div className="test-section">
                  <div className="test-list">
                    {filteredCases && filteredCases.length > 0 ? (
                      filteredCases.map((tc, idx) => (
                        <button
                          key={tc.id}
                          className={`test-item ${activeCaseId === tc.id ? "active" : ""}`}
                          onClick={() => changeTestCase(tc.id)}
                        >
                          <span className="test-number">Test {idx + 1}</span>
                        </button>
                      ))
                    ) : (
                      <div className="empty-state">Test mavjud emas</div>
                    )}
                  </div>

                  {activeCase && (
                    <div className="test-viewer">
                      <div className="test-content-block">
                        <div className="content-header">
                          <h3>Kirish</h3>
                        </div>
                        <pre className="content-code">{activeCase.input_data}</pre>
                      </div>

                      <div className="test-content-block">
                        <div className="content-header">
                          <h3>Kutilgan Natija</h3>
                        </div>
                        <pre className="content-code">{activeCase.expected_output}</pre>
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* Results Tab */}
              {runTimeWatch && (
                <div className="results-section">
                  {loaderRunTime ? (
                    <div className="loading-state">
                      <div className="spinner" />
                      <p>Natija tayyorlanmoqda...</p>
                    </div>
                  ) : output && Object.keys(output).length > 0 ? (
                    <div className="result-display">
                      {/* Success State */}
                      {(output.status === "Accepted" || output.status === "Passed") ? (
                        <div className="success-state">
                          <div className="success-header">
                            <div className="success-icon">✓</div>
                            <div className="success-text">
                              <h3>To'g'ri Javob!</h3>
                              <p>Barcha testlar muvaffaqiyatli o'tdi</p>
                            </div>
                          </div>
                          <div className="success-meta">
                            <div className="meta-item">
                              <span className="meta-label">Vaqt</span>
                              <span className="meta-value">{output.time}s</span>
                            </div>
                          </div>
                          <div className="success-celebration">
                            🎉 Tabriklaymiz! Sizning yechimingiz to'g'ri!
                          </div>
                        </div>
                      ) : (
                        <>
                          {/* Error State */}
                          <div className="error-state">
                            <div className="error-header">
                              <div className="error-icon">✗</div>
                              <div className="error-text">
                                <h3>Test Muvaffaq Olmadi</h3>
                                <p className="error-status">Status: {output.status}</p>
                              </div>
                            </div>
                            <div className="error-meta">
                              <span className="meta-value">{output.time}s</span>
                            </div>
                          </div>

                          {output.failed_test && output.failed_test !== "-" && (
                            <div className="comparison-view">
                              <div className="comparison-block input-block">
                                <div className="block-header">Kirish</div>
                                <pre className="block-content">
                                  {output.error_input && output.error_input !== "-"
                                    ? output.error_input
                                    : "-"}
                                </pre>
                              </div>

                              <div className="comparison-row">
                                <div className="comparison-block wrong-block">
                                  <div className="block-header">Sizning Natijangiz</div>
                                  <pre className="block-content">
                                    {output.error_output && output.error_output !== "-"
                                      ? output.error_output.includes("Got:")
                                        ? output.error_output.split("Got:")[1].trim()
                                        : output.error_output
                                      : "-"}
                                  </pre>
                                </div>

                                <div className="comparison-block correct-block">
                                  <div className="block-header">Kutilgan Natija</div>
                                  <pre className="block-content">
                                    {output.error_expected &&
                                    output.error_expected !== "-"
                                      ? output.error_expected
                                      : "-"}
                                  </pre>
                                </div>
                              </div>
                            </div>
                          )}
                        </>
                      )}
                    </div>
                  ) : (
                    <div className="empty-state">Kod yuborib natijani ko'ring</div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* AI Solution Modal */}
      <AISolution
        problemId={details?.id}
        problemTitle={details?.title}
        isOpen={showAISolution}
        onClose={() => setShowAISolution(false)}
      />
    </div>
  );
}

export default CodePanels;
