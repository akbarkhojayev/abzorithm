import React, { useEffect, useState } from "react";
import "./Problems.css";
import { Link, useNavigate } from "react-router-dom";
import { getProblems } from "../services/app.js";
import { getToken } from "../services/token.js";
import { FiSearch } from "react-icons/fi";
import { baseUrl } from "../services/config.js";

function Problems({ problemData, setProblemData }) {
  const [loader, setLoader] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const [search, setSearch] = useState("");
  const [selectedTag, setSelectedTag] = useState("");
  const [allTags, setAllTags] = useState([]);
  const [categoryCounts, setCategoryCounts] = useState({});
  const [currentPage, setCurrentPage] = useState(1);
  const [totalProblems, setTotalProblems] = useState(0);
  const [pageSize] = useState(10);

  useEffect(() => {
    loadProblems();
  }, []);

  const loadProblems = async (page = 1) => {
    setLoader(true);
    setError(null);
    try {
      const offset = (page - 1) * pageSize;
      const token = getToken();

      const response = await fetch(`${baseUrl}/problems/?limit=${pageSize}&offset=${offset}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : {}
      });

      if (!response.ok) {
        throw new Error("Failed to load problems");
      }

      const data = await response.json();
      setProblemData(Array.isArray(data.results) ? data.results : []);
      setTotalProblems(data.count || 0);
      setCurrentPage(page);

      if (page === 1) {
        extractTags(Array.isArray(data.results) ? data.results : []);
      }
    } catch (err) {
      setError("Masalalar yuklanishi uchun xatolik yuz berdi");
      console.error("Error loading problems:", err);
      setProblemData([]);
    } finally {
      setLoader(false);
    }
  };

  const extractTags = (problems) => {
    const tagsSet = new Set();
    const counts = {};
    problems?.forEach((problem) => {
      if (problem?.categories && Array.isArray(problem.categories)) {
        problem.categories.forEach((category) => {
          if (category?.name) {
            tagsSet.add(category.name);
            counts[category.name] = (counts[category.name] || 0) + 1;
          }
        });
      }
    });
    setAllTags(Array.from(tagsSet).sort());
    setCategoryCounts(counts);
  };

  const getFilterData = async (page = 1) => {
    setLoader(true);
    setError(null);

    try {
      const offset = (page - 1) * pageSize;
      const token = getToken();
      const params = new URLSearchParams({
        search,
        limit: pageSize,
        offset
      });

      const response = await fetch(`${baseUrl}/problems/?${params.toString()}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : {}
      });

      if (!response.ok) {
        throw new Error("Filtrlash uchun xatolik yuz berdi");
      }

      const data = await response.json();
      let filtered = Array.isArray(data.results) ? data.results : [];

      if (selectedTag) {
        filtered = filtered.filter((p) =>
          p.categories?.some((cat) => cat.name === selectedTag)
        );
      }

      setProblemData(filtered);
      setTotalProblems(data.count || 0);
      setCurrentPage(page);
    } catch (err) {
      setError("Qidirish uchun xatolik yuz berdi");
      console.error("Error filtering problems:", err);
      setProblemData([]);
    } finally {
      setLoader(false);
    }
  };

  useEffect(() => {
    const delay = setTimeout(() => {
      setCurrentPage(1);
      if (search || selectedTag) {
        getFilterData(1);
      } else {
        loadProblems(1);
      }
      window.scrollTo({ top: 0, behavior: "smooth" });
    }, 300);

    return () => clearTimeout(delay);
  }, [search, selectedTag]);

  return (
    <div className="problems-page">
      <div className="problems-header-section">
        <div className="problems-header-content">
          <h1>Masalalar</h1>
          <p>Algoritmik masalalarni yechish orqali o'zingizni sinab ko'ring</p>
        </div>
      </div>

      <div className="problems-container">
        <div className="problems-filters-section">
          <div className="search-box">
            <FiSearch className="search-icon" />
            <input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              type="text"
              placeholder="Masala qidirish..."
              className="search-input"
              aria-label="Masalalar bo'yicha qidirish"
            />
          </div>
        </div>

        <div className="problems-main">
          {allTags.length > 0 && (
            <div className="categories-sidebar">
              <h2 className="categories-title">Mavzular</h2>
              <div className="categories-grid">
                {allTags.map((tag) => (
                  <button
                    key={tag}
                    className={`category-item ${selectedTag === tag ? "active" : ""}`}
                    onClick={() => setSelectedTag(selectedTag === tag ? "" : tag)}
                    title={`${tag} - ${categoryCounts[tag] || 0} masalalar`}
                  >
                    <span className="category-name">{tag}</span>
                    <span className="category-count">{categoryCounts[tag] || 0}</span>
                  </button>
                ))}
              </div>
            </div>
          )}

          <div className="problems-content">
            {error && (
              <div className="error-banner" role="alert">
                <p>{error}</p>
                <button onClick={loadProblems} className="error-retry-btn">
                  Qayta urinish
                </button>
              </div>
            )}

            {loader ? (
              <div className="problems-loader">
                {[...Array(8)].map((_, i) => (
                  <div key={i} className="problems-loader-row"></div>
                ))}
              </div>
            ) : problemData && problemData.length > 0 ? (
              <div className="problems-table-wrapper">
                <div className="problems-table">
                  <div className="table-header">
                    <div className="header-status">Status</div>
                    <div className="header-title">Masala</div>
                    <div className="header-category">Mavzu</div>
                    <div className="header-difficulty">Qiyinlik</div>
                  </div>

                  <div className="table-body">
                    {problemData.map((item) => (
                      <Link
                        className={`table-row ${item?.is_solved ? "solved" : ""}`}
                        key={item?.id}
                        to={`/codepanels/${item?.slug}`}
                        onClick={(e) => {
                          if (!getToken()) {
                            e.preventDefault();
                            navigate("/create-account");
                          }
                        }}
                      >
                        <div className="row-status">
                          {item?.is_solved ? (
                            <span className="status-icon solved" title="Yechilgan">✓</span>
                          ) : (
                            <span className="status-icon unsolved" title="Yechilmagan"></span>
                          )}
                        </div>
                        <div className="row-title">
                          <span className="problem-title">{item?.title}</span>
                        </div>
                        <div className="row-category">
                          {item?.categories && item?.categories.length > 0 && (
                            <span className="category-badge">{item?.categories[0].name}</span>
                          )}
                        </div>
                        <div className="row-difficulty">
                          {item?.difficulty && (
                            <span className={`difficulty-badge difficulty-${item?.difficulty?.toLowerCase()}`}>
                              {item?.difficulty}
                            </span>
                          )}
                        </div>
                      </Link>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <div className="empty-state">
                <h2>Hech qanday masala topilmadi</h2>
                <p>Masalalar yuklanmayotgan bo'lsa, qayta urinib ko'ring</p>
              </div>
            )}

            {problemData && problemData.length > 0 && totalProblems > pageSize && (
              <div className="pagination-container">
                <button
                  className="pagination-btn"
                  onClick={() => {
                    if (search || selectedTag) {
                      getFilterData(currentPage - 1);
                    } else {
                      loadProblems(currentPage - 1);
                    }
                  }}
                  disabled={currentPage === 1}
                >
                  ← Oldingi
                </button>

                <div className="pagination-info">
                  <span>Sahifa {currentPage} / {Math.ceil(totalProblems / pageSize)}</span>
                  <span className="pagination-count">Jami: {totalProblems}</span>
                </div>

                <button
                  className="pagination-btn"
                  onClick={() => {
                    if (search || selectedTag) {
                      getFilterData(currentPage + 1);
                    } else {
                      loadProblems(currentPage + 1);
                    }
                  }}
                  disabled={currentPage >= Math.ceil(totalProblems / pageSize)}
                >
                  Keyingi →
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Problems;
