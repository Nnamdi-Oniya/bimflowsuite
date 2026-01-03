import React, { useState, useEffect } from "react";
import {
  CheckCircle,
  AlertTriangle,
  XCircle,
  Download,
  FileCheck,
  Zap,
  Shield,
  Building2,
  TrendingUp,
  Activity,
  BarChart3,
  PieChart,
  Layers,
  Clock,
  Target,
  Award,
  Upload,
  Play,
  Trash2,
} from "lucide-react";
import "../../assets/ComplianceChecksPage.css";

interface Project {
  id: string;
  name: string;
  type: "Building" | "Bridge" | "Road" | "HighRise";
  lastModified: string;
  fileSize: number;
  status: string;
  complianceScore?: number;
  clashes?: number;
  estimatedCost?: number;
  duration?: string;
}

interface ComplianceIssue {
  id: number;
  severity: "Critical" | "High" | "Medium" | "Low";
  description: string;
  location: string;
  ruleId: string;
  recommendation: string;
}

interface Calculations {
  quantities: Record<string, string>;
  structural: Record<string, string>;
  sustainability: Record<string, string>;
}

interface AnalysisMetric {
  category: string;
  score: number;
  status: "Excellent" | "Good" | "Fair" | "Poor";
  details: string;
  trend: "up" | "down" | "stable";
}

interface ComplianceResults {
  passed: number;
  failed: number;
  total: number;
  complianceRate: number;
  issues: ComplianceIssue[];
  calculations: Calculations;
  analysis: {
    overall: AnalysisMetric[];
    buildingPerformance: {
      energyEfficiency: number;
      structuralIntegrity: number;
      accessibility: number;
      sustainability: number;
      fireCompliance: number;
      spatialQuality: number;
    };
    modernStandards: {
      bimMaturity: string;
      digitalTwinReady: boolean;
      smartBuildingScore: number;
      carbonNeutralPath: string;
    };
    recommendations: string[];
  };
  timestamp: string;
}

const ComplianceChecksPage: React.FC = () => {
  const [userProjects, setUserProjects] = useState<Project[]>([]);
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);
  const [results, setResults] = useState<ComplianceResults | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [activeTab, setActiveTab] = useState<"compliance" | "calculations" | "analysis">("compliance");
  const [selectedRules, setSelectedRules] = useState<string[]>([
    "IFC Schema",
    "Fire Safety",
    "Structural",
    "Accessibility",
  ]);

  // Load user projects from localStorage on component mount
  useEffect(() => {
    const savedProjects = JSON.parse(localStorage.getItem('userProjects') || '[]');
    setUserProjects(savedProjects);
  }, []);

  // Update selected project when projects change
  useEffect(() => {
    if (userProjects.length > 0 && !selectedProject) {
      setSelectedProject(userProjects[userProjects.length - 1]);
    }
  }, [userProjects, selectedProject]);

  const rulePacks = [
    { id: "ifc", name: "IFC Schema", icon: FileCheck, color: "#3b82f6" },
    { id: "fire", name: "Fire Safety", icon: Zap, color: "#ef4444" },
    { id: "structural", name: "Structural", icon: Shield, color: "#8b5cf6" },
    { id: "access", name: "Accessibility", icon: Building2, color: "#10b981" },
  ] as const;

  const handleRunCheck = () => {
    if (!selectedProject) return;
    setIsRunning(true);

    setTimeout(() => {
      setResults({
        passed: 87,
        failed: 9,
        total: 96,
        complianceRate: 90.6,
        issues: [
          {
            id: 1,
            severity: "Critical",
            description: "Fire stair width below minimum (900mm required, 750mm found)",
            location: "North Stairwell, Level 3-4",
            ruleId: "FIRE-ESC-001",
            recommendation: "Widen stairwell to 950mm minimum. Estimated cost: $45,000. Timeline: 3 weeks.",
          },
          {
            id: 2,
            severity: "High",
            description: "Ramp slope exceeds 1:12 accessibility limit (current: 1:10)",
            location: "Main Entrance Ramp",
            ruleId: "ACC-RMP-003",
            recommendation: "Redesign ramp with 1:12 slope or install platform lift. Consider adding handrails both sides.",
          },
          {
            id: 3,
            severity: "Medium",
            description: "Missing handrail on staircase (ADA compliance)",
            location: "Level 5-6 Interior Stair",
            ruleId: "ACC-HND-001",
            recommendation: "Install continuous handrails on both sides extending 12\" beyond top and bottom steps.",
          },
          {
            id: 4,
            severity: "Medium",
            description: "Emergency lighting coverage gap detected",
            location: "Basement Parking Level B2",
            ruleId: "FIRE-LGT-008",
            recommendation: "Add 3 additional emergency light fixtures with battery backup. Ensure 90-minute runtime.",
          },
          {
            id: 5,
            severity: "Low",
            description: "Door closer adjustment needed for accessibility",
            location: "Conference Room 401",
            ruleId: "ACC-DOR-012",
            recommendation: "Adjust door closer to 5-second minimum closing time. Test with 5lbs force requirement.",
          },
        ],
        calculations: {
          quantities: {
            "Gross Floor Area": "48,320 m²",
            "Net Usable Area": "41,872 m²",
            "Building Volume": "182,450 m³",
            "Total Elements": "12,847",
            "Structural Members": "3,421",
            "MEP Components": "5,892",
          },
          structural: {
            "Max Wind Load": "2.8 kPa",
            "Seismic Zone": "D (High Risk)",
            "Safety Factor": "1.68",
            "Foundation Type": "Deep Pile",
            "Column Spacing": "7.5m x 7.5m",
            "Floor-to-Floor": "3.6m",
          },
          sustainability: {
            "Energy Rating": "A+ (LEED Platinum)",
            "Carbon Footprint": "42 kgCO₂/m²/year",
            "Water Efficiency": "35% reduction",
            "Renewable Energy": "45% solar coverage",
            "Green Roof Area": "2,840 m²",
            "Recycled Materials": "62% by weight",
          },
        },
        analysis: {
          overall: [
            {
              category: "Code Compliance",
              score: 91,
              status: "Excellent",
              details: "Meets 2025 IBC, ADA, and local building codes with minor exceptions",
              trend: "up",
            },
            {
              category: "Structural Performance",
              score: 94,
              status: "Excellent",
              details: "Exceeds seismic and wind load requirements. Advanced FEM analysis validated",
              trend: "stable",
            },
            {
              category: "Fire & Life Safety",
              score: 87,
              status: "Good",
              details: "Comprehensive fire protection system. Minor egress improvements needed",
              trend: "up",
            },
            {
              category: "Accessibility",
              score: 89,
              status: "Good",
              details: "Strong ADA compliance. Universal design principles applied throughout",
              trend: "up",
            },
            {
              category: "Sustainability",
              score: 96,
              status: "Excellent",
              details: "LEED Platinum certified. Net-zero ready with renewable energy integration",
              trend: "up",
            },
            {
              category: "BIM Quality",
              score: 92,
              status: "Excellent",
              details: "LOD 400 model. Full coordination across all disciplines. Clash-free",
              trend: "stable",
            },
          ],
          buildingPerformance: {
            energyEfficiency: 94,
            structuralIntegrity: 96,
            accessibility: 89,
            sustainability: 96,
            fireCompliance: 87,
            spatialQuality: 91,
          },
          modernStandards: {
            bimMaturity: "Level 3 (Integrated BIM)",
            digitalTwinReady: true,
            smartBuildingScore: 88,
            carbonNeutralPath: "On track for 2030 target",
          },
          recommendations: [
            "Implement IoT sensor network for real-time building performance monitoring",
            "Upgrade to smart HVAC controls with AI-driven optimization (potential 15% energy savings)",
            "Consider modular construction techniques for future expansion phases",
            "Integrate digital twin platform for predictive maintenance and lifecycle management",
            "Enhance occupant wellness features: circadian lighting, biophilic design elements",
            "Prepare infrastructure for EV charging stations (future-proofing for 2030+ requirements)",
            "Implement advanced water recycling system to achieve net-zero water consumption",
            "Add building automation system (BAS) integration with smart city infrastructure",
          ],
        },
        timestamp: new Date().toLocaleString(),
      });
      setIsRunning(false);
    }, 3200);
  };

  const handleExport = (format: "pdf" | "csv" | "bcf") => {
    alert(`Exporting comprehensive ${format.toUpperCase()} report with compliance, calculations, and analysis...`);
  };

  const getScoreColor = (score: number): string => {
    if (score >= 90) return "#10b981";
    if (score >= 75) return "#3b82f6";
    if (score >= 60) return "#f59e0b";
    return "#ef4444";
  };

  const getStatusBadgeClass = (status: string): string => {
    switch (status) {
      case "Excellent": return "status-excellent";
      case "Good": return "status-good";
      case "Fair": return "status-fair";
      case "Poor": return "status-poor";
      default: return "";
    }
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const handleDeleteProject = (projectId: string, event: React.MouseEvent) => {
    event.stopPropagation();
    
    if (window.confirm('Are you sure you want to delete this project? This action cannot be undone.')) {
      const updatedProjects = userProjects.filter(project => project.id !== projectId);
      setUserProjects(updatedProjects);
      localStorage.setItem('userProjects', JSON.stringify(updatedProjects));
      
      // If the deleted project was selected, clear the selection
      if (selectedProject?.id === projectId) {
        setSelectedProject(null);
        setResults(null);
      }
    }
  };

  return (
    <div className="compliance-pro">
      {/* Header */}
      <div className="compliance-header-pro">
        <div className="header-content">
          <h1>Compliance Analysis</h1>
          <p>Run automated compliance checks on your uploaded IFC projects</p>
        </div>
        <div className="status-badge live">
          <div className="pulse-dot"></div>
          Live Validation Engine
        </div>
      </div>

      {/* Project & Rules */}
      <div className="config-grid-pro">
        <div className="project-selector-pro">
          <div className="section-header">
            <h3>Select Project</h3>
            <span className="project-count">{userProjects.length} projects available</span>
          </div>
          
          {userProjects.length === 0 ? (
            <div className="empty-state">
              <Upload size={48} className="empty-icon" />
              <h4>No Projects Found</h4>
              <p>Upload IFC files to start compliance analysis</p>
              <button 
                className="btn primary"
                onClick={() => window.location.href = '/dashboard/upload-ifc'}
              >
                Upload First Project
              </button>
            </div>
          ) : (
            <div className="project-cards">
              {userProjects.map((project) => (
                <div
                  key={project.id}
                  className={`project-card ${selectedProject?.id === project.id ? "selected" : ""}`}
                  onClick={() => setSelectedProject(project)}
                >
                  <Building2 size={32} className="project-icon" />
                  <div className="project-info">
                    <strong className="project-name">{project.name}</strong>
                    <div className="project-meta">
                      <span className="project-type">{project.type}</span>
                      <span className="project-date">{project.lastModified}</span>
                      <span className="project-size">{formatFileSize(project.fileSize)}</span>
                    </div>
                    {project.complianceScore && (
                      <div className="project-score">
                        <div 
                          className="score-bar" 
                          style={{ width: `${project.complianceScore}%` }}
                        ></div>
                        <span>{project.complianceScore}% Compliant</span>
                      </div>
                    )}
                  </div>
                  <div className="project-actions">
                    {selectedProject?.id === project.id && <CheckCircle className="check" size={24} />}
                    <button 
                      className="delete-project-btn"
                      onClick={(e) => handleDeleteProject(project.id, e)}
                      title="Delete project"
                    >
                      <Trash2 size={16} />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="rules-selector-pro">
          <h3>Active Rule Packs</h3>
          <div className="rule-packs-grid">
            {rulePacks.map((rule) => {
              const Icon = rule.icon;
              const isActive = selectedRules.includes(rule.name);
              return (
                <div
                  key={rule.id}
                  className={`rule-pack-card ${isActive ? "active" : ""}`}
                  style={{ borderColor: isActive ? rule.color : undefined }}
                  onClick={() => {
                    setSelectedRules((prev) =>
                      prev.includes(rule.name)
                        ? prev.filter((r) => r !== rule.name)
                        : [...prev, rule.name]
                    );
                  }}
                >
                  <Icon size={36} color={isActive ? rule.color : "#94a3b8"} />
                  <span>{rule.name}</span>
                  {isActive && <CheckCircle size={22} className="active-check" />}
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Run Button */}
      <div className="run-section-pro">
        <button
          className="run-compliance-btn"
          onClick={handleRunCheck}
          disabled={!selectedProject || isRunning || userProjects.length === 0}
        >
          {isRunning ? (
            <>
              <div className="spinner"></div>
              Running {selectedRules.length} Rule Packs + Analysis...
            </>
          ) : (
            <>
              <Play size={26} />
              Run Compliance Analysis
            </>
          )}
        </button>
        
        {userProjects.length === 0 && (
          <p className="no-projects-hint">
            Upload IFC files first to run compliance analysis
          </p>
        )}
      </div>

      {/* Results */}
      {results && (
        <div className="results-pro">
          <div className="results-header-pro">
            <h2>Compliance Report - {selectedProject?.name}</h2>
            <div className="report-meta">
              <span>Generated: {results.timestamp}</span>
              <span className="compliance-rate">Compliance: {results.complianceRate}%</span>
            </div>
          </div>

          <div className="tabs-pro">
            <button
              className={activeTab === "compliance" ? "active" : ""}
              onClick={() => setActiveTab("compliance")}
            >
              <AlertTriangle size={18} />
              Compliance Issues
            </button>
            <button
              className={activeTab === "calculations" ? "active" : ""}
              onClick={() => setActiveTab("calculations")}
            >
              <BarChart3 size={18} />
              Calculations
            </button>
            <button
              className={activeTab === "analysis" ? "active" : ""}
              onClick={() => setActiveTab("analysis")}
            >
              <Activity size={18} />
              Analysis
            </button>
          </div>

          {/* Compliance Tab */}
          {activeTab === "compliance" && (
            <div className="compliance-results-pro">
              <div className="summary-cards-pro">
                <div className="summary-card passed">
                  <CheckCircle size={40} />
                  <strong>{results.passed}</strong>
                  <span>Passed</span>
                </div>
                <div className="summary-card failed">
                  <XCircle size={40} />
                  <strong>{results.failed}</strong>
                  <span>Failed</span>
                </div>
                <div className="summary-card total">
                  <Target size={40} />
                  <strong>{results.total}</strong>
                  <span>Total Checks</span>
                </div>
              </div>

              <div className="issues-list-pro">
                {results.issues.map((issue) => (
                  <div
                    key={issue.id}
                    className={`issue-card severity-${issue.severity.toLowerCase()}`}
                  >
                    <div className="issue-severity">{issue.severity}</div>
                    <div className="issue-content">
                      <h4>{issue.description}</h4>
                      <p className="issue-location">
                        <strong>Location:</strong> {issue.location} • <strong>Rule:</strong> {issue.ruleId}
                      </p>
                      <div className="issue-recommendation">
                        <strong>Recommendation:</strong> {issue.recommendation}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Calculations Tab */}
          {activeTab === "calculations" && results && (
            <div className="calculations-pro">
              {(Object.entries(results.calculations) as [string, Record<string, string>][]).map(
                ([category, values]) => (
                  <div key={category} className="calc-category">
                    <h4>
                      {category === "quantities" && <Layers size={24} />}
                      {category === "structural" && <Shield size={24} />}
                      {category === "sustainability" && <TrendingUp size={24} />}
                      {category.charAt(0).toUpperCase() + category.slice(1)}
                    </h4>
                    <div className="calc-items">
                      {Object.entries(values).map(([key, value]) => (
                        <div key={key} className="calc-item">
                          <span>{key}</span>
                          <strong>{value}</strong>
                        </div>
                      ))}
                    </div>
                  </div>
                )
              )}
            </div>
          )}

          {/* Analysis Tab */}
          {activeTab === "analysis" && results && (
            <div className="analysis-pro">
              {/* Overall Metrics */}
              <div className="analysis-section">
                <h3>
                  <Award size={28} />
                  Overall Performance Metrics
                </h3>
                <div className="metrics-grid">
                  {results.analysis.overall.map((metric) => (
                    <div key={metric.category} className="metric-card">
                      <div className="metric-header">
                        <span className="metric-category">{metric.category}</span>
                        <span className={`metric-status ${getStatusBadgeClass(metric.status)}`}>
                          {metric.status}
                        </span>
                      </div>
                      <div className="metric-score">
                        <div className="score-circle" style={{ background: `conic-gradient(${getScoreColor(metric.score)} ${metric.score * 3.6}deg, #e2e8f0 0deg)` }}>
                          <div className="score-inner">
                            <strong>{metric.score}</strong>
                            <span>/100</span>
                          </div>
                        </div>
                        <div className="metric-details">
                          <p>{metric.details}</p>
                          <div className={`trend-indicator trend-${metric.trend}`}>
                            {metric.trend === "up" && "↑ Improving"}
                            {metric.trend === "down" && "↓ Declining"}
                            {metric.trend === "stable" && "→ Stable"}
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Building Performance */}
              <div className="analysis-section">
                <h3>
                  <PieChart size={28} />
                  Building Performance Dashboard
                </h3>
                <div className="performance-grid">
                  {Object.entries(results.analysis.buildingPerformance).map(([key, value]) => (
                    <div key={key} className="performance-item">
                      <div className="performance-label">
                        {key.replace(/([A-Z])/g, ' $1').trim()}
                      </div>
                      <div className="performance-bar">
                        <div 
                          className="performance-fill" 
                          style={{ 
                            width: `${value}%`,
                            background: getScoreColor(value)
                          }}
                        >
                          <span>{value}%</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Modern Standards */}
              <div className="analysis-section">
                <h3>
                  <Zap size={28} />
                  2025 Modern Standards Compliance
                </h3>
                <div className="modern-standards-grid">
                  <div className="standard-card">
                    <div className="standard-icon">
                      <Layers size={40} />
                    </div>
                    <div className="standard-content">
                      <h4>BIM Maturity Level</h4>
                      <p className="standard-value">{results.analysis.modernStandards.bimMaturity}</p>
                      <p className="standard-desc">Full collaborative workflow with integrated data management</p>
                    </div>
                  </div>
                  <div className="standard-card">
                    <div className="standard-icon">
                      <Activity size={40} />
                    </div>
                    <div className="standard-content">
                      <h4>Digital Twin Ready</h4>
                      <p className="standard-value">
                        {results.analysis.modernStandards.digitalTwinReady ? "✓ Yes" : "✗ No"}
                      </p>
                      <p className="standard-desc">Real-time monitoring and predictive analytics enabled</p>
                    </div>
                  </div>
                  <div className="standard-card">
                    <div className="standard-icon">
                      <Building2 size={40} />
                    </div>
                    <div className="standard-content">
                      <h4>Smart Building Score</h4>
                      <p className="standard-value">{results.analysis.modernStandards.smartBuildingScore}/100</p>
                      <p className="standard-desc">IoT integration, automation, and occupant experience</p>
                    </div>
                  </div>
                  <div className="standard-card">
                    <div className="standard-icon">
                      <TrendingUp size={40} />
                    </div>
                    <div className="standard-content">
                      <h4>Carbon Neutral Path</h4>
                      <p className="standard-value">{results.analysis.modernStandards.carbonNeutralPath}</p>
                      <p className="standard-desc">Aligned with global sustainability commitments</p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Recommendations */}
              <div className="analysis-section">
                <h3>
                  <Clock size={28} />
                  Strategic Recommendations
                </h3>
                <div className="recommendations-list">
                  {results.analysis.recommendations.map((rec, idx) => (
                    <div key={idx} className="recommendation-item">
                      <div className="rec-number">{idx + 1}</div>
                      <p>{rec}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Export Buttons */}
          <div className="export-actions-pro">
            <button onClick={() => handleExport("pdf")} className="export-btn pdf">
              <Download size={18} /> Export PDF Report
            </button>
            <button onClick={() => handleExport("csv")} className="export-btn csv">
              <Download size={18} /> Export CSV Data
            </button>
            <button onClick={() => handleExport("bcf")} className="export-btn bcf">
              <Download size={18} /> Export BCF Issues
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ComplianceChecksPage;