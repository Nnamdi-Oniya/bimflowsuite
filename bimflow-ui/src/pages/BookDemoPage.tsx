import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "../assets/BookDemoPage.css";
import registerImage from "../assets/images/registerImage.jpg";

const BookDemoPage: React.FC = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    requestType: "",
    firstName: "",
    lastName: "",
    email: "",
    country: "",
    company: "",
    jobTitle: "",
    phone: "",
    additionalInfo: ""
  });
  const [consents, setConsents] = useState({
    communications: false,
    marketing: false
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isLoading, setIsLoading] = useState(false);

  const validateEmail = (email: string): string => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email) ? "" : "Please enter a valid email address.";
  };

  const validatePhone = (phone: string): string => {
    const phoneRegex = /^\+?[1-9]\d{1,14}$/; // Basic international phone validation
    return phoneRegex.test(phone.replace(/\s/g, '')) ? "" : "Please enter a valid phone number including country code.";
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });

    // Clear error on change for all fields
    if (errors[name]) {
      setErrors({ ...errors, [name]: "" });
    }

    // Real-time validation for email and phone
    if (name === "email") {
      if (value.trim()) {
        const emailError = validateEmail(value);
        setErrors({ ...errors, email: emailError });
      }
    } else if (name === "phone") {
      if (value.trim()) {
        const phoneError = validatePhone(value);
        setErrors({ ...errors, phone: phoneError });
      }
    }
  };

  const handleConsentChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setConsents({ ...consents, [e.target.name]: e.target.checked });
    if (errors[e.target.name]) {
      setErrors({ ...errors, [e.target.name]: "" });
    }
  };

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    // Validate requestType
    if (!formData.requestType.trim()) {
      newErrors.requestType = "Please select a request type.";
    }

    // Validate firstName
    if (!formData.firstName.trim()) {
      newErrors.firstName = "Please enter your first name.";
    } else if (formData.firstName.length < 2) {
      newErrors.firstName = "First name must be at least 2 characters long.";
    }

    // Validate lastName
    if (!formData.lastName.trim()) {
      newErrors.lastName = "Please enter your last name.";
    } else if (formData.lastName.length < 2) {
      newErrors.lastName = "Last name must be at least 2 characters long.";
    }

    // Validate email
    if (!formData.email.trim()) {
      newErrors.email = "Email is required.";
    } else {
      const emailError = validateEmail(formData.email);
      if (emailError) newErrors.email = emailError;
    }

    // Validate country
    if (!formData.country.trim()) {
      newErrors.country = "Please enter your country.";
    } else if (formData.country.length < 2) {
      newErrors.country = "Country name must be at least 2 characters long.";
    }

    // Validate company
    if (!formData.company.trim()) {
      newErrors.company = "Please enter your company name.";
    } else if (formData.company.length < 2) {
      newErrors.company = "Company name must be at least 2 characters long.";
    }

    // Validate jobTitle
    if (!formData.jobTitle.trim()) {
      newErrors.jobTitle = "Please enter your job title.";
    } else if (formData.jobTitle.length < 2) {
      newErrors.jobTitle = "Job title must be at least 2 characters long.";
    }

    // Validate phone
    if (!formData.phone.trim()) {
      newErrors.phone = "Phone number is required.";
    } else {
      const phoneError = validatePhone(formData.phone);
      if (phoneError) newErrors.phone = phoneError;
    }

    // Validate communications consent
    if (!consents.communications) {
      newErrors.communications = "You must consent to receive communications to proceed.";
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
      navigate("/"); // Redirect to home after submission
    }, 1500);
  };

  return (
    <div className="book-demo-page">
      <div className="book-demo-main">
        <div className="book-demo-image-section">
          <img src={registerImage} alt="Demo illustration" className="book-demo-image" />
        </div>
        <div className="book-demo-content-section">
          <div className="book-demo-content-wrapper">
            <div className="book-demo-form-card">
              <h2 className="book-demo-title">Book a Demo</h2>
              <p className="book-demo-subtitle">Schedule a call with our team to explore SME BIM Automation Toolkit.</p>
              
              {/* Moved Login Prompt Here */}
              <div className="login-prompt-top">
                <p>
                  Already have an account? <Link to="/login" className="login-link">Sign in here</Link>
                </p>
              </div>

              <form onSubmit={handleSubmit} className="book-demo-form">
                <div className="form-group">
                  <label htmlFor="requestType" className="form-label">
                    Request type *
                  </label>
                  <select
                    id="requestType"
                    name="requestType"
                    value={formData.requestType}
                    onChange={handleChange}
                    className={`form-input ${errors.requestType ? 'error' : ''}`}
                    required
                  >
                    <option value="">Select a request type</option>
                    <option value="book-demo">Book a Demo</option>
                    <option value="compliance-validation">Compliance Validation</option>
                    <option value="request-a-trial">Request a Trial</option>
                    <option value="general-inquiry">General Inquiry</option>
                    <option value="others">Others</option>
                  </select>
                  {errors.requestType && <span className="error-text">{errors.requestType}</span>}
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="firstName" className="form-label">
                      First name *
                    </label>
                    <input
                      type="text"
                      id="firstName"
                      name="firstName"
                      value={formData.firstName}
                      onChange={handleChange}
                      className={`form-input ${errors.firstName ? 'error' : ''}`}
                      placeholder="John"
                      required
                    />
                    {errors.firstName && <span className="error-text">{errors.firstName}</span>}
                  </div>
                  <div className="form-group">
                    <label htmlFor="lastName" className="form-label">
                      Last name *
                    </label>
                    <input
                      type="text"
                      id="lastName"
                      name="lastName"
                      value={formData.lastName}
                      onChange={handleChange}
                      className={`form-input ${errors.lastName ? 'error' : ''}`}
                      placeholder="Doe"
                      required
                    />
                    {errors.lastName && <span className="error-text">{errors.lastName}</span>}
                  </div>
                </div>

                <div className="form-group">
                  <label htmlFor="email" className="form-label">
                    Email *
                  </label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    className={`form-input ${errors.email ? 'error' : ''}`}
                    placeholder="john@bimflow.dev"
                    required
                  />
                  {errors.email && <span className="error-text">{errors.email}</span>}
                </div>

                <div className="form-group">
                  <label htmlFor="country" className="form-label">
                    Country *
                  </label>
                  <input
                    type="text"
                    id="country"
                    name="country"
                    value={formData.country}
                    onChange={handleChange}
                    className={`form-input ${errors.country ? 'error' : ''}`}
                    placeholder="United States"
                    required
                  />
                  {errors.country && <span className="error-text">{errors.country}</span>}
                </div>

                <div className="form-group">
                  <label htmlFor="company" className="form-label">
                    Company name *
                  </label>
                  <input
                    type="text"
                    id="company"
                    name="company"
                    value={formData.company}
                    onChange={handleChange}
                    className={`form-input ${errors.company ? 'error' : ''}`}
                    placeholder="Your Company Ltd."
                    required
                  />
                  {errors.company && <span className="error-text">{errors.company}</span>}
                </div>

                <div className="form-group">
                  <label htmlFor="jobTitle" className="form-label">
                    Job title *
                  </label>
                  <input
                    type="text"
                    id="jobTitle"
                    name="jobTitle"
                    value={formData.jobTitle}
                    onChange={handleChange}
                    className={`form-input ${errors.jobTitle ? 'error' : ''}`}
                    placeholder="BIM Manager"
                    required
                  />
                  {errors.jobTitle && <span className="error-text">{errors.jobTitle}</span>}
                </div>

                <div className="form-group">
                  <label htmlFor="phone" className="form-label">
                    Phone number *
                  </label>
                  <input
                    type="tel"
                    id="phone"
                    name="phone"
                    value={formData.phone}
                    onChange={handleChange}
                    className={`form-input ${errors.phone ? 'error' : ''}`}
                    placeholder="+1 123 456 7890"
                    required
                  />
                  <small className="form-note">Enter your phone number, including the country code</small>
                  {errors.phone && <span className="error-text">{errors.phone}</span>}
                </div>

                <div className="form-group">
                  <label htmlFor="additionalInfo" className="form-label">
                    Additional information
                  </label>
                  <textarea
                    id="additionalInfo"
                    name="additionalInfo"
                    value={formData.additionalInfo}
                    onChange={handleChange}
                    className="form-input"
                    rows={4}
                    placeholder="Tell us more about your needs..."
                  />
                </div>

                <div className="consent-group">
                  <label className="consent-label">
                    <input
                      type="checkbox"
                      name="communications"
                      checked={consents.communications}
                      onChange={handleConsentChange}
                      required
                    />
                    <span>I consent to receive communications from SME BIM Automation Toolkit entities and their partners according to Sections 4.1 (g) and 4.1 (i) and to the transfer of my personal data to SME BIM Automation Toolkit’s partners according to Section 4.1 (g) of the Privacy Policy.</span>
                  </label>
                  {errors.communications && <span className="error-text">{errors.communications}</span>}

                  <label className="consent-label">
                    <input
                      type="checkbox"
                      name="marketing"
                      checked={consents.marketing}
                      onChange={handleConsentChange}
                    />
                    <span>I agree to receive marketing communications from SME BIM Automation Toolkit.</span>
                  </label>

                  <p className="consent-note">
                    You may unsubscribe from these communications at any time. For more information on how to unsubscribe, our privacy practices, and how we are committed to protecting and respecting your privacy, please review our <Link to="/privacy-policy" className="privacy-link">Privacy Policy</Link>.
                  </p>

                  <p className="consent-disclaimer">
                    By clicking submit below, you consent to allow smebimautomationtoolkit.com to store and process the personal information submitted above to provide you the content requested.
                  </p>
                </div>

                <button 
                  type="submit" 
                  className="book-demo-btn"
                  disabled={isLoading}
                >
                  {isLoading ? (
                    <>
                      <div className="loading-spinner"></div>
                      Submitting...
                    </>
                  ) : (
                    'Submit'
                  )}
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BookDemoPage;