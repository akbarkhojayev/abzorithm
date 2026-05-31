import React from "react";
import "./SkeletonLoader.css";

/**
 * Reusable Skeleton Loader Component
 * Supports multiple layouts and dark mode
 */
export const TableSkeleton = ({ rows = 10, columns = 3 }) => (
  <div className="skeleton-table">
    {[...Array(rows)].map((_, i) => (
      <div key={i} className="skeleton-table-row">
        {[...Array(columns)].map((_, j) => (
          <div key={j} className="skeleton-cell"></div>
        ))}
      </div>
    ))}
  </div>
);

export const ListSkeleton = ({ items = 5 }) => (
  <div className="skeleton-list">
    {[...Array(items)].map((_, i) => (
      <div key={i} className="skeleton-list-item">
        <div className="skeleton-avatar"></div>
        <div className="skeleton-content">
          <div className="skeleton-line skeleton-title"></div>
          <div className="skeleton-line skeleton-subtitle"></div>
        </div>
      </div>
    ))}
  </div>
);

export const CardSkeleton = ({ count = 3 }) => (
  <div className="skeleton-card-grid">
    {[...Array(count)].map((_, i) => (
      <div key={i} className="skeleton-card">
        <div className="skeleton-card-header"></div>
        <div className="skeleton-card-body">
          <div className="skeleton-line"></div>
          <div className="skeleton-line"></div>
          <div className="skeleton-line skeleton-short"></div>
        </div>
      </div>
    ))}
  </div>
);

export const TextBlockSkeleton = ({ lines = 5 }) => (
  <div className="skeleton-text-block">
    {[...Array(lines)].map((_, i) => (
      <div
        key={i}
        className={`skeleton-line ${i === lines - 1 ? "skeleton-short" : ""}`}
      ></div>
    ))}
  </div>
);

/**
 * Generic Skeleton Loader with custom configuration
 */
export const SkeletonLoader = ({
  type = "table",
  rows = 5,
  columns = 3,
  count = 3,
  lines = 5
}) => {
  switch (type) {
    case "table":
      return <TableSkeleton rows={rows} columns={columns} />;
    case "list":
      return <ListSkeleton items={rows} />;
    case "card":
      return <CardSkeleton count={count} />;
    case "text":
      return <TextBlockSkeleton lines={lines} />;
    default:
      return <TableSkeleton rows={rows} columns={columns} />;
  }
};

export default SkeletonLoader;
