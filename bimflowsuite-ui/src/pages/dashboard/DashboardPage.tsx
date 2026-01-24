import React from "react";
import { useNavigate } from "react-router-dom";
import "../../assets/DashboardPage.css";

// RESTORED DEMO IMAGES
import officeTower from "../../assets/images/office-tower.jpg";
import bridgeExpansion from "../../assets/images/bridge-expansion.jpg";
import urbanRoad from "../../assets/images/urban-road.jpg";

// Icons (consistent with sidebar)
const ProjectsIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <rect x="3" y="3" width="18" height="18" rx="2" />
    <path d="M3 9H21" />
    <path d="M9 21V9" />
  </svg>
);

const UploadIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M21 15V19C21 20.1 20.1 21 19 21H5C3.9 21 3 20.1 3 19V15" />
    <path d="M17 8L12 3L7 8" />
    <path d="M12 3V15" />
  </svg>
);

const GenerateIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M12 2L2 7L12 12L22 7L12 2Z" />
    <path d="M2 17L12 22L22 17" />
    <path d="M2 12L12 17L22 12" />
  </svg>
);

const ComplianceIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <circle cx="12" cy="12" r="10" />
    <path d="M9 12L11 14L15 10" />
  </svg>
);

const CostIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M12 1V23" />
    <path d="M17 5H9.5C8.57174 5 7.6815 5.36875 7.02513 6.02513C6.36875 6.6815 6 7.57174 6 8.5C6 9.42826 6.36875 10.3185 7.02513 10.9749C7.6815 11.6313 8.57174 12 9.5 12H14.5C15.4283 12 16.3185 12.3687 16.9749 13.0251C17.6313 13.6815 18 14.5717 18 15.5C18 16.4283 17.6313 17.3185 16.9749 17.9749C16.3185 18.6313 15.4283 19 14.5 19H6" />
  </svg>
);

const ScheduleIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
    <line x1="16" y1="2" x2="16" y2="6" />
    <line x1="8" y1="2" x2="8" y2="6" />
    <line x1="3" y1="10" x2="21" y2="10" />
  </svg>
);

const ClashIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <circle cx="12" cy="12" r="10" />
    <path d="M12 8V16" />
    <path d="M8 12H16" />
  </svg>
);

const ReportsIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M14 2H6C4.9 2 4 2.9 4 4V20C4 21.1 4.9 22 6 22H18C19.1 22 20 21.1 20 20V8L14 2Z" />
    <path d="M14 2V8H20" />
    <path d="M16 13H8" />
    <path d="M16 17H8" />
    <path d="M10 9H8" />
  </svg>
);

const TemplatesIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2Z" />
    <path d="M14 2V8H20" />
  </svg>
);

const DashboardPage: React.FC = () => {
  const navigate = useNavigate();

  // Updated stats with real BIMFlow metrics
  const stats = [
    { id: "projects", label: "Active Projects", value: 18, trend: "+4", icon: <ProjectsIcon /> },
    { id: "models", label: "IFC Models Generated", value: 42, trend: "+12", icon: <GenerateIcon /> },
    { id: "compliance", label: "Avg. Compliance Rate", value: "97%", trend: "+2.3%", icon: <ComplianceIcon /> },
    { id: "cost", label: "Total Cost Savings", value: "$128K", trend: "+28%", icon: <CostIcon /> },
    { id: "clash", label: "Clashes Resolved", value: 156, trend: "+31", icon: <ClashIcon /> },
    { id: "schedule", label: "On-Time Projects", value: "94%", trend: "+5%", icon: <ScheduleIcon /> },
  ];

  // Quick actions updated to match new sidebar routes
  const quickActions = [
    // ⚠️ Updated to match sidebar route: /dashboard/upload-ifc
    { id: "upload", label: "Upload & Validate IFC", icon: <UploadIcon />, onClick: () => navigate('/dashboard/upload-ifc') },
    { id: "generate", label: "Generate New Model", icon: <GenerateIcon />, onClick: () => navigate('/dashboard/generate') },
    { id: "compliance", label: "Run Compliance Check", icon: <ComplianceIcon />, onClick: () => navigate('/dashboard/compliance') },
    // ⚠️ Updated to match sidebar route: /dashboard/clash-detection
    { id: "clash", label: "Clash Detection", icon: <ClashIcon />, onClick: () => navigate('/dashboard/clash-detection') },
    // ⚠️ Updated to match sidebar route: /dashboard/cost-estimation
    { id: "cost", label: "Cost Estimation", icon: <CostIcon />, onClick: () => navigate('/dashboard/cost-estimation') },
    // ⚠️ Updated to match sidebar route: /dashboard/scheduling
    { id: "schedule", label: "Project Scheduling", icon: <ScheduleIcon />, onClick: () => navigate('/dashboard/scheduling') },
    { id: "reports", label: "Reports Center", icon: <ReportsIcon />, onClick: () => navigate('/dashboard/reports') },
    { id: "templates", label: "Asset Packs", icon: <TemplatesIcon />, onClick: () => navigate('/dashboard/templates') },
  ];

  const recentProjects = [
    {
      id: 1,
      title: "Victoria High-Rise Complex",
      type: "High-Rise Building",
      status: "Cost Estimation",
      compliance: "99%",
      updated: "1 hour ago",
      image: officeTower,
    },
    {
      id: 2,
      title: "River Bridge Extension",
      type: "Bridge Infrastructure",
      status: "Clash Detection",
      compliance: "96%",
      updated: "3 hours ago",
      image: bridgeExpansion,
    },
    {
      id: 3,
      title: "Smart City Road Network",
      type: "Road Infrastructure",
      status: "Gantt Generated",
      compliance: "94%",
      updated: "6 hours ago",
      image: urbanRoad,
    },
  ];

  return (
    <>
      {/* Hero Section */}
      <section className="dashboard-hero">
        <div className="dashboard-hero__content">
          <div className="dashboard-hero__welcome">
            <h1>Welcome back, Nnamdi</h1>
            <p>Your open-source BIM automation hub — generate, validate, analyze, and deliver faster than ever.</p>
          </div>
          <div className="dashboard-hero__quick-actions">
            {quickActions.map((action) => (
              <button key={action.id} className="quick-action-btn" onClick={action.onClick}>
                <span className="quick-action-icon">{action.icon}</span>
                {action.label}
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* --- */}

      {/* Stats Grid */}
      <section className="dashboard-stats">
        <h2 className="section-title">Your BIMFlow Performance</h2>
        <div className="stats-grid">
          {stats.map((stat, index) => (
            <div key={stat.id} className="stat-card" style={{ animationDelay: `${index * 0.1}s` }}>
              <div className="stat-card__inner">
                <div className="stat-card__header">
                  <span className="stat-icon">{stat.icon}</span>
                  <div>
                    <h3 className="stat-label">{stat.label}</h3>
                    <div className="stat-card__value">
                      <span className="stat-number">{stat.value}</span>
                      <span className="stat-trend">{stat.trend}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* --- */}

      {/* Recent Projects */}
      <section className="dashboard-recent">
        <div className="section-header">
          <h2 className="section-title">Recent Projects</h2>
          <button className="see-all-btn" onClick={() => navigate('/dashboard/projects')}>
            View All Projects →
          </button>
        </div>
        <div className="projects-grid">
          {recentProjects.map((project, index) => (
            <div key={project.id} className="project-card" style={{ animationDelay: `${index * 0.1}s` }}>
              <div className="project-card__image">
                <img src={project.image} alt={project.title} />
                <div className={`project-status-badge status-${project.status.toLowerCase().replace(/ /g, '-')}`}>
                  {project.status}
                </div>
              </div>
              <div className="project-card__details">
                <h3>{project.title}</h3>
                <p className="project-type">{project.type}</p>
                <div className="project-meta">
                  <div className="compliance-meter">
                    <span>Compliance: {project.compliance}</span>
                    <div className="compliance-bar">
                      <div 
                        className="compliance-progress" 
                        style={{ width: `${parseFloat(project.compliance)}%` }}
                      ></div>
                    </div>
                  </div>
                  <span className="updated-time">{project.updated}</span>
                </div>
                <div className="project-actions">
                  <button className="project-action primary" onClick={() => navigate('/dashboard/projects')}>
                    Open Project
                  </button>
                  <button className="project-action secondary" onClick={() => navigate('/dashboard/reports')}>
                    View Report
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* --- */}

      {/* Two Column Bottom */}
      <div className="dashboard-columns">
        <section className="dashboard-tasks">
          <h2 className="section-title">Next Actions</h2>
          <div className="tasks-list">
            <div className="task-item">
              <div className="task-icon">📤</div>
              <div className="task-details">
                <h4>Upload IFC for Bridge Project</h4>
                <p>Run validation, clash detection and cost analysis</p>
              </div>
              <div className="task-meta">
                <span className="task-time">Due today</span>
                {/* ⚠️ Updated route */}
                <button className="task-action" onClick={() => navigate('/dashboard/upload-ifc')}>Upload Now</button>
              </div>
            </div>
            <div className="task-item">
              <div className="task-icon">📐</div>
              <div className="task-details">
                <h4>Generate High-Rise Model</h4>
                <p>From intent: 45 floors, glass facade, green roof</p>
              </div>
              <div className="task-meta">
                <span className="task-time">Due in 2 days</span>
                <button className="task-action" onClick={() => navigate('/dashboard/generate')}>Generate</button>
              </div>
            </div>
            <div className="task-item">
              <div className="task-icon">📊</div>
              <div className="task-details">
                <h4>Review Cost Report</h4>
                <p>Road project estimate ready for approval</p>
              </div>
              <div className="task-meta">
                <span className="task-time">Due in 3 days</span>
                {/* ⚠️ Updated route */}
                <button className="task-action" onClick={() => navigate('/dashboard/cost-estimation')}>Review</button>
              </div>
            </div>
          </div>
        </section>

        <section className="dashboard-insights">
          <h2 className="section-title">BIMFlow Insights</h2>
          <div className="insights-grid">
            <div className="insight-card">
              <h3>Compliance Trends</h3>
              <div className="insight-chart">
                <div className="chart-bars">
                  <div className="chart-bar" style={{ height: '78%' }}></div>
                  <div className="chart-bar" style={{ height: '92%' }}></div>
                  <div className="chart-bar" style={{ height: '96%' }}></div>
                  <div className="chart-bar" style={{ height: '99%' }}></div>
                </div>
              </div>
              <p>Average compliance up 21% since using BIMFlow Suite</p>
            </div>
            <div className="insight-card">
              <h3>Time Saved</h3>
              <div className="insight-chart">
                <div className="chart-dots">
                  <div className="chart-dot" style={{ left: '20%', bottom: '25%' }}></div>
                  <div className="chart-dot" style={{ left: '40%', bottom: '55%' }}></div>
                  <div className="chart-dot" style={{ left: '60%', bottom: '70%' }}></div>
                  <div className="chart-dot" style={{ left: '80%', bottom: '90%' }}></div>
                </div>
              </div>
              <p>Automation saves 40+ hours per project</p>
            </div>
          </div>
        </section>
      </div>
    </>
  );
};

export default DashboardPage;