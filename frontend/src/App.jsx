import React, { useState, useEffect, useRef } from 'react';
import './App.css';

const API_URL = 'http://localhost:8000';

// Theme icon component
const SunIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
  </svg>
);

const MoonIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
  </svg>
);

// Simple icon components
const icons = {
  shield: () => (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
    </svg>
  ),
  upload: () => (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/>
    </svg>
  ),
  file: () => (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/>
    </svg>
  ),
  check: () => (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="20 6 9 17 4 12"/>
    </svg>
  ),
  x: () => (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
    </svg>
  ),
  alert: () => (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
    </svg>
  ),
  history: () => (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
    </svg>
  ),
  chart: () => (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>
    </svg>
  ),
  brain: () => (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 1.98-3A2.5 2.5 0 0 1 9.5 2Z"/>
      <path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96.44 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24 2.5 2.5 0 0 0-1.98-3A2.5 2.5 0 0 0 14.5 2Z"/>
    </svg>
  ),
  settings: () => (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
    </svg>
  ),
  loader: () => (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="spin">
      <line x1="12" y1="2" x2="12" y2="6"/><line x1="12" y1="18" x2="12" y2="22"/><line x1="4.93" y1="4.93" x2="7.76" y2="7.76"/><line x1="16.24" y1="16.24" x2="19.07" y2="19.07"/><line x1="2" y1="12" x2="6" y2="12"/><line x1="18" y1="12" x2="22" y2="12"/><line x1="4.93" y1="19.07" x2="7.76" y2="16.24"/><line x1="16.24" y1="7.76" x2="19.07" y2="4.93"/>
    </svg>
  ),
  arrowRight: () => (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>
    </svg>
  ),
  arrowLeft: () => (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/>
    </svg>
  ),
  pie: () => (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M21.21 15.89A10 10 0 1 1 8 2.83"/><path d="M22 12A10 10 0 0 0 12 2v10z"/>
    </svg>
  ),
  bar: () => (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>
    </svg>
  ),
  download: () => (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>
    </svg>
  ),
  print: () => (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/>
    </svg>
  ),
  x: () => (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
    </svg>
  ),
};

function App() {
  const [view, setView] = useState('home'); // home, analyze, results, history
  const [chartView, setChartView] = useState('pie'); // pie, bar
  const [filterView, setFilterView] = useState('all'); // all, Compliant, Partial, Missing
  const [theme, setTheme] = useState(() => {
    const saved = localStorage.getItem('theme');
    return saved || 'dark';
  });
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [regFile, setRegFile] = useState(null);
  const [policyFile, setPolicyFile] = useState(null);
  const [threshold, setThreshold] = useState(0.75);
  const [useAI, setUseAI] = useState(false);
  const [geminiKey, setGeminiKey] = useState('');
  const [history, setHistory] = useState([]);
  const [apiStatus, setApiStatus] = useState(null);
  const regInputRef = useRef(null);
  const policyInputRef = useRef(null);

  // Apply theme to document
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => prev === 'dark' ? 'light' : 'dark');
  };

  useEffect(() => {
    checkApiStatus();
    fetchHistory();
  }, []);

  const checkApiStatus = async () => {
    try {
      const response = await fetch(`${API_URL}/info`);
      if (response.ok) {
        const data = await response.json();
        setApiStatus(data);
      }
    } catch (error) {
      console.error('API not reachable:', error);
    }
  };

  const fetchHistory = async () => {
    try {
      const response = await fetch(`${API_URL}/history`);
      if (response.ok) {
        const data = await response.json();
        setHistory(data);
      }
    } catch (error) {
      console.error('Failed to fetch history:', error);
    }
  };

  const handleAnalyze = async () => {
    if (!regFile || !policyFile) {
      alert('Please upload both regulatory and policy documents');
      return;
    }

    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('reg_file', regFile);
      formData.append('policy_file', policyFile);
      formData.append('threshold', threshold);
      formData.append('use_ai', useAI);
      if (geminiKey) formData.append('gemini_key', geminiKey);

      const response = await fetch(`${API_URL}/analyze`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error('Analysis failed');

      const data = await response.json();
      setResults(data);
      await fetchHistory();
      setView('results');
    } catch (error) {
      console.error('Error:', error);
      alert('Analysis failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const loadFromHistory = async (itemId) => {
    try {
      const response = await fetch(`${API_URL}/history/${itemId}`);
      if (response.ok) {
        const data = await response.json();
        setResults(data.results);
        setView('results');
      }
    } catch (error) {
      console.error('Failed to load history item:', error);
    }
  };

  // Render Home View
  const renderHome = () => (
    <div className="home-view">
      <div className="hero-section">
        <div className="hero-icon">
          <icons.shield />
        </div>
        <h1 className="hero-title">
          <span className="gradient-text">AI-Powered</span> Compliance Copilot
        </h1>
        <p className="hero-subtitle">
          Automatically analyze your internal policies against regulatory requirements.
          Get instant gap analysis with AI-generated explanations.
        </p>
        <div className="hero-actions">
          <button className="btn btn-primary btn-large" onClick={() => setView('analyze')}>
            Start Analysis <icons.arrowRight />
          </button>
          <button className="btn btn-secondary btn-large" onClick={() => setView('history')}>
            View History
          </button>
        </div>
      </div>

      <div className="features-grid">
        <div className="feature-card">
          <div className="feature-icon"><icons.file /></div>
          <h3>PDF Analysis</h3>
          <p>Upload regulatory documents and policies in PDF format for automated analysis</p>
        </div>
        <div className="feature-card">
          <div className="feature-icon"><icons.chart /></div>
          <h3>Gap Detection</h3>
          <p>Identify compliance gaps with clause-level similarity matching</p>
        </div>
        <div className="feature-card">
          <div className="feature-icon"><icons.brain /></div>
          <h3>AI Explanations</h3>
          <p>Get intelligent explanations for each compliance gap using AI</p>
        </div>
      </div>

      {apiStatus && (
        <div className="api-status-badge">
          <span className="status-dot connected"></span>
          API Connected • v{apiStatus.version}
        </div>
      )}
    </div>
  );

  // Render Analyze View
  const renderAnalyze = () => (
    <div className="analyze-view">
      <div className="page-header">
        <button className="btn btn-ghost" onClick={() => setView('home')}>
          <icons.arrowLeft /> Back
        </button>
        <h2>New Compliance Analysis</h2>
      </div>

      <div className="upload-section">
        <div 
          className={`upload-card ${regFile ? 'has-file' : ''}`}
          onClick={() => regInputRef.current?.click()}
        >
          {regFile ? (
            <div className="file-preview">
              <div className="file-icon success"><icons.check /></div>
              <span className="file-name">{regFile.name}</span>
              <button className="btn-remove" onClick={(e) => { e.stopPropagation(); setRegFile(null); }}>
                <icons.x />
              </button>
            </div>
          ) : (
            <div className="upload-placeholder">
              <div className="upload-icon"><icons.upload /></div>
              <h3>Regulatory Document</h3>
              <p>Click to upload or drag and drop</p>
              <span className="file-hint">PDF files only</span>
            </div>
          )}
          <input
            ref={regInputRef}
            type="file"
            accept=".pdf"
            hidden
            onChange={(e) => setRegFile(e.target.files[0])}
          />
        </div>

        <div className="upload-arrow">
          <icons.arrowRight />
        </div>

        <div 
          className={`upload-card ${policyFile ? 'has-file' : ''}`}
          onClick={() => policyInputRef.current?.click()}
        >
          {policyFile ? (
            <div className="file-preview">
              <div className="file-icon success"><icons.check /></div>
              <span className="file-name">{policyFile.name}</span>
              <button className="btn-remove" onClick={(e) => { e.stopPropagation(); setPolicyFile(null); }}>
                <icons.x />
              </button>
            </div>
          ) : (
            <div className="upload-placeholder">
              <div className="upload-icon"><icons.upload /></div>
              <h3>Internal Policy</h3>
              <p>Click to upload or drag and drop</p>
              <span className="file-hint">PDF files only</span>
            </div>
          )}
          <input
            ref={policyInputRef}
            type="file"
            accept=".pdf"
            hidden
            onChange={(e) => setPolicyFile(e.target.files[0])}
          />
        </div>
      </div>

      <div className="settings-section">
        <h3>Analysis Settings</h3>
        
        <div className="setting-item">
          <label>Similarity Threshold: {threshold}</label>
          <input 
            type="range" 
            min="0.1" 
            max="1" 
            step="0.05" 
            value={threshold}
            onChange={(e) => setThreshold(parseFloat(e.target.value))}
          />
          <div className="range-labels">
            <span>Strict (0.1)</span>
            <span>Lenient (1.0)</span>
          </div>
        </div>

        <div className="setting-item toggle">
          <label>
            <input 
              type="checkbox" 
              checked={useAI}
              onChange={(e) => setUseAI(e.target.checked)}
            />
            <span className="toggle-slider"></span>
            Enable AI Explanations
          </label>
        </div>

        {useAI && (
          <div className="setting-item">
            <label>Gemini API Key (optional)</label>
            <input 
              type="password" 
              placeholder="Enter your Gemini API key"
              value={geminiKey}
              onChange={(e) => setGeminiKey(e.target.value)}
            />
            <p className="setting-hint">Leave empty if GEMINI_API_KEY is set in .env</p>
          </div>
        )}
      </div>

      <button 
        className="btn btn-primary btn-large btn-full" 
        onClick={handleAnalyze}
        disabled={loading || !regFile || !policyFile}
      >
        {loading ? (
          <><icons.loader /> Analyzing...</>
        ) : (
          <>Analyze Documents</>
        )}
      </button>
    </div>
  );

  // Render Results View
  const renderResults = () => {
    if (!results) return null;

    const { total_clauses, compliant, partial, missing, risk_score, results: items } = results;

    // Calculate percentages for pie chart
    const total = total_clauses || 1;
    const compliantPct = (compliant / total) * 100;
    const partialPct = (partial / total) * 100;
    const missingPct = (missing / total) * 100;

    // Pie chart calculations
    const radius = 70;
    const circumference = 2 * Math.PI * radius;
    const compliantOffset = circumference - (compliantPct / 100) * circumference;
    const partialOffset = circumference - (partialPct / 100) * circumference;
    const missingOffset = circumference - (missingPct / 100) * circumference;

    // Export to CSV
    const exportCSV = () => {
      const headers = ['Status', 'Similarity', 'Regulatory Text', 'Policy Match', 'Explanation'];
      const rows = items.map(item => [
        item.status,
        `${Math.round(item.similarity * 100)}%`,
        item.regulatory_text.replace(/,/g, ';'),
        item.policy_match.replace(/,/g, ';'),
        (item.explanation || '').replace(/,/g, ';')
      ]);
      
      const csvContent = [headers, ...rows].map(row => row.join(',')).join('\n');
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = `compliance_report_${new Date().toISOString().slice(0,10)}.csv`;
      link.click();
    };

    // Print / Save as PDF
    const exportPDF = () => {
      const printContent = `
        <html>
        <head>
          <title>Compliance Report</title>
          <style>
            body { font-family: Arial, sans-serif; padding: 40px; }
            h1 { color: #333; }
            .summary { display: flex; gap: 20px; margin: 20px 0; flex-wrap: wrap; }
            .summary-card { padding: 15px; border-radius: 8px; background: #f5f5f5; }
            .status-compliant { color: green; }
            .status-partial { color: orange; }
            .status-missing { color: red; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
            th { background: #f5f5f5; }
          </style>
        </head>
        <body>
          <h1>Compliance Analysis Report</h1>
          <p>Generated: ${new Date().toLocaleString()}</p>
          <div class="summary">
            <div class="summary-card"><strong>Total:</strong> ${total_clauses}</div>
            <div class="summary-card"><strong>Compliant:</strong> ${compliant}</div>
            <div class="summary-card"><strong>Partial:</strong> ${partial}</div>
            <div class="summary-card"><strong>Missing:</strong> ${missing}</div>
            <div class="summary-card"><strong>Risk:</strong> ${risk_score}</div>
          </div>
          <table>
            <thead><tr><th>Status</th><th>Match %</th><th>Regulatory Text</th><th>Policy Match</th></tr></thead>
            <tbody>
              ${items.map(item => `
                <tr>
                  <td class="status-${item.status.toLowerCase()}">${item.status}</td>
                  <td>${Math.round(item.similarity * 100)}%</td>
                  <td>${item.regulatory_text.substring(0, 100)}...</td>
                  <td>${item.policy_match.substring(0, 100)}...</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </body>
        </html>
      `;
      
      const printWindow = window.open('', '_blank');
      printWindow.document.write(printContent);
      printWindow.document.close();
      printWindow.print();
    };

    return (
      <div className="results-view">
        <div className="page-header">
          <button className="btn btn-ghost" onClick={() => setView('analyze')}>
            <icons.arrowLeft /> New Analysis
          </button>
          <h2>Analysis Results</h2>
          <div className="export-buttons">
            <button className="btn btn-secondary" onClick={exportCSV}>
              <icons.download /> Export CSV
            </button>
            <button className="btn btn-secondary" onClick={exportPDF}>
              <icons.print /> Print / PDF
            </button>
          </div>
        </div>

        {/* Charts Section */}
        <div className="charts-section">
          <div className="charts-toggle">
            <button 
              className={`chart-btn ${chartView === 'pie' ? 'active' : ''}`}
              onClick={() => setChartView('pie')}
            >
              <icons.pie /> Pie Chart
            </button>
            <button 
              className={`chart-btn ${chartView === 'bar' ? 'active' : ''}`}
              onClick={() => setChartView('bar')}
            >
              <icons.bar /> Bar Chart
            </button>
          </div>

          {chartView === 'pie' ? (
            <div className="pie-chart-container">
              <svg viewBox="0 0 200 200" className="pie-chart">
                {/* Background circle */}
                <circle cx="100" cy="100" r="70" fill="none" stroke="var(--bg-tertiary)" strokeWidth="30" />
                {/* Compliant segment */}
                <circle 
                  cx="100" cy="100" r="70" 
                  fill="none" 
                  stroke="var(--success)" 
                  strokeWidth="30"
                  strokeDasharray={`${(compliantPct / 100) * 440} ${440 - (compliantPct / 100) * 440}`}
                  strokeDashoffset="0"
                  transform="rotate(-90 100 100)"
                />
                {/* Partial segment */}
                <circle 
                  cx="100" cy="100" r="70" 
                  fill="none" 
                  stroke="var(--warning)" 
                  strokeWidth="30"
                  strokeDasharray={`${(partialPct / 100) * 440} ${440 - (partialPct / 100) * 440}`}
                  strokeDashoffset={`-${(compliantPct / 100) * 440}`}
                  transform="rotate(-90 100 100)"
                />
                {/* Missing segment */}
                <circle 
                  cx="100" cy="100" r="70" 
                  fill="none" 
                  stroke="var(--danger)" 
                  strokeWidth="30"
                  strokeDasharray={`${(missingPct / 100) * 440} ${440 - (missingPct / 100) * 440}`}
                  strokeDashoffset={`-${((compliantPct + partialPct) / 100) * 440}`}
                  transform="rotate(-90 100 100)"
                />
              </svg>
              <div className="pie-legend">
                <div className="legend-item">
                  <span className="legend-dot success"></span>
                  <span>Compliant ({compliant})</span>
                  <span className="legend-pct">{Math.round(compliantPct)}%</span>
                </div>
                <div className="legend-item">
                  <span className="legend-dot warning"></span>
                  <span>Partial ({partial})</span>
                  <span className="legend-pct">{Math.round(partialPct)}%</span>
                </div>
                <div className="legend-item">
                  <span className="legend-dot danger"></span>
                  <span>Missing ({missing})</span>
                  <span className="legend-pct">{Math.round(missingPct)}%</span>
                </div>
              </div>
            </div>
          ) : (
            <div className="bar-chart-container">
              <div className="bar-chart">
                <div className="bar-item">
                  <span className="bar-label">Compliant</span>
                  <div className="bar-track">
                    <div className="bar-fill success" style={{width: `${compliantPct}%`}}></div>
                  </div>
                  <span className="bar-value">{compliant} ({Math.round(compliantPct)}%)</span>
                </div>
                <div className="bar-item">
                  <span className="bar-label">Partial</span>
                  <div className="bar-track">
                    <div className="bar-fill warning" style={{width: `${partialPct}%`}}></div>
                  </div>
                  <span className="bar-value">{partial} ({Math.round(partialPct)}%)</span>
                </div>
                <div className="bar-item">
                  <span className="bar-label">Missing</span>
                  <div className="bar-track">
                    <div className="bar-fill danger" style={{width: `${missingPct}%`}}></div>
                  </div>
                  <span className="bar-value">{missing} ({Math.round(missingPct)}%)</span>
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="results-summary">
          <div className="summary-card total">
            <span className="summary-value">{total_clauses}</span>
            <span className="summary-label">Total Clauses</span>
          </div>
          <div className="summary-card compliant">
            <span className="summary-value">{compliant}</span>
            <span className="summary-label">Compliant</span>
          </div>
          <div className="summary-card partial">
            <span className="summary-value">{partial}</span>
            <span className="summary-label">Partial</span>
          </div>
          <div className="summary-card missing">
            <span className="summary-value">{missing}</span>
            <span className="summary-label">Missing</span>
          </div>
          <div className={`summary-card risk ${risk_score > 10 ? 'high' : risk_score > 5 ? 'medium' : 'low'}`}>
            <span className="summary-value">{risk_score}</span>
            <span className="summary-label">Risk Score</span>
          </div>
        </div>

        {/* Filter Buttons */}
        <div className="results-filter">
          <button 
            className={`filter-btn ${filterView === 'all' ? 'active' : ''}`}
            onClick={() => setFilterView('all')}
          >
            All ({total_clauses})
          </button>
          <button 
            className={`filter-btn success ${filterView === 'Compliant' ? 'active' : ''}`}
            onClick={() => setFilterView('Compliant')}
          >
            <icons.check /> Compliant ({compliant})
          </button>
          <button 
            className={`filter-btn warning ${filterView === 'Partial' ? 'active' : ''}`}
            onClick={() => setFilterView('Partial')}
          >
            <icons.alert /> Partial ({partial})
          </button>
          <button 
            className={`filter-btn danger ${filterView === 'Missing' ? 'active' : ''}`}
            onClick={() => setFilterView('Missing')}
          >
            <icons.x /> Missing ({missing})
          </button>
        </div>

        <div className="results-list">
          {items.filter(item => filterView === 'all' || item.status === filterView).map((item, index) => (
            <div key={index} className={`result-card ${item.status.toLowerCase()}`}>
              <div className="result-header">
                <span className={`status-badge ${item.status.toLowerCase()}`}>
                  {item.status === 'Compliant' && <icons.check />}
                  {item.status === 'Partial' && <icons.alert />}
                  {item.status === 'Missing' && <icons.x />}
                  {item.status}
                </span>
                <span className="similarity-score">
                  {Math.round(item.similarity * 100)}% match
                </span>
              </div>
              
              <div className="result-content">
                <div className="clause-section">
                  <h4>Regulatory Requirement</h4>
                  <p>{item.regulatory_text}</p>
                </div>
                <div className="clause-section">
                  <h4>Policy Match</h4>
                  <p>{item.policy_match}</p>
                </div>
              </div>

              {item.explanation && (
                <div className="ai-explanation">
                  <div className="explanation-header">
                    <icons.brain /> AI Explanation
                  </div>
                  <p>{item.explanation}</p>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    );
  };

  // Render History View
  const renderHistory = () => (
    <div className="history-view">
      <div className="page-header">
        <button className="btn btn-ghost" onClick={() => setView('home')}>
          <icons.arrowLeft /> Back
        </button>
        <h2>Analysis History</h2>
      </div>

      {history.length === 0 ? (
        <div className="empty-state">
          <icons.history />
          <h3>No analysis history</h3>
          <p>Start a new analysis to see it here</p>
          <button className="btn btn-primary" onClick={() => setView('analyze')}>
            Start Analysis
          </button>
        </div>
      ) : (
        <div className="history-list">
          {history.map((item) => (
            <div key={item.id} className="history-card" onClick={() => loadFromHistory(item.id)}>
              <div className="history-info">
                <h4>{item.reg_file_name} vs {item.policy_file_name}</h4>
                <span className="history-date">{new Date(item.timestamp).toLocaleString()}</span>
              </div>
              <div className="history-stats">
                <span className="stat compliant">{item.compliant} ✓</span>
                <span className="stat partial">~{item.partial}</span>
                <span className="stat missing">✗ {item.missing}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="sidebar-header">
          <div className="logo">
            <icons.shield />
          </div>
          <div className="brand">
            <span className="brand-name">ComplianceAI</span>
            <span className="brand-tag">Regulatory Copilot</span>
          </div>
        </div>

        <nav className="sidebar-nav">
          <button 
            className={`nav-item ${view === 'home' ? 'active' : ''}`}
            onClick={() => setView('home')}
          >
            <icons.shield /> Dashboard
          </button>
          <button 
            className={`nav-item ${view === 'analyze' ? 'active' : ''}`}
            onClick={() => setView('analyze')}
          >
            <icons.upload /> New Analysis
          </button>
          <button 
            className={`nav-item ${view === 'history' ? 'active' : ''}`}
            onClick={() => setView('history')}
          >
            <icons.history /> History
          </button>
        </nav>

        <div className="sidebar-theme">
          <button className="nav-item theme-toggle" onClick={toggleTheme}>
            {theme === 'dark' ? <MoonIcon /> : <SunIcon />}
            {theme === 'dark' ? 'Dark Mode' : 'Light Mode'}
          </button>
        </div>

        <div className="sidebar-footer">
          <div className="api-status">
            {apiStatus ? (
              <>
                <span className="status-dot connected"></span>
                API Connected
              </>
            ) : (
              <>
                <span className="status-dot disconnected"></span>
                API Offline
              </>
            )}
          </div>
        </div>
      </aside>

      <main className="main-content">
        {view === 'home' && renderHome()}
        {view === 'analyze' && renderAnalyze()}
        {view === 'results' && renderResults()}
        {view === 'history' && renderHistory()}
      </main>
    </div>
  );
}

export default App;
