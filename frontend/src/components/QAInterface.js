import React, { useState } from 'react';
import { answerQuestion, indexPdf } from '../api';
import CitationHighlight from './CitationHighlight';
import SourcePanel from './SourcePanel';
import CitationHeatmap from './CitationHeatmap';
import './QAInterface.css';

/**
 * QAInterface Component
 * Main interface for asking questions and viewing citation-aware answers
 */
const QAInterface = () => {
  const [query, setQuery] = useState('');
  const [answer, setAnswer] = useState(null);
  const [citations, setCitations] = useState(null);
  const [context, setContext] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('answer');
  const [pdfPath, setPdfPath] = useState('');
  const [indexing, setIndexing] = useState(false);
  const [indexMessage, setIndexMessage] = useState('');

  const handleAsk = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const response = await answerQuestion(query);
      setAnswer(response.answer);
      setCitations(response.citations);
      setContext(response.context);
      setActiveTab('answer');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleIndexPdf = async (e) => {
    e.preventDefault();
    if (!pdfPath.trim()) return;

    setIndexing(true);
    setIndexMessage('');

    try {
      const response = await indexPdf(pdfPath);
      setIndexMessage(response.message);
      setPdfPath('');
    } catch (err) {
      setIndexMessage(`Error: ${err.message}`);
    } finally {
      setIndexing(false);
    }
  };

  return (
    <div className="qa-interface">
      <div className="qa-container">
        {/* Header */}
        <div className="qa-header">
          <h1>IKMS Multi-Agent RAG</h1>
          <p className="subtitle">Evidence-Aware Question Answering with Citations</p>
        </div>

        {/* Query Form */}
        <form onSubmit={handleAsk} className="query-form">
          <div className="input-group">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask a question..."
              className="query-input"
              disabled={loading}
            />
            <button type="submit" className="submit-button" disabled={loading}>
              {loading ? 'Searching...' : 'Ask'}
            </button>
          </div>
        </form>

        {/* PDF Indexing Section */}
        <div className="indexing-section">
          <form onSubmit={handleIndexPdf} className="index-form">
            <div className="input-group">
              <input
                type="text"
                value={pdfPath}
                onChange={(e) => setPdfPath(e.target.value)}
                placeholder="PDF file path to index..."
                className="pdf-input"
                disabled={indexing}
              />
              <button type="submit" className="index-button" disabled={indexing}>
                {indexing ? 'Indexing...' : 'Index PDF'}
              </button>
            </div>
            {indexMessage && (
              <p className={`index-message ${indexMessage.includes('Error') ? 'error' : 'success'}`}>
                {indexMessage}
              </p>
            )}
          </form>
        </div>

        {/* Error Display */}
        {error && <div className="error-message">{error}</div>}

        {/* Results Section */}
        {answer && (
          <div className="results-section">
            <div className="tabs">
              <button
                className={`tab ${activeTab === 'answer' ? 'active' : ''}`}
                onClick={() => setActiveTab('answer')}
              >
                Answer
              </button>
              <button
                className={`tab ${activeTab === 'sources' ? 'active' : ''}`}
                onClick={() => setActiveTab('sources')}
              >
                Sources ({citations ? Object.keys(citations).length : 0})
              </button>
              <button
                className={`tab ${activeTab === 'heatmap' ? 'active' : ''}`}
                onClick={() => setActiveTab('heatmap')}
              >
                Citation Frequency
              </button>
              <button
                className={`tab ${activeTab === 'context' ? 'active' : ''}`}
                onClick={() => setActiveTab('context')}
              >
                Full Context
              </button>
            </div>

            <div className="tab-content">
              {activeTab === 'answer' && (
                <div className="answer-panel">
                  <h3>Answer</h3>
                  <CitationHighlight text={answer} citations={citations} />
                </div>
              )}

              {activeTab === 'sources' && (
                <SourcePanel citations={citations} />
              )}

              {activeTab === 'heatmap' && (
                <CitationHeatmap citations={citations} answer={answer} />
              )}

              {activeTab === 'context' && (
                <div className="context-panel">
                  <h3>Retrieved Context</h3>
                  <pre>{context}</pre>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Loading Indicator */}
        {loading && (
          <div className="loading-indicator">
            <div className="spinner"></div>
            <p>Processing your question...</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default QAInterface;
