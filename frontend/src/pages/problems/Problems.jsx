import React, { useEffect, useState, useRef } from "react";
import "./Problems.css";
import { Link, useNavigate } from "react-router-dom";
import { getProblems } from "../services/app.js";
import { getToken } from "../services/token.js";
import { FiSearch, FiCheck, FiCircle } from "react-icons/fi";
import { baseUrl } from "../services/config.js";
import StatusBadge from "../../components/badges/StatusBadge.jsx";

function Problems({ problemData, setProblemData }) {
  const [loader, setLoader] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const [search, setSearch] = useState("");
  const [selectedTag, setSelectedTag] = useState("");
  const [selectedDifficulty, setSelectedDifficulty] = useState("");
  const [allTags, setAllTags] = useState([]);
  const [categoryCounts, setCategoryCounts] = useState({});
  const difficulties = ["Easy", "Medium", "Hard"];
  const scrollContainerRef = useRef(null);

  useEffect(() => {
    loadProblems();
  }, []);

  const loadProblems = async () => {
    setLoader(true);
    setError(null);
    try {
      const data = await getProblems();
      setProblemData(data);
      extractTags(data);
    } catch (err) {
      setError("Masalalar yuklanishi uchun xatolik yuz berdi");
      console.error("Error loading problems:", err);
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

  const getFilterData = async () => {
    setLoader(true);
    setError(null);

    try {
      const params = new URLSearchParams({ search });
      const response = await fetch(`${baseUrl}/problems/?${params.toString()}`);

      if (!response.ok) {
        throw new Error("Filtrlash uchun xatolik yuz berdi");
      }

      const data = await response.json();
      let filtered = data;

      if (selectedTag) {
        filtered = filtered.filter((p) =>
          p.categories?.some((cat) => cat.name === selectedTag)
        );
      }

      if (selectedDifficulty) {
        filtered = filtered.filter((p) => p.difficulty === selectedDifficulty);
      }

      setProblemData(filtered);
    } catch (err) {
      setError("Qidirish uchun xatolik yuz berdi");
      console.error("Error filtering problems:", err);
    } finally {
      setLoader(false);
    }
  };

  useEffect(() => {
    const delay = setTimeout(() => {
      if (search || selectedTag || selectedDifficulty) {
        getFilterData();
      } else {
        loadProblems();
      }
      // Reset scroll to top when filters change
      if (scrollContainerRef.current) {
        scrollContainerRef.current.scrollTop = 0;
      }
    }, 300);

    return () => clearTimeout(delay);
  }, [search, selectedTag, selectedDifficulty]);


  return (
    <>
      {/* STICKY CONTROLS: Title + Search + Filter - Centered */}
      <div className="problems-controls-sticky">
        <h2 className="sticky-title">Masalalar</h2>
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

        <select
          value={selectedDifficulty}
          onChange={(e) => setSelectedDifficulty(e.target.value)}
          className="difficulty-select"
          aria-label="Darajasi bo'yicha filtrlash"
        >
          <option value="">Darajasi</option>
          {difficulties.map((difficulty) => (
            <option key={difficulty} value={difficulty}>
              {difficulty}
            </option>
          ))}
        </select>
      </div>

      <div className="problems-wrapper" ref={scrollContainerRef}>
        {/* CATEGORIES SIDEBAR - Grid column 2 */}
        {allTags.length > 0 && (
          <div className="categories-card">
            <h2 className="categories-title">Mavzu</h2>
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

        {/* MAIN CONTENT - Grid column 1 */}
        <div className="problems-content">
          {/* ERROR MESSAGE */}
          {error && (
            <div className="error-banner" role="alert">
              <p>{error}</p>
              <button onClick={loadProblems} className="error-retry-btn">
                Qayta urinish
              </button>
            </div>
          )}

          {/* HEADER: Subtitle */}
          <div className="problems-header">
            <p className="page-subtitle">Algoritmik masalalarni yechish orqali o'zingizni sinab ko'ring</p>
          </div>

          {/* PROBLEMS TABLE */}
          <div className="problems-table">
          {loader ? (
            <div className="loader-list">
              {[...Array(10)].map((_, i) => (
                <div key={i} className="loader-item"></div>
              ))}
            </div>
          ) : problemData && problemData.length > 0 ? (
            <div className="problems-table-body">
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
                  <div className="table-col col-checkbox">
                    {item?.is_solved ? (
                      <span className="solved-check">✓</span>
                    ) : (
                      <span className="unsolved-dot">•</span>
                    )}
                  </div>

                  <div className="table-col col-title">
                    <span className="problem-name">{item?.title}</span>
                    {item?.difficulty && (
                      <span className={`difficulty-tag difficulty-${item?.difficulty?.toLowerCase()}`}>
                        {item?.difficulty}
                      </span>
                    )}
                  </div>

                  <div className="table-col col-badge">
                    {item?.categories && item?.categories.length > 0 && (
                      <span className="algo-badge">{item?.categories[0].name}</span>
                    )}
                  </div>
                </Link>
              ))}
            </div>
          ) : (
            <div className="no-problems">
              <p>📭 Hech qanday masala topilmadi</p>
            </div>
          )}
        </div>
      </div>
    </div>
    </>
  );
}

export default Problems;
