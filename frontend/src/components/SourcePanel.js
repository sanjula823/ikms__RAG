import React, { useState } from 'react';
import './SourcePanel.css';

/**
 * SourcePanel Component
 * Displays all cited chunks with page numbers and source information
 */
const SourcePanel = ({ citations, onCitationClick }) => {
  const [expandedCitation, setExpandedCitation] = useState(null);

  if (!citations || Object.keys(citations).length === 0) {
    return (
      <div className="source-panel empty">
        <p>No citations found</p>
      </div>
    );
  }

  const citationEntries = Object.entries(citations).sort((a, b) => {
    // Sort by citation ID number
    const numA = parseInt(a[0].replace('C', ''));
    const numB = parseInt(b[0].replace('C', ''));
    return numA - numB;
  });

  return (
    <div className="source-panel">
      <div className="source-panel-header">
        <h3>Citation Sources ({citationEntries.length})</h3>
      </div>
      <div className="source-panel-content">
        {citationEntries.map(([citationId, metadata]) => (
          <div
            key={citationId}
            className={`source-item ${expandedCitation === citationId ? 'expanded' : ''}`}
          >
            <div
              className="source-item-header"
              onClick={() =>
                setExpandedCitation(
                  expandedCitation === citationId ? null : citationId
                )
              }
            >
              <span className="citation-id">{citationId}</span>
              <span className="page-number">Page {metadata.page}</span>
              <span className="expand-icon">
                {expandedCitation === citationId ? '▼' : '▶'}
              </span>
            </div>
            {expandedCitation === citationId && (
              <div className="source-item-details">
                <div className="source-field">
                  <span className="label">Source:</span>
                  <span className="value">{metadata.source}</span>
                </div>
                <div className="source-field">
                  <span className="label">Snippet:</span>
                  <p className="snippet">{metadata.snippet}</p>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default SourcePanel;
