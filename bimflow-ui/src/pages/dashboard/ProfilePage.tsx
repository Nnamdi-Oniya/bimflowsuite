// src/pages/dashboard/ProfilePage.tsx
import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "../../assets/ProfilePage.css"; // We'll define this CSS below

const DashboardProfile: React.FC = () => {
  const navigate = useNavigate();
  const [isEditing, setIsEditing] = useState(false);
  const [userData, setUserData] = useState({
    name: "Nnamdi Oniya",
    email: "nnamdi.oniya@bimflow.com",
    role: "Admin",
    bio: "Founder & CEO of BIMFlow Suite. Passionate about democratizing BIM for SMEs.",
    avatar: "https://ui-avatars.com/api/?name=Nnamdi+Oniya&background=4ade80&color=1f2937&bold=true",
    phone: "+234 123 456 7890",
    location: "Lagos, Nigeria",
    subscription: "Pro Plan",
    joined: "November 2023",
  });
  const [tempData, setTempData] = useState(userData);
  const [isUploading, setIsUploading] = useState(false);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setTempData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSave = () => {
    setUserData(tempData);
    setIsEditing(false);
    // Simulate API call
    console.log("Profile updated:", tempData);
  };

  const handleCancel = () => {
    setTempData(userData);
    setIsEditing(false);
  };

  const handleAvatarUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setIsUploading(true);
      // Simulate upload
      setTimeout(() => {
        setTempData((prev) => ({ ...prev, avatar: URL.createObjectURL(file) }));
        setIsUploading(false);
      }, 1500);
    }
  };

  const handleLogout = () => {
    console.log("Logging out...");
    navigate("/login");
  };

  return (
    <div className="profile-page">
      <div className="profile-container">
        {/* Header */}
        <div className="profile-header">
          <h1 className="profile-title">My Profile</h1>
          <div className="profile-actions">
            {!isEditing ? (
              <button className="btn-edit" onClick={() => setIsEditing(true)}>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M11 4H4C3.46957 4 2.96086 4.21071 2.58579 4.58579C2.21071 4.96086 2 5.46957 2 6V18C2 18.5304 2.21071 19.0391 2.58579 19.4142C2.96086 19.7893 3.46957 20 4 20H16C16.5304 20 17.0391 19.7893 17.4142 19.4142C17.7893 19.0391 18 18.5304 18 18V11M18.364 5.63604C18.6074 5.39262 18.8978 5.23032 19.2001 5.14912C19.5024 5.06792 19.813 5.07766 20.1084 5.17578C20.4038 5.2739 20.679 5.45513 20.9261 5.70224C21.1732 5.94935 21.3544 6.22454 21.4525 6.51988C21.5507 6.81522 21.5604 7.12585 21.4792 7.42811C21.398 7.73037 21.2357 8.02081 20.9923 8.26423L12 17.256V18H10V15.744L18.364 7.364L18.364 5.63604Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
                Edit Profile
              </button>
            ) : (
              <>
                <button className="btn-save" onClick={handleSave}>
                  Save Changes
                </button>
                <button className="btn-cancel" onClick={handleCancel}>
                  Cancel
                </button>
              </>
            )}
          </div>
        </div>

        {/* Avatar Section */}
        <div className="profile-avatar-section">
          <div className="avatar-upload">
            <img src={tempData.avatar} alt="Profile Avatar" className="avatar-large" />
            {isEditing && (
              <label htmlFor="avatar-upload" className="avatar-edit-overlay">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M11 4H4C3.46957 4 2.96086 4.21071 2.58579 4.58579C2.21071 4.96086 2 5.46957 2 6V18C2 18.5304 2.21071 19.0391 2.58579 19.4142C2.96086 19.7893 3.46957 20 4 20H16C16.5304 20 17.0391 19.7893 17.4142 19.4142C17.7893 19.0391 18 18.5304 18 18V11M18.364 5.63604C18.6074 5.39262 18.8978 5.23032 19.2001 5.14912C19.5024 5.06792 19.813 5.07766 20.1084 5.17578C20.4038 5.2739 20.679 5.45513 20.9261 5.70224C21.1732 5.94935 21.3544 6.22454 21.4525 6.51988C21.5507 6.81522 21.5604 7.12585 21.4792 7.42811C21.398 7.73037 21.2357 8.02081 20.9923 8.26423L12 17.256V18H10V15.744L18.364 7.364L18.364 5.63604Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
                <input
                  id="avatar-upload"
                  type="file"
                  accept="image/*"
                  onChange={handleAvatarUpload}
                  style={{ display: "none" }}
                />
                {isUploading && <span className="upload-status">Uploading...</span>}
              </label>
            )}
          </div>
          <div className="avatar-info">
            <h2 className="avatar-name">{tempData.name}</h2>
            <p className="avatar-role">{tempData.role}</p>
          </div>
        </div>

        {/* Main Profile Details */}
        <div className="profile-details">
          <div className="detail-card">
            <h3 className="detail-title">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M20 21V19C20 17.9391 19.5786 16.9217 18.8284 16.1716C18.0783 15.4214 17.0609 15 16 15H8C6.93913 15 5.92172 15.4214 5.17157 16.1716C4.42143 16.9217 4 17.9391 4 19V21" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M12 11C14.2091 11 16 9.20914 16 7C16 4.79086 14.2091 3 12 3C9.79086 3 8 4.79086 8 7C8 9.20914 9.79086 11 12 11Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
              Personal Information
            </h3>
            <div className="detail-grid">
              <div className="detail-field">
                <label htmlFor="name">Full Name</label>
                <input
                  id="name"
                  name="name"
                  type="text"
                  value={tempData.name}
                  onChange={handleInputChange}
                  disabled={!isEditing}
                  className={`input-field ${isEditing ? 'editable' : ''}`}
                />
              </div>
              <div className="detail-field">
                <label htmlFor="email">Email Address</label>
                <input
                  id="email"
                  name="email"
                  type="email"
                  value={tempData.email}
                  onChange={handleInputChange}
                  disabled={!isEditing}
                  className={`input-field ${isEditing ? 'editable' : ''}`}
                />
              </div>
              <div className="detail-field">
                <label htmlFor="phone">Phone Number</label>
                <input
                  id="phone"
                  name="phone"
                  type="tel"
                  value={tempData.phone}
                  onChange={handleInputChange}
                  disabled={!isEditing}
                  className={`input-field ${isEditing ? 'editable' : ''}`}
                />
              </div>
              <div className="detail-field full-width">
                <label htmlFor="bio">Bio</label>
                <textarea
                  id="bio"
                  name="bio"
                  value={tempData.bio}
                  onChange={handleInputChange}
                  disabled={!isEditing}
                  rows={3}
                  className={`input-field textarea-field ${isEditing ? 'editable' : ''}`}
                />
              </div>
              <div className="detail-field">
                <label>Location</label>
                <input
                  type="text"
                  value={tempData.location}
                  disabled
                  className="input-field"
                />
              </div>
              <div className="detail-field">
                <label>Member Since</label>
                <input
                  type="text"
                  value={tempData.joined}
                  disabled
                  className="input-field"
                />
              </div>
            </div>
          </div>

          {/* Account Section */}
          <div className="detail-card">
            <h3 className="detail-title">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2L2 7V17L12 22L22 17V7L12 2Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M12 2V22" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M2 7H22" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
              Account Settings
            </h3>
            <div className="account-actions">
              <Link to="/dashboard/settings" className="action-link">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <circle cx="12" cy="12" r="3" stroke="currentColor" strokeWidth="2"/>
                  <path d="M19.4 15A7.5 7.5 0 0 0 12 4.6M12 19.4A7.5 7.5 0 0 0 19.4 12M12 4.6V19.4" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                </svg>
                Manage Settings
              </Link>
              <Link to="/dashboard/billing" className="action-link">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <rect x="9" y="7" width="6" height="14" rx="1" stroke="currentColor" strokeWidth="2"/>
                  <path d="M22.28 15.7A3.78 3.78 0 0 1 19 16.5C17.28 16.5 15.8 15.08 15.8 13.5S17.28 10.5 19 10.5C20.18 10.5 21.28 11.34 21.72 12.62L22.62 12L22.28 15.7Z" stroke="currentColor" strokeWidth="2"/>
                  <path d="M21 12H15" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                </svg>
                Billing & Subscription ({tempData.subscription})
              </Link>
              <button className="action-link danger" onClick={handleLogout}>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M9 21H5C4.46957 21 4 20.5304 4 20V4C4 3.46957 4.46957 3 5 3H9M16 17L21 12L16 7M21 12H9" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
                Sign Out
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardProfile;