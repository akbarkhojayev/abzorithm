import React from 'react';
import './EmptyState.css';

function EmptyState({ 
  icon = 'fa-inbox',
  title = 'No results found',
  message = 'Try adjusting your search or filter to find what you are looking for.',
  action,
  actionLabel
}) {
  return (
    <div className="empty-state">
      <div className="empty-state-icon">
        <i className={`fas ${icon}`}></i>
      </div>
      <h3 className="empty-state-title">{title}</h3>
      <p className="empty-state-message">{message}</p>
      {action && actionLabel && (
        <button onClick={action} className="empty-state-button">
          {actionLabel}
        </button>
      )}
    </div>
  );
}

export default EmptyState;
