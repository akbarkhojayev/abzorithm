import React, { useEffect, useState } from "react";
import "./LeaderBoard.css";
import { getLeaderBoard } from "../services/app.js";
import { useTheme } from "../../context/ThemeContext";
import { FaMedal } from "react-icons/fa6";

function LeaderBoard({ ratingUser, setRatingUser }) {
  const [loaderLederboard, setLoaderLeaderboard] = useState(false);
  const { isDark } = useTheme();

  useEffect(() => {
    setLoaderLeaderboard(true);
    getLeaderBoard()
      ?.then(setRatingUser)
      .finally(() => {
        setLoaderLeaderboard(false);
      });
  }, []);

  const getMedalColor = (rank) => {
    if (rank === 1) return "#fbbf24";
    if (rank === 2) return "#9ca3af";
    if (rank === 3) return "#f97316";
    return null;
  };

  return (
    <div className={`leaderboard ${isDark ? "dark" : "light"}`}>
      <div className="page-header">
        <div className="header-content">
          <h1>Reyting Taxtasi</h1>
          <p>Eng yaxshi o'quvchilarni ko'ring</p>
        </div>
      </div>

      <div className="container">
        {loaderLederboard ? (
          <div className="loader-leaderboard">
            {[...Array(8)].map((_, i) => (
              <div key={i} className="loader-row"></div>
            ))}
          </div>
        ) : (
          <div className="leaderboard-table">
            <div className="table-header">
              <div className="header-rank">Rank</div>
              <div className="header-user">User</div>
              <div className="header-bio">Bio</div>
              <div className="header-score">Score</div>
            </div>

            <div className="table-body">
              {ratingUser?.map((item, index) => {
                const medalColor = getMedalColor(index + 1);
                const isMedal = index < 3;
                return (
                  <div key={item?.id} className={`table-row ${isMedal ? "top-rank" : ""}`}>
                    <div className="row-rank">
                      <div className={`rank-badge rank-${index + 1}`}>
                        {isMedal ? (
                          <FaMedal className="medal-icon" style={{ color: medalColor }} />
                        ) : (
                          <span>{index + 1}</span>
                        )}
                      </div>
                    </div>

                    <div className="row-user">
                      <div className="user-avatar">
                        <img
                          src={item?.avatar || "/imgs/icons.png"}
                          onError={(e) => {
                            e.target.onerror = null;
                            e.target.src = "/imgs/icons.png";
                          }}
                          alt={item?.username}
                        />
                      </div>
                      <div className="user-info">
                        <h3>{item?.username}</h3>
                        <p className="user-country">
                          {item?.country || "No location"}
                        </p>
                      </div>
                    </div>

                    <div className="row-bio">
                      <p>
                        {item?.bio && item?.bio.length > 0
                          ? item?.bio.length > 50
                            ? item?.bio.slice(0, 50) + "..."
                            : item?.bio
                          : "-"}
                      </p>
                    </div>

                    <div className="row-score">
                      <span className="score-value">{item?.score}</span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default LeaderBoard;
