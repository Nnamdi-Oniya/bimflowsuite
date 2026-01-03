// src/components/DashboardSidebar.tsx
import React, { useState, useEffect } from "react";
// 1. Import useNavigate to handle redirection
import { Link, useLocation, useNavigate } from "react-router-dom";
import "../assets/DashboardSidebar.css";

// Keep all your beautiful SVG icons exactly as they are (unchanged)
const HomeIcon = () => ( <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"> <path d="M3 9L12 2L21 9V20C21 21.1 20.1 22 19 22H5C3.9 22 3 21.1 3 20V9Z" /> <path d="M9 22V12H15V22" /> </svg> );
const ProjectsIcon = () => ( <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"> <rect x="3" y="3" width="18" height="18" rx="2" /> <path d="M3 9H21" /> <path d="M9 21V9" /> </svg> );
const UploadIcon = () => ( <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"> <path d="M21 15V19C21 20.1 20.1 21 19 21H5C3.9 21 3 20.1 3 19V15" /> <path d="M17 8L12 3L7 8" /> <path d="M12 3V15" /> </svg> );
const GenerateIcon = () => ( <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"> <path d="M12 2L2 7L12 12L22 7L12 2Z" /> <path d="M2 17L12 22L22 17" /> <path d="M2 12L12 17L22 12" /> </svg> );
const ComplianceIcon = () => ( <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"> <circle cx="12" cy="12" r="10" /> <path d="M9 12L11 14L15 10" /> </svg> );
const ClashIcon = () => ( <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"> <circle cx="12" cy="12" r="10" /> <path d="M12 8V16" /> <path d="M8 12H16" /> </svg> );
const CostIcon = () => ( <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"> <path d="M12 1V23" /> <path d="M17 5H9.5C8.57174 5 7.6815 5.36875 7.02513 6.02513C6.36875 6.6815 6 7.57174 6 8.5C6 9.42826 6.36875 10.3185 7.02513 10.9749C7.6815 11.6313 8.57174 12 9.5 12H14.5C15.4283 12 16.3185 12.3687 16.9749 13.0251C17.6313 13.6815 18 14.5717 18 15.5C18 16.4283 17.6313 17.3185 16.9749 17.9749C16.3185 18.6313 15.4283 19 14.5 19H6" /> </svg> );
const ScheduleIcon = () => ( <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"> <rect x="3" y="4" width="18" height="18" rx="2" ry="2" /> <line x1="16" y1="2" x2="16" y2="6" /> <line x1="8" y1="2" x2="8" y2="6" /> <line x1="3" y1="10" x2="21" y2="10" /> </svg> );
const ReportsIcon = () => ( <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"> <path d="M14 2H6C4.9 2 4 2.9 4 4V20C4 21.1 4.9 22 6 22H18C19.1 22 20 21.1 20 20V8L14 2Z" /> <path d="M14 2V8H20" /> <path d="M16 13H8" /> <path d="M16 17H8" /> <path d="M10 9H8" /> </svg> );
const ScenarioIcon = () => ( <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"> <path d="M3 3H21V21H3V3Z" /> <path d="M3 9H21" /> <path d="M9 21V9" /> <path d="M15 21V15" /> </svg> );
const TemplatesIcon = () => ( <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"> <path d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2Z" /> <path d="M14 2V8H20" /> </svg> );
const SunIcon = () => ( <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"> <circle cx="12" cy="12" r="5" /> <line x1="12" y1="1" x2="12" y2="3" /> <line x1="12" y1="21" x2="12" y2="23" /> <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" /> <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" /> <line x1="1" y1="12" x2="3" y2="12" /> <line x1="21" y1="12" x2="23" y2="12" /> <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" /> <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" /> </svg> );
const MoonIcon = () => ( <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"> <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79Z" /> </svg> );

const DashboardSidebar: React.FC<{ isOpen: boolean; onToggle: () => void }> = ({ isOpen, onToggle }) => {
  const location = useLocation();
  // 2. Initialize navigate hook
  const navigate = useNavigate();
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  useEffect(() => {
    const saved = localStorage.getItem('theme') as 'light' | 'dark' | null;
    const newTheme = saved || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    setTheme(newTheme);
    document.documentElement.classList.toggle('dark', newTheme === 'dark');
  }, []);

  const toggleTheme = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme);
    document.documentElement.classList.toggle('dark', newTheme === 'dark');
  };

  // 3. Create handleLogout function
  const handleLogout = () => {
    // Since there is no backend yet, we simulate logging out by clearing
    // any potential auth tokens stored in localStorage.
    // Assuming you might use names like 'authToken' or 'user' in the future.
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
    // Note: We keep the 'theme' in localStorage because that's a UI preference, not auth data.

    // Redirect the user to the login page (or home page)
    navigate('/login'); // Change '/login' to '/' if you want to redirect to home instead
  };

  const sidebarItems = [
    { id: "overview", label: "Overview", icon: <HomeIcon />, link: "/dashboard" },
    { id: "projects", label: "Projects", icon: <ProjectsIcon />, link: "/dashboard/projects" },
    { id: "upload", label: "Upload & Validate", icon: <UploadIcon />, link: "/dashboard/upload-ifc" },
    { id: "generate", label: "Generate Model", icon: <GenerateIcon />, link: "/dashboard/generate" },
    { id: "compliance", label: "Compliance Checks", icon: <ComplianceIcon />, link: "/dashboard/compliance" },
    { id: "clash", label: "Clash Detection", icon: <ClashIcon />, link: "/dashboard/clash-detection" },
    { id: "cost", label: "Cost Estimation", icon: <CostIcon />, link: "/dashboard/cost-estimation" },
    { id: "schedule", label: "Project Scheduling", icon: <ScheduleIcon />, link: "/dashboard/scheduling" },
    { id: "reports", label: "Reports Center", icon: <ReportsIcon />, link: "/dashboard/reports" },
    { id: "scenarios", label: "Scenario Manager", icon: <ScenarioIcon />, link: "/dashboard/scenarios" },
    { id: "templates", label: "Templates", icon: <TemplatesIcon />, link: "/dashboard/templates" },
  ];

  const isActive = (link: string) => {
    if (link === "/dashboard") return location.pathname === "/dashboard";
    return location.pathname.startsWith(link);
  };

  return (
    <>
      {isOpen && <div className="sidebar-backdrop" onClick={onToggle} />}
      <nav className={`dashboard-sidebar ${isOpen ? 'active' : ''}`}>
        <div className="sidebar-header">
          <h2 className="sidebar-title">BIMFlow Suite</h2>
          <button className="sidebar-close" onClick={onToggle} aria-label="Close sidebar">×</button>
        </div>

        <ul className="sidebar-nav">
          {sidebarItems.map(item => (
            <li key={item.id}>
              <Link
                to={item.link}
                className={`sidebar-link ${isActive(item.link) ? 'active' : ''}`}
                onClick={() => window.innerWidth <= 1024 && onToggle()}
              >
                <span className="sidebar-icon">{item.icon}</span>
                <span className="sidebar-label">{item.label}</span>
              </Link>
            </li>
          ))}
        </ul>

        <div className="sidebar-footer">
          <div className="user-info">
            <img src="https://ui-avatars.com/api/?name=Nnamdi+Oniya&background=F8780F&color=fff&bold=true" alt="User" className="user-avatar" />
            <div>
              <div className="user-name">Nnamdi+Oniya</div>
              <div className="user-role">Founder & Admin</div>
            </div>
          </div>
          {/* 4. Attach the handleLogout function to the onClick event */}
          <button className="logout-btn" onClick={handleLogout}>Sign Out</button>
          <button className="theme-toggle" onClick={toggleTheme} aria-label="Toggle theme">
            {theme === 'light' ? <MoonIcon /> : <SunIcon />}
          </button>
        </div>
      </nav>
    </>
  );
};

export default DashboardSidebar;