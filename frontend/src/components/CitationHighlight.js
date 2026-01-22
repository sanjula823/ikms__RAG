import React, { useState } from 'react';
import './CitationHighlight.css';

/**
 * CitationHighlight Component
 * Highlights citations in answer and shows metadata on hover
 */
const CitationHighlight = ({ text, citations }) => {
  const [hoveredCitation, setHoveredCitation] = useState(null);
  const [tooltipPosition, setTooltipPosition] = useState({ x: 0, y: 0 });

  // Parse citations from text like [C1], [C2]
  const parseCitations = () => {
    const parts = [];
    let lastIndex = 0;
    const citationRegex = /\[C\d+\]/g;
    let match;

    while ((match = citationRegex.exec(text)) !== null) {
      // Add text before citation
      if (match.index > lastIndex) {
        parts.push({
          type: 'text',
          content: text.slice(lastIndex, match.index),
        });
      }

      // Add citation
      const citationId = match[0].slice(1, -1); // Remove brackets
      parts.push({
        type: 'citation',
        content: match[0],
        id: citationId,
        exists: citations && citationId in citations,
      });

      lastIndex = match.index + match[0].length;
    }

    // Add remaining text
    if (lastIndex < text.length) {
      parts.push({
        type: 'text',
        content: text.slice(lastIndex),
      });
    }

    return parts;
  };

  const handleCitationHover = (e, citationId) => {
    const rect = e.target.getBoundingClientRect();
    setTooltipPosition({
      x: rect.left,
      y: rect.bottom + 5,
    });
    setHoveredCitation(citationId);
  };

  const handleCitationLeave = () => {
    setHoveredCitation(null);
  };

  const parts = parseCitations();

  return (
    <div className="citation-highlight">
      {parts.map((part, idx) => {
        if (part.type === 'text') {
          return (
            <span key={idx} className="text-content">
              {part.content}
            </span>
          );
        } else {
          return (
            <span
              key={idx}
              className={`citation ${part.exists ? 'valid' : 'invalid'}`}
              onMouseEnter={(e) => handleCitationHover(e, part.id)}
              onMouseLeave={handleCitationLeave}
            >
              {part.content}
              {hoveredCitation === part.id && citations && citations[part.id] && (
                <div
                  className="citation-tooltip"
                  style={{
                    position: 'fixed',
                    left: `${tooltipPosition.x}px`,
                    top: `${tooltipPosition.y}px`,
                  }}
                >
                  <div className="tooltip-header">
                    <strong>{part.id}</strong> - Page {citations[part.id].page}
                  </div>
                  <div className="tooltip-source">
                    <small>{citations[part.id].source}</small>
                  </div>
                  <div className="tooltip-snippet">{citations[part.id].snippet}</div>
                </div>
              )}
            </span>
          );
        }
      })}
    </div>
  );
};

export default CitationHighlight;
