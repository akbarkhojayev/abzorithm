import React, { useEffect, useRef, useState, useCallback } from "react";
import Editor from "@monaco-editor/react";
import { getMasala, getProfilMe } from "../../pages/services/app.js";
import { getToken } from "../../pages/services/token.js";
import { baseUrl } from "../../pages/services/config.js";
import { FiRotateCcw, FiRotateCw, FiRefreshCw } from "react-icons/fi";
import { SiPython, SiJavascript, SiDart } from "react-icons/si";
import { useTheme } from "../../context/ThemeContext.jsx";
import "./CodeEditor.css";

const LANGUAGES = ["python", "javascript", "dart"];

const getLanguageIcon = (lang) => {
  switch (lang) {
    case "python":
      return <SiPython />;
    case "javascript":
      return <SiJavascript />;
    case "dart":
      return <SiDart />;
    default:
      return null;
  }
};

function formatSubmissionOutput(response) {
  const status = (response.status || "").toLowerCase();
  const colorMap = {
    accepted: "green",
    wrong: "red",
    runtime: "orange",
    "time limit": "purple",
  };

  let color = "gray";
  for (const [key, val] of Object.entries(colorMap)) {
    if (status.includes(key)) {
      color = val;
      break;
    }
  }

  return {
    id: response.id,
    status: response.status,
    color,
    time: Math.floor((response.execution_time || 0) * 1000) / 1000,
    failed_test: response.failed_test ?? "-",
    error_input: response.error_input ?? "-",
    error_expected: response.error_expected ?? "-",
    error_output: response.error_output ?? "-",
  };
}

function CodeEditor({
  codeBy,
  setCodeBy,
  profil,
  setProfil,
  problemId,
  setOutput,
  setRunTimeWatch,
  setTestCaseWatch,
  setLoaderRunTime,
}) {
  const { isDark } = useTheme();
  const [language, setLanguage] = useState(() => {
    if (typeof window === "undefined") return "python";
    try {
      const saved = localStorage.getItem("editorLanguage");
      return saved || "python";
    } catch {
      return "python";
    }
  });
  const [isSelectionOpen, setIsSelectionOpen] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [fontSize, setFontSize] = useState(() => {
    try {
      return Number(localStorage.getItem("editorFontSize")) || 14;
    } catch {
      return 14;
    }
  });
  const optionRef = useRef(null);
  const editorRef = useRef(null);

  const loadTemplate = useCallback(async (lang) => {
    if (!problemId) return;
    try {
      const res = await getMasala(problemId, lang);
      if (!res) {
        throw new Error("Template yuklanishi uchun xatolik");
      }
      setCodeBy(res);
    } catch (err) {
      console.error("Template loading error:", err);
    }
  }, [problemId, setCodeBy]);

  // Load profile when problem changes
  useEffect(() => {
    if (!problemId) return;

    getProfilMe()
      ?.then(setProfil)
      .catch((err) => console.error("Failed to load profile:", err));
  }, [problemId, setProfil]);

  // Load template when problemId OR language changes
  useEffect(() => {
    if (!problemId || !language) return;
    loadTemplate(language);
  }, [problemId, language, loadTemplate]);

  // Save language preference to localStorage whenever it changes
  useEffect(() => {
    try {
      localStorage.setItem("editorLanguage", language);
    } catch {
      console.error("Failed to save language preference");
    }
  }, [language]);

  // Save font size preference to localStorage
  useEffect(() => {
    try {
      localStorage.setItem("editorFontSize", fontSize.toString());
    } catch {
      console.error("Failed to save font size preference");
    }
  }, [fontSize]);

  const submitCode = useCallback(async () => {
    if (!codeBy?.template_code || isSubmitting) return;

    setIsSubmitting(true);
    setLoaderRunTime(true);

    try {
      const response = await fetch(`${baseUrl}/submissions/create/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${getToken()}`,
        },
        body: JSON.stringify({
          user: profil?.id,
          problem: problemId,
          code: codeBy.template_code,
          language,
        }),
      });

      if (!response.ok) {
        throw new Error(`Server xatosi: ${response.status}`);
      }

      const res = await response.json();
      const formattedOutput = formatSubmissionOutput(res);
      setOutput(formattedOutput);
      setRunTimeWatch(true);
      setTestCaseWatch(false);
    } catch (err) {
      console.error("Submission error:", err);
      setOutput({
        status: "Xatolik",
        color: "red",
        error_output: err.message || "Kodni yuborish uchun xatolik yuz berdi",
      });
      setRunTimeWatch(true);
      setTestCaseWatch(false);
    } finally {
      setIsSubmitting(false);
      setLoaderRunTime(false);
    }
  }, [
    codeBy,
    isSubmitting,
    profil?.id,
    problemId,
    language,
    setOutput,
    setRunTimeWatch,
    setTestCaseWatch,
    setLoaderRunTime,
  ]);

  // Dropdown o'chirish click outside bilan
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (optionRef.current && !optionRef.current.contains(e.target)) {
        setIsSelectionOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleLanguageChange = (lang) => {
    setLanguage(lang);
    setIsSelectionOpen(false);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    submitCode();
  };

  const undoCode = useCallback(() => {
    if (!editorRef.current) return;
    editorRef.current.trigger("keyboard", "undo", null);
  }, []);

  const redoCode = useCallback(() => {
    if (!editorRef.current) return;
    editorRef.current.trigger("keyboard", "redo", null);
  }, []);

  const resetCode = useCallback(() => {
    loadTemplate(language);
  }, [language, loadTemplate]);

  return (
    <div className="code-editor">
      <div className="editor-controls">
        <div className="control-group">
          <div ref={optionRef} className="language-selector">
            <button
              className={`language-button ${isSelectionOpen ? "open" : ""}`}
              onClick={() => setIsSelectionOpen(!isSelectionOpen)}
              aria-label="Til tanglash"
              aria-expanded={isSelectionOpen}
              aria-haspopup="listbox"
            >
              <span className="language-icon">{getLanguageIcon(language)}</span>
              {language}
              <span className="arrow-icon" />
            </button>

            {isSelectionOpen && (
              <div className="language-options" role="listbox">
                {LANGUAGES.map((lang) => (
                  <button
                    key={lang}
                    className={`language-option ${
                      language === lang ? "active" : ""
                    }`}
                    onClick={() => handleLanguageChange(lang)}
                    role="option"
                    aria-selected={language === lang}
                  >
                    <span className="language-icon">{getLanguageIcon(lang)}</span>
                    {lang}
                  </button>
                ))}
              </div>
            )}
          </div>

          <button
            className="submit-btn"
            onClick={handleSubmit}
            disabled={isSubmitting || !codeBy?.template_code}
            aria-label="Kodni yuborish (Ctrl+Enter)"
            title="Kodni yuborish"
          >
            {isSubmitting ? "Yuborilmoqda..." : "Yuborish"}
          </button>

          <button
            onClick={resetCode}
            className="reset-btn"
            title="Kodni qayta boshlash"
            aria-label="Kodni qayta boshlash"
          >
            <FiRefreshCw />
          </button>
        </div>

        <div className="action-buttons">
          <button
            onClick={undoCode}
            className="action-btn"
            title="Orqaga qaytarish"
            aria-label="Orqaga qaytarish"
          >
            <FiRotateCcw />
          </button>

          <button
            onClick={redoCode}
            className="action-btn"
            title="Oldinga qaytarish"
            aria-label="Oldinga qaytarish"
          >
            <FiRotateCw />
          </button>

          <div className="font-size-control">
            <select
              id="font-size-select"
              value={fontSize}
              onChange={(e) => setFontSize(Number(e.target.value))}
              className="font-size-select"
              title="Kod o'lchami"
              aria-label="Kod o'lchami"
            >
              <option value={12}>12px</option>
              <option value={14}>14px</option>
              <option value={16}>16px</option>
              <option value={18}>18px</option>
              <option value={20}>20px</option>
            </select>
          </div>
        </div>
      </div>

      <Editor
        width="100%"
        height="400px"
        language={language}
        theme={isDark ? "darkCustomTheme" : "lightCustomTheme"}
        beforeMount={(monaco) => {
          // Light theme
          monaco.editor.defineTheme("lightCustomTheme", {
            base: "vs",
            inherit: false,
            rules: [
              { token: "keyword", foreground: "#ff3300ff" },
              { token: "string", foreground: "#137613ff" },
              { token: "comment", foreground: "#aaaaaaff", fontStyle: "italic" },
            ],
            colors: {
              "editor.background": "#FAF8F8",
              "editor.foreground": "#1b31bdff",
              "editor.lineNumbersBackground": "#FAF8F8",
              "editor.lineNumbersForeground": "#999999",
              "editorCursor.foreground": "#1b31bd",
              "editor.selectionBackground": "#e0e0ff",
            },
          });

          // Dark theme
          monaco.editor.defineTheme("darkCustomTheme", {
            base: "vs-dark",
            inherit: false,
            rules: [
              { token: "keyword", foreground: "#ff6b6b" },
              { token: "string", foreground: "#51cf66" },
              { token: "comment", foreground: "#909090", fontStyle: "italic" },
              { token: "number", foreground: "#ffd666" },
              { token: "variable", foreground: "#a8d8ff" },
            ],
            colors: {
              "editor.background": "#1a1f3a",
              "editor.foreground": "#e2e8f0",
              "editor.lineNumbersBackground": "#252d45",
              "editor.lineNumbersForeground": "#9ca3af",
              "editorCursor.foreground": "#3b82f6",
              "editor.selectionBackground": "#374151",
              "editor.lineHighlightBackground": "#252d45",
              "editorWhitespace.foreground": "#4b5563",
            },
          });
        }}
        onMount={(editor) => (editorRef.current = editor)}
        value={codeBy?.template_code || ""}
        onChange={(value) =>
          setCodeBy((prev) => ({ ...prev, template_code: value || "" }))
        }
        options={{
          minimap: { enabled: false },
          fontSize: fontSize,
          wordWrap: "on",
          scrollBeyondLastLine: false,
          automaticLayout: true,
        }}
      />
    </div>
  );
}

export default CodeEditor;
