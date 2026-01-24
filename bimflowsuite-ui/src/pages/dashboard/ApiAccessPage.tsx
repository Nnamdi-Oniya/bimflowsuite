// src/pages/dashboard/ApiAccessPage.tsx – FIXED & ALWAYS WORKS
import React, { useState } from "react";
import "../../assets/ApiAccessPage.css";

const ApiAccessPage: React.FC = () => {
  // Fake key for demo / until you generate real ones
  const [copied, setCopied] = useState(false);

  // Replace this later with real user API key from your backend
  const API_KEY = "bf_4f8a9c2e7d91b3f6e8d5a1c9b2e7f6d8a3c5e9f1"; // ← Demo key (safe to show partially)

  const maskedKey = `${API_KEY.slice(0, 8)}••••••••${API_KEY.slice(-8)}`;

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(API_KEY);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      alert("Failed to copy – your browser may be blocking clipboard access.");
    }
  };

  return (
    <div className="dashboard-api">
      <div className="dashboard-api__header">
        <h1>API Access</h1>
        <p>Integrate BIMFlow Suite into Revit, Navisworks, Excel, Power BI, and custom tools</p>
      </div>

      <div className="api-card">
        {/* API Key Section */}
        <div className="api-key">
          <label>Your API Key</label>
          <div className="key-display">
            <code>{maskedKey}</code>
            <button
              className={`btn small primary ${copied ? "success" : ""}`}
              onClick={handleCopy}
            >
              {copied ? "✓ Copied!" : "Copy Key"}
            </button>
            <button className="btn small secondary" disabled>
              Regenerate (Coming Soon)
            </button>
          </div>
          <small style={{ color: "#888", marginTop: "8px", display: "block" }}>
            Keep this key secret • Never commit it to code
          </small>
        </div>

        {/* Quick Start Example */}
        <div className="api-docs">
          <h3>Quick Start Example</h3>
          <pre>
{`curl -X POST https://api.bimflowsuite.com/v1/generate \\
  -H "Authorization: Bearer ${API_KEY}" \\
  -H "Content-Type: application/json" \\
  -d '{
    "intent": "5-story office building with basement parking and green roof",
    "asset_pack": "office",
    "location": "Lagos, Nigeria",
    "standards": "NBC 2018"
  }'`}
          </pre>

          <div style={{ marginTop: "1.5rem" }}>
            <button className="btn primary" style={{ marginRight: "12px" }}>
              View Full API Documentation ↗
            </button>
            <button className="btn secondary">
              Download Postman Collection
            </button>
          </div>
        </div>

        {/* Rate Limits & Pricing Info */}
        <div className="api-info-grid" style={{ marginTop: "2rem", display: "grid", gap: "1rem", gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))" }}>
          <div className="info-card">
            <strong>Free Tier</strong>
            <p>50 requests / month</p>
          </div>
          <div className="info-card">
            <strong>Pro Tier</strong>
            <p>10,000 requests / month</p>
          </div>
          <div className="info-card">
            <strong>Enterprise</strong>
            <p>Unlimited + Dedicated Support</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ApiAccessPage;