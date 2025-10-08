import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import CodeMirror from '@uiw/react-codemirror';
import { python } from '@codemirror/lang-python';
import { api } from '../services/api';
import './ProblemSolverPage.css';

function ProblemSolverPage() {
  const { slug } = useParams();
  const navigate = useNavigate();
  const [problem, setProblem] = useState(null);
  const [code, setCode] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [testCases, setTestCases] = useState([]);
  const [activeTab, setActiveTab] = useState('testcase');
  const [descriptionTab, setDescriptionTab] = useState('description');
  const [leftWidth, setLeftWidth] = useState(50);
  const [testHeight, setTestHeight] = useState(250);
  const [fontSize, setFontSize] = useState(14);
  const [originalCode, setOriginalCode] = useState('');

  useEffect(() => {
    loadProblem();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [slug]);

  const increaseFontSize = () => {
    if (fontSize < 24) {
      setFontSize(fontSize + 2);
    }
  };

  const decreaseFontSize = () => {
    if (fontSize > 10) {
      setFontSize(fontSize - 2);
    }
  };

  const resetCode = () => {
    setCode(originalCode);
    setResult(null);
    setActiveTab('testcase');
  };

  const loadProblem = async () => {
    try {
      // First get the problem by slug
      const problemData = await api.getProblem(slug);
      
      // Then use the problem ID for template and test cases
      const [template, testCasesData, userData] = await Promise.all([
        api.getTemplate(problemData.id),
        api.getTestCases(problemData.id),
        api.getCurrentUser()
      ]);
      
      console.log('Problem Slug:', slug);
      console.log('Problem ID:', problemData.id);
      console.log('Test Cases:', testCasesData);
      console.log('Test Cases Count:', testCasesData.length);
      
      // Filter test cases for this problem only
      const filteredTestCases = testCasesData.filter(tc => tc.problem === problemData.id);
      console.log('Filtered Test Cases:', filteredTestCases);
      
      setProblem(problemData);
      setCode(template.template_code || '');
      setOriginalCode(template.template_code || '');
      setTestCases(filteredTestCases);
      
      // Update score display
      const scoreEl = document.getElementById('user-score-solver');
      if (scoreEl && userData) {
        scoreEl.textContent = userData.score || 0;
      }
    } catch (error) {
      console.error('Failed to load problem:', error);
    }
  };

  // Horizontal resizer (left-right)
  const handleHorizontalResize = (e) => {
    const startX = e.clientX;
    const startWidth = leftWidth;

    const onMouseMove = (e) => {
      const containerWidth = window.innerWidth;
      const deltaX = e.clientX - startX;
      const newWidth = startWidth + (deltaX / containerWidth) * 100;
      
      if (newWidth > 30 && newWidth < 70) {
        setLeftWidth(newWidth);
      }
    };

    const onMouseUp = () => {
      document.removeEventListener('mousemove', onMouseMove);
      document.removeEventListener('mouseup', onMouseUp);
      document.body.style.cursor = '';
    };

    document.addEventListener('mousemove', onMouseMove);
    document.addEventListener('mouseup', onMouseUp);
    document.body.style.cursor = 'col-resize';
  };

  // Vertical resizer (top-bottom for test section)
  const handleVerticalResize = (e) => {
    const startY = e.clientY;
    const startHeight = testHeight;

    const onMouseMove = (e) => {
      const deltaY = startY - e.clientY;
      const newHeight = startHeight + deltaY;
      
      if (newHeight > 150 && newHeight < 600) {
        setTestHeight(newHeight);
      }
    };

    const onMouseUp = () => {
      document.removeEventListener('mousemove', onMouseMove);
      document.removeEventListener('mouseup', onMouseUp);
      document.body.style.cursor = '';
    };

    document.addEventListener('mousemove', onMouseMove);
    document.addEventListener('mouseup', onMouseUp);
    document.body.style.cursor = 'row-resize';
  };

  const formatCode = () => {
    if (!code.trim()) return;
    
    // Simple Python code formatter
    const lines = code.split('\n');
    let formatted = [];
    let indentLevel = 0;
    
    for (let line of lines) {
      const trimmed = line.trim();
      
      // Decrease indent for closing statements
      if (trimmed.startsWith('return') || trimmed.startsWith('break') || trimmed.startsWith('continue')) {
        // Keep current indent
      } else if (indentLevel > 0 && !trimmed.startsWith('#') && trimmed && !line.startsWith(' ')) {
        indentLevel = Math.max(0, indentLevel - 1);
      }
      
      // Add formatted line
      if (trimmed) {
        formatted.push('    '.repeat(indentLevel) + trimmed);
        
        // Increase indent after colons
        if (trimmed.endsWith(':')) {
          indentLevel++;
        }
      } else {
        formatted.push('');
      }
    }
    
    setCode(formatted.join('\n'));
  };

  const handleSubmit = async () => {
    if (!code.trim()) {
      // Don't show alert, just switch to result tab with message
      setResult({ status: 'Error', message: 'Please write some code!' });
      setActiveTab('result');
      return;
    }

    setLoading(true);
    setResult(null);
    
    try {
      const res = await api.submitCode({ 
        problem: problem.id, 
        code: code 
      });
      setResult(res);
      
      // Update score if submission was successful
      if (res.user_score) {
        const scoreEl = document.getElementById('user-score-solver');
        if (scoreEl) {
          scoreEl.textContent = res.user_score;
        }
      }
      
      // Switch to result tab (no alert)
      setActiveTab('result');
    } catch (error) {
      console.error('Submission error:', error);
      setResult({ 
        status: 'Error', 
        message: error.response?.data?.detail || error.message || 'Submission failed'
      });
      setActiveTab('result');
    } finally {
      setLoading(false);
    }
  };

  if (!problem) return <div className="loading">Loading...</div>;

  return (
    <div className="solver-page">
      <nav className="navbar solver-navbar">
        <div className="nav-left">
          <button onClick={() => navigate('/problems')} className="btn-back">
            <i className="fas fa-chevron-left"></i>
          </button>
          <div className="nav-brand">
            <i className="fas fa-code brand-icon"></i>
            <span className="brand-text">Abzorithm</span>
          </div>
        </div>
        <div className="nav-right">
          <div className="user-score">
            <i className="fas fa-star"></i>
            <span id="user-score-solver">0</span>
          </div>
        </div>
      </nav>

      <div className="solver-layout">
        <div className="problem-panel" style={{ width: `${leftWidth}%` }}>
          {/* Problem Tabs */}
          <div className="problem-tabs">
            <button 
              className={`problem-tab ${descriptionTab === 'description' ? 'active' : ''}`}
              onClick={() => setDescriptionTab('description')}
            >
              <i className="fas fa-file-alt"></i>
              Description
            </button>
            <button 
              className={`problem-tab ${descriptionTab === 'editorial' ? 'active' : ''}`}
              onClick={() => setDescriptionTab('editorial')}
            >
              <i className="fas fa-book"></i>
              Editorial
            </button>
            <button 
              className={`problem-tab ${descriptionTab === 'submissions' ? 'active' : ''}`}
              onClick={() => setDescriptionTab('submissions')}
            >
              <i className="fas fa-history"></i>
              Submissions
            </button>
          </div>

          <div className="problem-content">
            {descriptionTab === 'description' && (
              <>
                <div className="problem-header-section">
                  <h1 className="problem-main-title">{problem.title}</h1>
                  <div className="problem-meta">
                    <span className={`difficulty-pill ${problem.difficulty}`}>
                      <i className="fas fa-signal"></i>
                      {problem.difficulty}
                    </span>
                  </div>
                </div>

            <div className="problem-section">
              <div className="section-header">
                <i className="fas fa-file-alt"></i>
                <h3>Description</h3>
              </div>
              <div className="section-content">
                <p>{problem.description}</p>
              </div>
            </div>

            <div className="problem-section">
              <div className="section-header">
                <i className="fas fa-lightbulb"></i>
                <h3>Example</h3>
              </div>
              <div className="section-content">
                <div className="example-box">
                  <div className="example-item">
                    <span className="example-label">Input:</span>
                    <code className="example-code">{problem.input_example}</code>
                  </div>
                  <div className="example-item">
                    <span className="example-label">Output:</span>
                    <code className="example-code">{problem.output_example}</code>
                  </div>
                </div>
              </div>
            </div>
              </>
            )}

            {descriptionTab === 'editorial' && (
              <div className="empty-state">
                <i className="fas fa-book"></i>
                <p>Editorial coming soon...</p>
              </div>
            )}

            {descriptionTab === 'submissions' && (
              <div className="empty-state">
                <i className="fas fa-history"></i>
                <p>Your submissions will appear here</p>
              </div>
            )}
          </div>
        </div>

        <div 
          className="horizontal-resizer" 
          onMouseDown={handleHorizontalResize}
        />

        <div className="editor-panel" style={{ width: `${100 - leftWidth}%` }}>
          <div className="editor-header">
            <div className="editor-tabs">
              <div className="editor-tab active">
                <i className="fab fa-python"></i> Python
              </div>
            </div>
            <div className="editor-actions">
              <div className="font-size-controls">
                <button 
                  onClick={decreaseFontSize}
                  className="btn-font-size"
                  title="Decrease Font Size"
                  disabled={fontSize <= 10}
                >
                  <i className="fas fa-minus"></i>
                </button>
                <span className="font-size-display">{fontSize}px</span>
                <button 
                  onClick={increaseFontSize}
                  className="btn-font-size"
                  title="Increase Font Size"
                  disabled={fontSize >= 24}
                >
                  <i className="fas fa-plus"></i>
                </button>
                <button 
                  onClick={resetCode}
                  className="btn-reset"
                  title="Reset Code to Template"
                >
                  <i className="fas fa-undo"></i>
                </button>
              </div>
              <button 
                onClick={formatCode}
                className="btn-format"
                title="Format Code (Shift+Alt+F)"
              >
                <i className="fas fa-magic"></i>
                <span>Format</span>
              </button>
            </div>
          </div>
          
          <div style={{ '--editor-font-size': `${fontSize}px`, flex: 1, display: 'flex', flexDirection: 'column' }}>
          <CodeMirror
            value={code}
            height="100%"
            theme="dark"
            extensions={[python()]}
            onChange={(value) => setCode(value)}
            className="code-mirror-editor"
            basicSetup={{
              lineNumbers: true,
              highlightActiveLineGutter: true,
              highlightSpecialChars: true,
              foldGutter: true,
              drawSelection: true,
              dropCursor: true,
              allowMultipleSelections: true,
              indentOnInput: true,
              bracketMatching: true,
              closeBrackets: true,
              autocompletion: true,
              rectangularSelection: true,
              crosshairCursor: true,
              highlightActiveLine: true,
              highlightSelectionMatches: true,
              closeBracketsKeymap: true,
              searchKeymap: true,
              foldKeymap: true,
              completionKeymap: true,
              lintKeymap: true,
            }}
          />
          </div>

          <div 
            className="vertical-resizer" 
            onMouseDown={handleVerticalResize}
          />

          {/* Test Cases / Results Section */}
          <div className="test-section" style={{ height: `${testHeight}px` }}>
            <div className="test-header">
              <div className="test-tabs">
                <button 
                  className={`test-tab ${activeTab === 'testcase' ? 'active' : ''}`}
                  onClick={() => setActiveTab('testcase')}
                >
                  Testcase
                </button>
                <button 
                  className={`test-tab ${activeTab === 'result' ? 'active' : ''}`}
                  onClick={() => setActiveTab('result')}
                >
                  Result
                </button>
              </div>
              <button 
                onClick={handleSubmit} 
                disabled={loading}
                className="btn-run-main"
              >
                {loading ? (
                  <>
                    <i className="fas fa-spinner fa-spin"></i>
                    <span>Running...</span>
                  </>
                ) : (
                  <>
                    <i className="fas fa-play"></i>
                    <span>Run Code</span>
                  </>
                )}
              </button>
            </div>

            <div className="test-content">
              {activeTab === 'testcase' && (
                <div className="test-cases">
                  {testCases.length === 0 ? (
                    <div className="no-data">No test cases available</div>
                  ) : (
                    testCases.map((tc, index) => (
                      <div key={tc.id} className="test-case">
                        <div className="test-case-title">Test Case {index + 1}</div>
                        <div className="test-case-content">
                          <div className="test-case-label">Input:</div>
                          <div className="test-case-value">{tc.input_data}</div>
                          <div className="test-case-label">Expected Output:</div>
                          <div className="test-case-value">{tc.expected_output}</div>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              )}

              {activeTab === 'result' && (
                <div className="results">
                  {!result ? (
                    <div className="no-data">Run your code to see results</div>
                  ) : (
                    <div className={`result ${result.status === 'Accepted' ? 'success' : 'error'}`}>
                      <div><strong>Status:</strong> {result.status}</div>
                      
                      {result.message && (
                        <div><strong>Message:</strong> {result.message}</div>
                      )}
                      
                      {result.execution_time && (
                        <div><strong>Time:</strong> {result.execution_time}ms</div>
                      )}
                      
                      {result.status !== 'Accepted' && result.status !== 'Error' && (
                        <>
                          {result.failed_test && (
                            <div><strong>Failed Test:</strong> {result.failed_test}</div>
                          )}
                          {result.error_input && (
                            <div><strong>Input:</strong> {result.error_input}</div>
                          )}
                          {result.error_output && (
                            <div><strong>Your Output:</strong> {result.error_output}</div>
                          )}
                          {result.error_expected && (
                            <div><strong>Expected:</strong> {result.error_expected}</div>
                          )}
                        </>
                      )}
                      
                      {result.status === 'Accepted' && (
                        <div style={{textAlign: 'center', padding: '1rem'}}>
                          <div style={{fontSize: '3rem'}}>🎉</div>
                          <div><strong>Score:</strong> {result.user_score}</div>
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
    </div>
  );
}

export default ProblemSolverPage;
