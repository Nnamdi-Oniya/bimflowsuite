import React, { useState, useEffect } from "react";
import { Settings as SettingsIcon, User, Palette, Link2, FileCode } from "lucide-react";
import "../../assets/SettingsPage.css";

type Theme = 'light' | 'dark' | 'system';

const SettingsPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState('general');
  const [theme, setTheme] = useState<Theme>(() => {
    const saved = localStorage.getItem('theme') as Theme;
    return saved || 'system';
  });

  // Apply theme on mount and when theme changes
  useEffect(() => {
    const applyTheme = (selectedTheme: Theme) => {
      const root = document.documentElement;
      
      if (selectedTheme === 'system') {
        const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        if (systemPrefersDark) {
          root.classList.add('dark');
        } else {
          root.classList.remove('dark');
        }
      } else if (selectedTheme === 'dark') {
        root.classList.add('dark');
      } else {
        root.classList.remove('dark');
      }
    };

    applyTheme(theme);
    localStorage.setItem('theme', theme);

    // Listen for system theme changes when system mode is selected
    if (theme === 'system') {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
      const handleChange = () => applyTheme('system');
      mediaQuery.addEventListener('change', handleChange);
      return () => mediaQuery.removeEventListener('change', handleChange);
    }
  }, [theme]);

  const handleThemeChange = (newTheme: Theme) => {
    setTheme(newTheme);
  };

  const tabs = [
    { id: 'general', label: 'General', icon: SettingsIcon },
    { id: 'account', label: 'Account', icon: User },
    { id: 'integrations', label: 'Integrations', icon: Link2 },
    { id: 'rules', label: 'Rule Packs', icon: FileCode },
  ];

  return (
    <div className="settings-page">
      <div className="settings-header">
        <div className="header-content">
          <h1>Settings</h1>
          <p>Manage your account, preferences, and integrations</p>
        </div>
      </div>

      <div className="settings-container">
        <div className="settings-tabs">
          {tabs.map(tab => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                className={`tab-btn ${activeTab === tab.id ? 'active' : ''}`}
                onClick={() => setActiveTab(tab.id)}
              >
                <Icon size={20} />
                {tab.label}
              </button>
            );
          })}
        </div>

        <div className="settings-content">
          {activeTab === 'general' && (
            <div className="tab-panel">
              <h2>
                <Palette size={24} />
                General Settings
              </h2>
              <div className="setting-group">
                <label>Theme</label>
                <p className="setting-description">Choose your preferred theme or sync with system settings</p>
                <div className="theme-options">
                  <button
                    className={`theme-btn ${theme === 'light' ? 'active' : ''}`}
                    onClick={() => handleThemeChange('light')}
                  >
                    ☀️ Light
                  </button>
                  <button
                    className={`theme-btn ${theme === 'dark' ? 'active' : ''}`}
                    onClick={() => handleThemeChange('dark')}
                  >
                    🌙 Dark
                  </button>
                  <button
                    className={`theme-btn ${theme === 'system' ? 'active' : ''}`}
                    onClick={() => handleThemeChange('system')}
                  >
                    💻 System
                  </button>
                </div>
              </div>
              <div className="setting-group">
                <label>Language</label>
                <p className="setting-description">Select your preferred language</p>
                <select>
                  <option>English</option>
                  <option>Spanish</option>
                  <option>French</option>
                  <option>German</option>
                </select>
              </div>
              <button className="save-btn">Save Changes</button>
            </div>
          )}

          {activeTab === 'account' && (
            <div className="tab-panel">
              <h2>
                <User size={24} />
                Account Settings
              </h2>
              <div className="setting-group">
                <label>Email</label>
                <p className="setting-description">Your primary email address</p>
                <input type="email" defaultValue="nnamdi.oniya@bimflow.com" />
              </div>
              <div className="setting-group">
                <label>Role</label>
                <p className="setting-description">Your current role in the organization</p>
                <select>
                  <option>Administrator</option>
                  <option>Editor</option>
                  <option>Viewer</option>
                </select>
              </div>
              <div className="setting-group">
                <label>Organization</label>
                <p className="setting-description">Your company or organization name</p>
                <input type="text" defaultValue="BIMFlow Solutions" />
              </div>
              <button className="save-btn">Update Account</button>
            </div>
          )}

          {activeTab === 'integrations' && (
            <div className="tab-panel">
              <h2>
                <Link2 size={24} />
                Integrations
              </h2>
              <p className="tab-description">Connect to external BIM tools like Revit or BlenderBIM via BCF.</p>
              
              <div className="integration-item">
                <div className="integration-info">
                  <h3>Revit API</h3>
                  <p>Connect to Autodesk Revit for seamless BIM data exchange</p>
                </div>
                <button className="connect-btn">Connect</button>
              </div>
              
              <div className="integration-item">
                <div className="integration-info">
                  <h3>BlenderBIM</h3>
                  <p>Integrate with open-source BlenderBIM for IFC workflows</p>
                </div>
                <button className="connect-btn">Connect</button>
              </div>
              
              <div className="integration-item">
                <div className="integration-info">
                  <h3>Navisworks</h3>
                  <p>Sync clash detection results with Autodesk Navisworks</p>
                </div>
                <button className="connect-btn connected">Connected</button>
              </div>
            </div>
          )}

          {activeTab === 'rules' && (
            <div className="tab-panel">
              <h2>
                <FileCode size={24} />
                Custom Rule Packs
              </h2>
              <p className="tab-description">Upload YAML/JSON rule packs for custom compliance checking.</p>
              
              <div className="upload-area">
                <input type="file" accept=".yaml,.json" id="rule-upload" />
                <label htmlFor="rule-upload" className="upload-label">
                  <FileCode size={32} />
                  <span>Click to upload or drag & drop</span>
                  <small>Supports .yaml and .json files</small>
                </label>
              </div>
              
              <button className="upload-btn">Upload Pack</button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SettingsPage;