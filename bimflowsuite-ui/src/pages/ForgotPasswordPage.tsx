// Updated ForgotPasswordPage.tsx with form validation
import React, { useState } from "react";
import { Link } from "react-router-dom";

import "../assets/ForgotPasswordPage.css";
import forgotPasswordImage from "../assets/images/forgotPasswordImage.jpg"; // Full-page left side image

const ForgotPasswordPage: React.FC = () => {
  const [email, setEmail] = useState("");
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  const validateEmail = (email: string): string => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email) ? "" : "Please enter a valid email address.";
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setEmail(value);

    // Clear error on change
    if (errors.email) {
      setErrors({});
    }

    // Validate email on change
    if (value.trim()) {
      const emailError = validateEmail(value);
      setErrors({ email: emailError });
    }
  };

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!email.trim()) {
      newErrors.email = "Email is required.";
    } else {
      const emailError = validateEmail(email);
      if (emailError) newErrors.email = emailError;
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateForm()) return;
    setIsLoading(true);

    // Simulate API call
    setTimeout(() => {
      setIsLoading(false);
      setMessage("If an account with that email exists, we've sent a reset link.");
      setEmail("");
    }, 1500);
  };

  return (
    <div className="forgot-password-page">
    
      <div className="forgot-password-main">
        <div className="forgot-password-image-section">
          <img src={forgotPasswordImage} alt="Password recovery illustration" className="forgot-password-image" />
        </div>
        <div className="forgot-password-content-section">
          <div className="forgot-password-content-wrapper">
            <div className="forgot-password-form-card">
              <h2 className="forgot-password-title">Forgot Password</h2>
              <p className="forgot-password-subtitle">Enter your email to reset your password.</p>
              <form onSubmit={handleSubmit} className="forgot-password-form">
                <div className="form-group">
                  <label htmlFor="email" className="form-label">
                    Email Address *
                  </label>
                  <input
                    type="email"
                    id="email"
                    value={email}
                    onChange={handleChange}
                    className={`form-input ${errors.email ? 'error' : ''}`}
                    placeholder="Enter your email"
                    required
                  />
                  {errors.email && <span className="error-text">{errors.email}</span>}
                </div>

                <button 
                  type="submit" 
                  className="forgot-password-btn"
                  disabled={isLoading}
                >
                  {isLoading ? (
                    <>
                      <div className="loading-spinner"></div>
                      Sending Link...
                    </>
                  ) : (
                    'Send Reset Link'
                  )}
                </button>
              </form>

              {message && <div className="success-message">{message}</div>}

              <div className="back-link">
                <Link to="/login" className="back-to-login">Back to Login</Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ForgotPasswordPage;