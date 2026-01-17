import React, { useState } from "react";
import { AlertCircle, AlertTriangle, Info, Zap, Download, Bell } from "lucide-react";
import "../../assets/ClashDetectionPage.css";

interface Clash {
  id: number;
  type: "Hard Clash" | "Soft Clash" | "Workflow Clash";
  elements: string;
  location: string;
  severity: "Critical" | "High" | "Medium" | "Low";
  status: "New" | "In Review" | "Resolved";
}

const ClashDetectionPage: React.FC = () => {
  const [selectedClash, setSelectedClash] = useState<number | null>(null);
  const [hoveredClash, setHoveredClash] = useState<number | null>(null);

  const clashes: Clash[] = [
    { id: 1, type: "Hard Clash", elements: "Steel Beam vs HVAC Duct", location: "Level 5 - Grid A-3", severity: "Critical", status: "New" },
    { id: 2, type: "Soft Clash", elements: "Pipe vs Cable Tray", location: "Basement MEP Zone", severity: "High", status: "In Review" },
    { id: 3, type: "Hard Clash", elements: "Column vs Plumbing Riser", location: "Level 3 Core", severity: "Critical", status: "New" },
    { id: 4, type: "Workflow Clash", elements: "Rebar vs Formwork Sequence", location: "Foundation Pour 2", severity: "Medium", status: "Resolved" },
    { id: 5, type: "Soft Clash", elements: "Duct vs Lighting Fixtures", location: "Level 2 Ceiling Void", severity: "Low", status: "In Review" },
  ];

  const summary = {
    total: clashes.length,
    critical: clashes.filter(c => c.severity === "Critical").length,
    high: clashes.filter(c => c.severity === "High").length,
    medium: clashes.filter(c => c.severity === "Medium").length,
    low: clashes.filter(c => c.severity === "Low").length,
  };

  const getClashPosition = (id: number) => {
    const positions: Record<number, { top: string; left: string }> = {
      1: { top: "38%", left: "52%" },
      2: { top: "68%", left: "28%" },
      3: { top: "45%", left: "48%" },
      4: { top: "75%", left: "60%" },
      5: { top: "55%", left: "35%" },
    };
    return positions[id] || { top: "50%", left: "50%" };
  };

  return (
    <div className="clash-detection-pro">
      <div className="clash-header-pro">
        <div className="header-content">
          <h1>Clash Detection</h1>
          <p>8 clashes detected across disciplines • Last scan: <strong>5 minutes ago</strong></p>
        </div>
        <div className="scan-status">
          <Zap size={20} className="pulse" />
          <span>Live Monitoring Active</span>
        </div>
      </div>

      <div className="clash-grid-pro">
        {/* 3D Viewer */}
        <div className="viewer-container">
          <div className="viewer-card">
            <div className="viewer-header">
              <h3>3D Model Viewer</h3>
              <span className="view-mode">Federated IFC Model</span>
            </div>
            <div className="ifc-viewer">
              <div className="model-bg"></div>
              <div className="model-grid"></div>

              {clashes.map((clash) => {
                const pos = getClashPosition(clash.id);
                const isActive = selectedClash === clash.id || hoveredClash === clash.id;
                return (
                  <div
                    key={clash.id}
                    className={`clash-marker ${isActive ? "active" : ""} severity-${clash.severity.toLowerCase()}`}
                    style={{ top: pos.top, left: pos.left }}
                    onMouseEnter={() => setHoveredClash(clash.id)}
                    onMouseLeave={() => setHoveredClash(null)}
                  >
                    <div className="marker-pulse"></div>
                    <div className="marker-icon">
                      {clash.severity === "Critical" && <AlertCircle size={24} />}
                      {clash.severity === "High" && <AlertTriangle size={24} />}
                      {clash.severity === "Medium" && <Zap size={24} />}
                      {clash.severity === "Low" && <Info size={24} />}
                    </div>
                  </div>
                );
              })}

              <div className="viewer-overlay-text">
                <span>Interactive 3D Clash Visualization</span>
                <p>Hover or click clashes to highlight in model</p>
              </div>
            </div>
          </div>
        </div>

        {/* Clash List */}
        <div className="list-container">
          <div className="summary-grid">
            <div className="summary-card total">
              <AlertCircle size={32} />
              <div>
                <strong>{summary.total}</strong>
                <span>Total Clashes</span>
              </div>
            </div>
            <div className="summary-card critical">
              <strong>{summary.critical}</strong>
              <span>Critical</span>
            </div>
            <div className="summary-card high">
              <strong>{summary.high}</strong>
              <span>High</span>
            </div>
            <div className="summary-card medium">
              <strong>{summary.medium}</strong>
              <span>Medium</span>
            </div>
            <div className="summary-card low">
              <strong>{summary.low}</strong>
              <span>Low</span>
            </div>
          </div>

          <div className="clash-list-pro">
            <h3>Detected Clashes</h3>
            {clashes.map((clash) => (
              <div
                key={clash.id}
                className={`clash-card ${selectedClash === clash.id ? "selected" : ""} ${clash.status.toLowerCase().replace(" ", "-")}`}
                onClick={() => setSelectedClash(clash.id)}
                onMouseEnter={() => setHoveredClash(clash.id)}
                onMouseLeave={() => setHoveredClash(null)}
              >
                <div className="clash-card-header">
                  <div className="clash-type">
                    <span className={`status-dot ${clash.status.toLowerCase().replace(" ", "-")}`}></span>
                    {clash.type}
                  </div>
                  <div className={`severity-badge severity-${clash.severity.toLowerCase()}`}>
                    {clash.severity}
                  </div>
                </div>
                <h4>{clash.elements}</h4>
                <p className="location">{clash.location}</p>
                <div className="clash-status">Status: {clash.status}</div>
              </div>
            ))}
          </div>

          <div className="clash-actions-pro">
            <button className="btn primary">
              <Download size={18} /> Export BCF Report
            </button>
            <button className="btn secondary">
              <Bell size={18} /> Notify Team
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ClashDetectionPage;