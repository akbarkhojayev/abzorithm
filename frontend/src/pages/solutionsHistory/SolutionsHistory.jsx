import React, { useEffect, useState } from "react";
import "./SolutionsHistory.css";
import { baseUrl } from "../services/config.js";
import { getToken } from "../services/token.js";
import { FaList, FaCheckCircle, FaTimesCircle } from "react-icons/fa";

function SolutionsHistory() {
  const [submissions, setSubmissions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [filter, setFilter] = useState("all");

  useEffect(() => {
    fetchSubmissions();
  }, []);

  const fetchSubmissions = () => {
    setLoading(true);
    const token = getToken();

    fetch(`${baseUrl}/submissions/`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to fetch submissions");
        }
        return res.json();
      })
      .then((data) => {
        const sortedData = Array.isArray(data)
          ? data.sort(
              (a, b) =>
                new Date(b.submitted_at) - new Date(a.submitted_at)
            )
          : [];
        setSubmissions(sortedData);
      })
      .catch((error) => {
        console.error("Error:", error);
        setSubmissions([]);
      })
      .finally(() => setLoading(false));
  };

  const getStatusBadge = (status) => {
    const statusClass = status
      ?.toLowerCase()
      .replace(/\s+/g, "-");
    return (
      <span className={`status-badge status-${statusClass}`}>
        {status}
      </span>
    );
  };

  const getDifficultyBadge = (difficulty) => {
    return (
      <span className={`difficulty-badge difficulty-${difficulty?.toLowerCase()}`}>
        {difficulty}
      </span>
    );
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString("uz-UZ", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  const filteredSubmissions =
    filter === "all"
      ? submissions
      : submissions.filter(
          (sub) =>
            sub.status?.toLowerCase().replace(/\s+/g, "-") === filter
        );

  return (
    <div className="solutions-history">
      <div className="container">
        <div className="history-header">
          <div>
            <h1>Yechimlar Tarixi</h1>
            <p>Barcha yuborilgan yechimlar</p>
          </div>
          <div className="history-stats">
            <div className="stat-card">
              <span className="stat-value">{submissions.length}</span>
              <span className="stat-label">Jami Yechim</span>
            </div>
            <div className="stat-card">
              <span className="stat-value">
                {submissions.filter((s) => s.status === "Accepted").length}
              </span>
              <span className="stat-label">Qabul Qilingan</span>
            </div>
          </div>
        </div>

        <div className="history-filters">
          <button
            className={`filter-btn ${filter === "all" ? "active" : ""}`}
            onClick={() => setFilter("all")}
          >
            Hamasi ({submissions.length})
          </button>
          <button
            className={`filter-btn ${filter === "accepted" ? "active" : ""}`}
            onClick={() => setFilter("accepted")}
          >
            Qabul ({submissions.filter((s) => s.status === "Accepted").length})
          </button>
          <button
            className={`filter-btn ${filter === "wrong-answer" ? "active" : ""}`}
            onClick={() => setFilter("wrong-answer")}
          >
            Xato ({submissions.filter((s) => s.status === "Wrong Answer").length})
          </button>
        </div>

        {loading ? (
          <div className="history-loader">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="history-loader-row"></div>
            ))}
          </div>
        ) : filteredSubmissions.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon"><FaList /></div>
            <h2>Hali yechim yo'q</h2>
            <p>Masalalarni yechib, yechimlar tarixini to'ldiring</p>
          </div>
        ) : (
          <div className="history-table">
            <div className="table-header">
              <div className="col-problem">Masala</div>
              <div className="col-status">Status</div>
              <div className="col-difficulty">Qiyinlik</div>
              <div className="col-time">Vaqt</div>
              <div className="col-execution">Bajarish Vaqti</div>
            </div>

            <div className="table-body">
              {filteredSubmissions.map((sub) => (
                <div key={sub.id} className="table-row">
                  <div className="col-problem">
                    <div className="problem-title">
                      {sub.problem_title || `Problem #${sub.problem}`}
                    </div>
                    <div className="problem-language">
                      {sub.language?.toUpperCase()}
                    </div>
                  </div>
                  <div className="col-status">
                    {getStatusBadge(sub.status)}
                  </div>
                  <div className="col-difficulty">
                    {getDifficultyBadge(sub.difficulty)}
                  </div>
                  <div className="col-time">
                    {formatDate(sub.submitted_at)}
                  </div>
                  <div className="col-execution">
                    {sub.execution_time
                      ? `${(sub.execution_time * 1000).toFixed(0)}ms`
                      : "-"}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default SolutionsHistory;
