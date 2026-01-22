import React, { useMemo } from 'react';
import './CitationHeatmap.css';

/**
 * CitationHeatmap Component
 * Visual indication of which chunks were most cited
 */
const CitationHeatmap = ({ citations, answer }) => {
  // Calculate citation frequency
  const citationFrequency = useMemo(() => {
    if (!citations || !answer) return {};

    const freq = {};
    const citationRegex = /\[C\d+\]/g;
    let match;

    while ((match = citationRegex.exec(answer)) !== null) {
      const citationId = match[0].slice(1, -1); // Remove brackets
      freq[citationId] = (freq[citationId] || 0) + 1;
    }

    return freq;
  }, [citations, answer]);

  if (!citations || Object.keys(citations).length === 0) {
    return (
      <div className="citation-heatmap empty">
        <p>No citation data available</p>
      </div>
    );
  }

  const citationEntries = Object.entries(citations).sort((a, b) => {
    const numA = parseInt(a[0].replace('C', ''));
    const numB = parseInt(b[0].replace('C', ''));
    return numA - numB;
  });

  // Calculate max frequency for normalization
  const maxFreq = Math.max(...Object.values(citationFrequency), 1);

  // Get intensity color based on frequency
  const getIntensityColor = (freq) => {
    const intensity = Math.min(freq / maxFreq, 1);
    const hue = 210 - intensity * 30; // Blue to purple
    const saturation = 70 + intensity * 20;
    const lightness = 90 - intensity * 40;
    return `hsl(${hue}, ${saturation}%, ${lightness}%)`;
  };

  return (
    <div className="citation-heatmap">
      <div className="heatmap-header">
        <h3>Citation Frequency</h3>
        <div className="heatmap-legend">
          <span className="legend-item">
            <span className="legend-color" style={{ backgroundColor: getIntensityColor(0) }}></span>
            <span>Low</span>
          </span>
          <span className="legend-item">
            <span className="legend-color" style={{ backgroundColor: getIntensityColor(maxFreq) }}></span>
            <span>High</span>
          </span>
        </div>
      </div>
      <div className="heatmap-grid">
        {citationEntries.map(([citationId, metadata]) => {
          const freq = citationFrequency[citationId] || 0;
          const bgColor = getIntensityColor(freq);

          return (
            <div
              key={citationId}
              className="heatmap-item"
              style={{ backgroundColor: bgColor }}
              title={`${citationId}: ${freq} reference${freq !== 1 ? 's' : ''}`}
            >
              <div className="heatmap-id">{citationId}</div>
              <div className="heatmap-freq">{freq}</div>
              <div className="heatmap-page">p{metadata.page}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default CitationHeatmap;
