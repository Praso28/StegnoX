import React, { useState } from 'react';
import '../styles/AnalysisResults.css';

const AnalysisResults = ({ results }) => {
  const [activeTab, setActiveTab] = useState(Object.keys(results)[0] || '');

  if (!results || Object.keys(results).length === 0) {
    return <div className="no-results">No analysis results available</div>;
  }

  const formatMethodName = (method) => {
    return method
      .replace(/_/g, ' ')
      .replace(/\b\w/g, (char) => char.toUpperCase());
  };

  const renderContent = (result) => {
    if (result.error) {
      return <div className="result-error">{result.error}</div>;
    }

    if (result.message) {
      return <div className="result-message">{result.message}</div>;
    }

    // Handle different result types
    if (activeTab === 'lsb_extraction') {
      return renderLsbResults(result);
    } else if (activeTab === 'parity_bit_extraction') {
      return renderParityResults(result);
    } else if (activeTab === 'metadata_extraction') {
      return renderMetadataResults(result);
    } else if (activeTab === 'dct_analysis') {
      return renderDctResults(result);
    } else if (activeTab === 'bit_plane_analysis') {
      return renderBitPlaneResults(result);
    } else if (activeTab === 'histogram_analysis') {
      return renderHistogramResults(result);
    } else {
      // Generic rendering for other methods
      return (
        <div className="result-generic">
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      );
    }
  };

  const renderLsbResults = (result) => {
    return (
      <div className="lsb-results">
        <h4>LSB Extraction Results</h4>
        {result.message && (
          <div className="result-message">
            <h5>Extracted Message:</h5>
            <div className="message-box">{result.message}</div>
          </div>
        )}
      </div>
    );
  };

  const renderParityResults = (result) => {
    return (
      <div className="parity-results">
        <h4>Parity Bit Extraction Results</h4>
        {result.message && (
          <div className="result-message">
            <h5>Extracted Message:</h5>
            <div className="message-box">{result.message}</div>
          </div>
        )}
      </div>
    );
  };

  const renderMetadataResults = (result) => {
    return (
      <div className="metadata-results">
        <h4>Metadata Extraction Results</h4>
        <div className="metadata-table">
          <table>
            <tbody>
              {Object.entries(result).map(([key, value]) => {
                if (key === 'exif' && typeof value === 'object') {
                  return (
                    <tr key={key}>
                      <td className="key">EXIF Data</td>
                      <td className="value">
                        <details>
                          <summary>Show EXIF Data</summary>
                          <table className="exif-table">
                            <tbody>
                              {Object.entries(value).map(([exifKey, exifValue]) => (
                                <tr key={exifKey}>
                                  <td>{exifKey}</td>
                                  <td>{String(exifValue)}</td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </details>
                      </td>
                    </tr>
                  );
                } else {
                  return (
                    <tr key={key}>
                      <td className="key">{key}</td>
                      <td className="value">{String(value)}</td>
                    </tr>
                  );
                }
              })}
            </tbody>
          </table>
        </div>
      </div>
    );
  };

  const renderDctResults = (result) => {
    return (
      <div className="dct-results">
        <h4>DCT Analysis Results</h4>
        <div className="confidence-meter">
          <h5>Confidence: {result.confidence?.toFixed(2)}%</h5>
          <div className="meter">
            <div 
              className="meter-fill" 
              style={{ width: `${result.confidence || 0}%` }}
            ></div>
          </div>
        </div>
        <div className="assessment">
          <h5>Assessment: {result.assessment}</h5>
        </div>
        {result.statistics && (
          <div className="statistics">
            <h5>Statistics:</h5>
            <table>
              <tbody>
                {Object.entries(result.statistics).map(([key, value]) => (
                  <tr key={key}>
                    <td>{key.replace(/_/g, ' ')}</td>
                    <td>{value}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    );
  };

  const renderBitPlaneResults = (result) => {
    return (
      <div className="bit-plane-results">
        <h4>Bit Plane Analysis Results</h4>
        <div className="confidence-meter">
          <h5>Confidence: {result.confidence?.toFixed(2)}%</h5>
          <div className="meter">
            <div 
              className="meter-fill" 
              style={{ width: `${result.confidence || 0}%` }}
            ></div>
          </div>
        </div>
        <div className="assessment">
          <h5>Assessment: {result.assessment}</h5>
        </div>
        <div className="suspicious-planes">
          <h5>Suspicious Planes: {result.suspicious_planes || 0}</h5>
        </div>
      </div>
    );
  };

  const renderHistogramResults = (result) => {
    return (
      <div className="histogram-results">
        <h4>Histogram Analysis Results</h4>
        <div className="confidence-meter">
          <h5>Confidence: {result.confidence?.toFixed(2)}%</h5>
          <div className="meter">
            <div 
              className="meter-fill" 
              style={{ width: `${result.confidence || 0}%` }}
            ></div>
          </div>
        </div>
        <div className="assessment">
          <h5>Assessment: {result.assessment}</h5>
        </div>
      </div>
    );
  };

  return (
    <div className="analysis-results">
      <div className="results-tabs">
        {Object.keys(results).map((method) => (
          <button
            key={method}
            className={`tab-button ${activeTab === method ? 'active' : ''}`}
            onClick={() => setActiveTab(method)}
          >
            {formatMethodName(method)}
          </button>
        ))}
      </div>
      
      <div className="results-content">
        {renderContent(results[activeTab])}
      </div>
      
      <div className="results-actions">
        <button className="export-button">
          Export Results
        </button>
      </div>
    </div>
  );
};

export default AnalysisResults;
