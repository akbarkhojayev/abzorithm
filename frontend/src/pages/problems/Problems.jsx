import React, { useState, useEffect } from "react";
import "./Problems.css";
import { useNavigate } from "react-router-dom";
import { baseUrl } from "../services/config.js";
import { getToken } from "../services/token.js";
import { useTheme } from "../../context/ThemeContext";

function Problems() {
  const navigate = useNavigate();
  const { isDark } = useTheme();

  const [problems, setProblems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedDifficulty, setSelectedDifficulty] = useState(null);
  const [sortBy, setSortBy] = useState("id");
  const [currentPage, setCurrentPage] = useState(1);

  const itemsPerPage = 20;

  useEffect(() => {
    const fetchProblems = async () => {
      try {
        const response = await fetch(`${baseUrl}/problems/?limit=1000`, {
          headers: { Authorization: `Bearer ${getToken()}` },
        });
        if (response.ok) {
          const data = await response.json();
          setProblems(data.results || data);
        }
      } catch (err) {
        console.error("Error loading problems:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchProblems();
  }, []);

  // Filter masalalar
  const filtered = problems.filter(p => {
    const matchSearch = p.title.toLowerCase().includes(searchQuery.toLowerCase());
    const matchDifficulty = !selectedDifficulty || p.difficulty === selectedDifficulty;
    return matchSearch && matchDifficulty;
  });

  // Saralash
  const sorted = [...filtered].sort((a, b) => {
    if (sortBy === "title") return a.title.localeCompare(b.title);
    if (sortBy === "difficulty") {
      const order = { "Easy": 0, "Medium": 1, "Hard": 2 };
      return order[a.difficulty] - order[b.difficulty];
    }
    return a.id - b.id;
  });

  // Pagination
  const totalPages = Math.ceil(sorted.length / itemsPerPage);
  const paginatedItems = sorted.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  const getDifficultyColor = (difficulty) => {
    const colors = {
      "Easy": "#10b981",
      "Medium": "#f59e0b",
      "Hard": "#ef4444",
    };
    return colors[difficulty] || "#666";
  };

  if (loading) {
    return (
      <div className={`problems-page ${isDark ? "dark" : "light"}`}>
        <div className="loading-state">
          <div className="spinner"></div>
          <p>Masalalar yuklanmoqda...</p>
        </div>
      </div>
    );
  }

  return (
    <div className={`problems-page ${isDark ? "dark" : "light"}`}>
      {/* Header */}
      <div className="page-header">
        <div className="header-wrapper">
          <div className="header-left">
            <h1>Masalalar</h1>
            <p className="count-badge">{sorted.length} ta</p>
          </div>

          <div className="header-right">
            <input
              type="text"
              placeholder="Qidirish..."
              className="search-input"
              value={searchQuery}
              onChange={(e) => {
                setSearchQuery(e.target.value);
                setCurrentPage(1);
              }}
            />
            <select
              className="select-control"
              value={selectedDifficulty || "all"}
              onChange={(e) => {
                setSelectedDifficulty(e.target.value === "all" ? null : e.target.value);
                setCurrentPage(1);
              }}
            >
              <option value="all">Qiyinlik</option>
              <option value="Easy">Oson</option>
              <option value="Medium">O'rtacha</option>
              <option value="Hard">Qiyin</option>
            </select>
            <select
              className="select-control"
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
            >
              <option value="id">ID</option>
              <option value="title">Nomi</option>
              <option value="difficulty">Qiyinlik</option>
            </select>
          </div>
        </div>
      </div>

      {/* Content Area */}
      <div className="content-wrapper">
        {loading ? (
          <div className="loading-state">
            <div className="spinner"></div>
            <p>Yuklanmoqda...</p>
          </div>
        ) : paginatedItems.length > 0 ? (
          <>
            <div className="problems-list">
              {paginatedItems.map((problem) => (
                <div
                  key={problem.id}
                  className="list-item"
                  onClick={() => navigate(`/codepanels/${problem.slug}`)}
                >
                  <div className="item-number">{problem.id}</div>
                  <div className="item-content">
                    <h3 className="item-name">{problem.title}</h3>
                    {problem.categories && problem.categories.length > 0 && (
                      <div className="item-cats">
                        {problem.categories.slice(0, 2).map((cat) => (
                          <span key={cat.id} className="cat-label">{cat.name}</span>
                        ))}
                      </div>
                    )}
                  </div>
                  <div
                    className="item-diff"
                    style={{
                      backgroundColor: getDifficultyColor(problem.difficulty),
                      color: 'white'
                    }}
                  >
                    {problem.difficulty}
                  </div>
                </div>
              ))}
            </div>

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="pagination-compact">
                <button
                  disabled={currentPage === 1}
                  onClick={() => setCurrentPage(1)}
                  className="pg-btn"
                >
                  ⟨⟨
                </button>
                <button
                  disabled={currentPage === 1}
                  onClick={() => setCurrentPage(currentPage - 1)}
                  className="pg-btn"
                >
                  ⟨
                </button>

                {Array.from({ length: totalPages }, (_, i) => i + 1)
                  .filter(
                    (p) =>
                      p === 1 ||
                      p === totalPages ||
                      (p >= currentPage - 1 && p <= currentPage + 1)
                  )
                  .map((page, idx, arr) => (
                    <React.Fragment key={page}>
                      {idx > 0 && arr[idx - 1] !== page - 1 && (
                        <span className="pg-dots">...</span>
                      )}
                      <button
                        onClick={() => setCurrentPage(page)}
                        className={`pg-btn ${currentPage === page ? "active" : ""}`}
                      >
                        {page}
                      </button>
                    </React.Fragment>
                  ))}

                <button
                  disabled={currentPage === totalPages}
                  onClick={() => setCurrentPage(currentPage + 1)}
                  className="pg-btn"
                >
                  ⟩
                </button>
                <button
                  disabled={currentPage === totalPages}
                  onClick={() => setCurrentPage(totalPages)}
                  className="pg-btn"
                >
                  ⟩⟩
                </button>
              </div>
            )}
          </>
        ) : (
          <div className="empty-state">
            <p>Masala topilmadi</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default Problems;
