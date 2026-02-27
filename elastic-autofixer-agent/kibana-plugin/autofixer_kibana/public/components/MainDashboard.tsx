import React, { useState } from 'react';
import { AutoFixerAPI } from '../services/api';

export const MainDashboard = () => {
  const [issues, setIssues] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedIssue, setSelectedIssue] = useState<any>(null);
  const [fixProposal, setFixProposal] = useState<any>(null);
  const [statusMsg, setStatusMsg] = useState("");

  // 1. Run Diagnosis
  const runScan = async () => {
    setLoading(true);
    setStatusMsg("Scanning cluster for inefficiencies...");
    const results = await AutoFixerAPI.diagnoseCluster();
    setIssues(results);
    setLoading(false);
    setStatusMsg(`Found ${results.length} issues.`);
  };

  // 2. Generate Fix
  const handleFixClick = async (issue: any) => {
    setSelectedIssue(issue);
    setStatusMsg("Consulting AI for solution...");
    setLoading(true);
    const proposal = await AutoFixerAPI.generateFix(issue);
    setFixProposal(proposal);
    setLoading(false);
    setStatusMsg("Fix generated! Review below.");
  };

  // 3. Apply Fix
  const handleApplyClick = async () => {
    if (!fixProposal) return;
    setLoading(true);
    setStatusMsg("Applying fix to cluster...");
    const result = await AutoFixerAPI.applyFix(fixProposal);
    setLoading(false);
    setStatusMsg(`Result: ${result.message}`);
    // Clear state after success
    if (result.status === 'success') {
      setFixProposal(null);
      setSelectedIssue(null);
      runScan(); // Refresh list
    }
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>🛠️ Elastic Auto-Fixer Agent</h1>
      
      <button 
        onClick={runScan} 
        style={{ padding: '10px 20px', fontSize: '16px', cursor: 'pointer', backgroundColor: '#0077cc', color: 'white', border: 'none', borderRadius: '4px' }}
        disabled={loading}
      >
        {loading ? "Processing..." : "🔍 Scan Cluster Now"}
      </button>

      <p><strong>Status:</strong> {statusMsg}</p>

      {/* List Issues */}
      <div style={{ marginTop: '20px' }}>
        {issues.map((issue) => (
          <div key={issue.issue_id} style={{ border: '1px solid #ddd', padding: '15px', marginBottom: '10px', borderRadius: '5px', backgroundColor: issue.severity === 'critical' ? '#fff0f0' : '#f9f9f9' }}>
            <h3>⚠️ {issue.category.toUpperCase()}: {issue.issue_id}</h3>
            <p>{issue.description}</p>
            <p><strong>Resource:</strong> {issue.affected_resource}</p>
            <button 
              onClick={() => handleFixClick(issue)}
              style={{ padding: '8px 15px', backgroundColor: '#28a745', color: 'white', border: 'none', cursor: 'pointer' }}
            >
              🪄 Auto-Fix with AI
            </button>
          </div>
        ))}
      </div>

      {/* Fix Proposal Modal (Simple Inline) */}
      {fixProposal && (
        <div style={{ marginTop: '30px', border: '2px solid #0077cc', padding: '20px', backgroundColor: '#eef7ff' }}>
          <h2>💡 AI Fix Proposal</h2>
          <p><strong>Explanation:</strong> {fixProposal.explanation}</p>
          <div style={{ display: 'flex', gap: '20px' }}>
            <div style={{ flex: 1 }}>
              <h4>Original Code:</h4>
              <pre style={{ background: '#eee', padding: '10px' }}>{JSON.stringify(fixProposal.original_code, null, 2)}</pre>
            </div>
            <div style={{ flex: 1 }}>
              <h4>Fixed Code:</h4>
              <pre style={{ background: '#d4edda', padding: '10px' }}>{JSON.stringify(fixProposal.fixed_code, null, 2)}</pre>
            </div>
          </div>
          <br />
          <button 
            onClick={handleApplyClick}
            style={{ padding: '10px 20px', backgroundColor: '#0077cc', color: 'white', border: 'none', fontSize: '16px', cursor: 'pointer' }}
          >
            🚀 Apply Fix Now
          </button>
          <button 
            onClick={() => setFixProposal(null)}
            style={{ marginLeft: '10px', padding: '10px 20px', backgroundColor: '#ccc', border: 'none', fontSize: '16px', cursor: 'pointer' }}
          >
            Cancel
          </button>
        </div>
      )}
    </div>
  );
};