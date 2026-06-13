import React, { useState } from "react";
import "./AISolution.css";
import { X } from "lucide-react";

export default function AISolution({ problemId, problemTitle, isOpen, onClose }) {
  const [solution, setSolution] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchAISolution = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(
        `http://localhost:8001/problems/${problemId}/ai-solution/`
      );
      if (!response.ok) throw new Error("AI yechim yuklashda xatolik");
      const data = await response.json();
      setSolution(data);
    } catch (err) {
      setError(err.message || "Xatolik yuz berdi");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="ai-solution-overlay" onClick={onClose}>
      <div className="ai-solution-modal" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="ai-header">
          <h2 className="ai-title">AI Yechim: {problemTitle}</h2>
          <button className="ai-close-btn" onClick={onClose} title="Yopish">
            <X size={20} />
          </button>
        </div>

        {/* Content */}
        <div className="ai-body">
          {!solution ? (
            <>
              {loading ? (
                <div className="ai-loading-state">
                  <div className="ai-spinner"></div>
                  <p className="ai-loading-text">AI yechim tayyorlanmoqda...</p>
                  <small className="ai-loading-hint">Bir necha soniya kutib turing</small>
                </div>
              ) : error ? (
                <div className="ai-error-state">
                  <p className="ai-error-text">{error}</p>
                  <button className="ai-retry-btn" onClick={fetchAISolution}>
                    Qayta urinish
                  </button>
                </div>
              ) : (
                <div className="ai-empty-state">
                  <div className="ai-empty-icon-box">
                    <div className="ai-icon-graphic"></div>
                  </div>
                  <h3 className="ai-empty-title">Masalani Tahlil Qilish</h3>
                  <p className="ai-empty-desc">
                    Ushbu masala uchun to'liq yechim va batafsil tushuntirishni olish uchun tugmani bosing.
                  </p>
                  <button className="ai-ask-btn" onClick={fetchAISolution}>
                    Get Solution
                  </button>
                </div>
              )}
            </>
          ) : (
            <div className="ai-solution-text">
              <FormattedText text={solution.full_response} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function FormattedText({ text }) {
  const lines = text.split('\n');
  const elements = [];
  let codeBlock = null;
  let codeLines = [];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Code block detection
    if (line.includes('```')) {
      if (codeBlock === null) {
        codeBlock = true;
        codeLines = [];
      } else {
        elements.push(
          <pre key={`code-${elements.length}`} className="ai-code-block">
            <code>{codeLines.join('\n')}</code>
          </pre>
        );
        codeBlock = null;
        codeLines = [];
      }
      continue;
    }

    if (codeBlock) {
      codeLines.push(line);
      continue;
    }

    // Headers
    if (line.startsWith('###')) {
      elements.push(
        <h3 key={`h3-${elements.length}`} className="ai-h3">
          {line.replace(/^###\s+/, '')}
        </h3>
      );
      continue;
    }

    if (line.startsWith('##')) {
      elements.push(
        <h2 key={`h2-${elements.length}`} className="ai-h2">
          {line.replace(/^##\s+/, '')}
        </h2>
      );
      continue;
    }

    if (line.startsWith('#')) {
      elements.push(
        <h1 key={`h1-${elements.length}`} className="ai-h1">
          {line.replace(/^#\s+/, '')}
        </h1>
      );
      continue;
    }

    // Divider
    if (line.match(/^-{3,}$/)) {
      elements.push(<div key={`hr-${elements.length}`} className="ai-divider" />);
      continue;
    }

    // Empty lines
    if (!line.trim()) {
      elements.push(<div key={`space-${elements.length}`} className="ai-space" />);
      continue;
    }

    // Regular text
    if (line.trim()) {
      elements.push(
        <p key={`p-${elements.length}`} className="ai-p">
          {line}
        </p>
      );
    }
  }

  return <div className="ai-formatted">{elements}</div>;
}
