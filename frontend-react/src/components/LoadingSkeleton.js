import React from 'react';
import './LoadingSkeleton.css';

function LoadingSkeleton({ count = 6 }) {
  return (
    <div className="problems-grid">
      {[...Array(count)].map((_, index) => (
        <div key={index} className="skeleton-card">
          <div className="skeleton-header">
            <div className="skeleton-badge"></div>
            <div className="skeleton-badge"></div>
          </div>
          <div className="skeleton-title"></div>
          <div className="skeleton-text"></div>
          <div className="skeleton-text short"></div>
          <div className="skeleton-tags">
            <div className="skeleton-tag"></div>
            <div className="skeleton-tag"></div>
            <div className="skeleton-tag"></div>
          </div>
          <div className="skeleton-footer">
            <div className="skeleton-stats"></div>
            <div className="skeleton-button"></div>
          </div>
        </div>
      ))}
    </div>
  );
}

export default LoadingSkeleton;
