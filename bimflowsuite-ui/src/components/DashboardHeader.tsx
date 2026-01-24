// src/components/DashboardHeader.tsx
import React, { useState, useRef, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import "../assets/DashboardHeader.css";

const DashboardHeader: React.FC<{ onMobileToggle: () => void }> = ({ onMobileToggle }) => {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsDropdownOpen(false);
      }
    };
    if (isDropdownOpen) {
      document.addEventListener("mousedown", handleClickOutside);
    }
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [isDropdownOpen]);

  const toggleDropdown = () => {
    setIsDropdownOpen(!isDropdownOpen);
  };

  const handleLogout = () => {
    // Clear auth token from localStorage (adjust key if using a different one, e.g., 'authToken')
    localStorage.removeItem('token');
    // Optionally clear other auth-related storage
    sessionStorage.clear();
    // Close dropdown
    setIsDropdownOpen(false);
    // Navigate to login page
    navigate('/login');
  };

  return (
    <header className="dashboard-header">
      <div className="dashboard-header__container">
        <div className="header-left">
          <button className="menu-toggle" onClick={onMobileToggle} aria-label="Toggle menu">
            <span className="menu-icon">☰</span>
          </button>
        </div>
        <div className="dashboard-actions">
          <button className="action-btn" title="Notifications" aria-label="Notifications">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M18 8C18 6.4087 17.3679 4.88258 16.2426 3.75736C15.1174 2.63214 13.5913 2 12 2C10.4087 2 8.88258 2.63214 7.75736 3.75736C6.63214 4.88258 6 6.4087 6 8C6 13.2113 3 17 3 17H21C21 17 18 13.2113 18 8Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M13.73 21A1.9974 1.9974 0 0 1 12 21C10.8954 21 10 20.1046 10 19C10 17.8954 10.8954 17 12 17C13.1046 17 14 17.8954 14 19C14 20.1046 13.1046 21 12 21H13.73Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
            <span className="notification-badge"></span>
          </button>
          <button className="action-btn" title="Settings" aria-label="Settings">
            <SettingsIcon />
          </button>
          <div className="user-profile-wrapper" ref={dropdownRef}>
            <div className={`user-profile ${isDropdownOpen ? 'active' : ''}`} onClick={toggleDropdown}>
              <img src="https://ui-avatars.com/api/?name=Nnamdi+Oniya&background=4ade80&color=1f2937&bold=true" alt="Nnamdi Oniya" className="avatar" />
              <div className="user-info">
                <span className="user-name">Nnamdi Oniya</span>
                <span className="user-role">Admin</span>
              </div>
              <span className="dropdown-arrow">▼</span>
            </div>
            <div className={`user-dropdown ${isDropdownOpen ? 'active' : ''}`}>
              <div className="dropdown-header">
                <span className="dropdown-user-name">Nnamdi Oniya</span>
                <span className="dropdown-user-email">nnamdi.oniya@bimflow.com</span>
              </div>
              <div className="dropdown-menu">
                <Link to="/dashboard/profile" className="dropdown-item" onClick={() => setIsDropdownOpen(false)}>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M20 21V19C20 17.9391 19.5786 16.9217 18.8284 16.1716C18.0783 15.4214 17.0609 15 16 15H8C6.93913 15 5.92172 15.4214 5.17157 16.1716C4.42143 16.9217 4 17.9391 4 19V21" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    <path d="M12 11C14.2091 11 16 9.20914 16 7C16 4.79086 14.2091 3 12 3C9.79086 3 8 4.79086 8 7C8 9.20914 9.79086 11 12 11Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                  <span>Profile</span>
                </Link>
                <Link to="/dashboard/settings" className="dropdown-item" onClick={() => setIsDropdownOpen(false)}>
                  <SettingsIcon />
                  <span>Settings</span>
                </Link>
                <Link to="/dashboard/billing" className="dropdown-item" onClick={() => setIsDropdownOpen(false)}>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="9" y="7" width="6" height="14" rx="1" stroke="currentColor" strokeWidth="2"/>
                    <path d="M22.28 15.7A3.78 3.78 0 0 1 19 16.5C17.28 16.5 15.8 15.08 15.8 13.5S17.28 10.5 19 10.5C20.18 10.5 21.28 11.34 21.72 12.62L22.62 12L22.28 15.7Z" stroke="currentColor" strokeWidth="2"/>
                    <path d="M21 12H15" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                  </svg>
                  <span>Billing</span>
                </Link>
                <div className="dropdown-divider"></div>
                <button className="dropdown-item logout" onClick={handleLogout}>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M9 21H5C4.46957 21 4 20.5304 4 20V4C4 3.46957 4.46957 3 5 3H9M16 17L21 12L16 7M21 12H9" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                  <span>Sign Out</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

// Reuse SettingsIcon from sidebar
const SettingsIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="12" cy="12" r="3" stroke="currentColor" strokeWidth="2"/>
    <path d="M19.4 15A7.5 7.5 0 0 0 12 4.6M12 19.4A7.5 7.5 0 0 0 19.4 12M12 4.6V19.4" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
  </svg>
);

export default DashboardHeader;