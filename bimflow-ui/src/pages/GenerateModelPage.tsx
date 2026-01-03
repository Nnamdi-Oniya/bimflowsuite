// src/pages/GenerateModelPage.tsx
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../assets/GenerateModelPage.css";
import generateModelHero from "../assets/images/generateModelHero.jpg";

const GenerateModelPage: React.FC = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    projectType: "",
    projectName: "",
    description: "",
    floors: "",
    area: "",
    location: "",
    budget: "",
    timeline: "",
    specialRequirements: "",
    contactEmail: ""
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);

  const projectTypes = [
    { value: "residential", label: "🏠 Residential Building", description: "Houses, apartments, condominiums" },
    { value: "commercial", label: "🏢 Commercial Office", description: "Office buildings, retail spaces" },
    { value: "industrial", label: "🏭 Industrial Facility", description: "Factories, warehouses, plants" },
    { value: "healthcare", label: "🏥 Healthcare Facility", description: "Hospitals, clinics, medical centers" },
    { value: "educational", label: "🎓 Educational Building", description: "Schools, universities, libraries" },
    { value: "bridge", label: "🌉 Bridge Structure", description: "Highway bridges, pedestrian bridges" },
    { value: "road", label: "🛣️ Road Infrastructure", description: "Highways, streets, tunnels" },
    { value: "other", label: "🔧 Other Project", description: "Custom infrastructure projects" }
  ];

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    // Simulate API call
    setTimeout(() => {
      setIsSubmitting(false);
      setIsSubmitted(true);
      console.log('Form submitted:', formData);
    }, 2000);
  };

  const handleNewProject = () => {
    setIsSubmitted(false);
    setFormData({
      projectType: "",
      projectName: "",
      description: "",
      floors: "",
      area: "",
      location: "",
      budget: "",
      timeline: "",
      specialRequirements: "",
      contactEmail: ""
    });
  };

  if (isSubmitted) {
    return (
      <div className="generate-model-page">
        <div className="generate-model-container">
          <div className="success-state">
            <div className="success-icon">🎉</div>
            <h1>Project Submitted Successfully!</h1>
            <p>Your BIM model generation request has been received. Our engine is processing your requirements.</p>
            
            <div className="submission-details">
              <h3>Project Summary</h3>
              <div className="details-grid">
                <div className="detail-item">
                  <span className="detail-label">Project Name:</span>
                  <span className="detail-value">{formData.projectName}</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Project Type:</span>
                  <span className="detail-value">
                    {projectTypes.find(type => type.value === formData.projectType)?.label}
                  </span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Estimated Timeline:</span>
                  <span className="detail-value">{formData.timeline}</span>
                </div>
              </div>
            </div>

            <div className="next-steps">
              <h3>What Happens Next?</h3>
              <div className="steps-timeline">
                <div className="step">
                  <div className="step-number">1</div>
                  <div className="step-content">
                    <strong>Requirements Analysis</strong>
                    <p>Our system analyzes your requirements and generates optimal design options</p>
                  </div>
                </div>
                <div className="step">
                  <div className="step-number">2</div>
                  <div className="step-content">
                    <strong>Model Generation</strong>
                    <p>IFC-compliant 3D model creation with all structural elements</p>
                  </div>
                </div>
                <div className="step">
                  <div className="step-number">3</div>
                  <div className="step-content">
                    <strong>Compliance Check</strong>
                    <p>Automated validation against building codes and standards</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="success-actions">
              <button className="btn btn--primary" onClick={handleNewProject}>
                Create Another Project
              </button>
              <button className="btn btn--secondary" onClick={() => navigate('/demo')}>
                Back to Demo
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="generate-model-page">
      {/* Hero Section */}
      <section 
        className="generate-model-hero"
        style={{
          backgroundImage: `linear-gradient(rgba(78, 68, 60, 0.6), rgba(42, 36, 32, 0.6)), url(${generateModelHero})`,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          backgroundAttachment: 'fixed'
        }}
      >
        <div className="generate-model-hero__overlay"></div>
        <div className="generate-model-hero__content">
          <h1 className="generate-model-hero__title">Generate Your BIM Model</h1>
          <p className="generate-model-hero__subtitle">
            Describe your project and let BIMFlow Suite create a compliant 3D BIM model automatically
          </p>
        </div>
      </section>

      <div className="generate-model-container">
        <div className="form-container">
          <form onSubmit={handleSubmit} className="project-form">
            {/* Project Basics */}
            <div className="form-section">
              <h3 className="section-title">Project Basics</h3>
              <div className="form-grid">
                <div className="form-group">
                  <label htmlFor="projectType" className="form-label">
                    Project Type *
                  </label>
                  <select
                    id="projectType"
                    name="projectType"
                    value={formData.projectType}
                    onChange={handleInputChange}
                    className="form-select"
                    required
                  >
                    <option value="">Select project type</option>
                    {projectTypes.map(type => (
                      <option key={type.value} value={type.value}>
                        {type.label}
                      </option>
                    ))}
                  </select>
                  {formData.projectType && (
                    <div className="option-description">
                      {projectTypes.find(type => type.value === formData.projectType)?.description}
                    </div>
                  )}
                </div>

                <div className="form-group">
                  <label htmlFor="projectName" className="form-label">
                    Project Name *
                  </label>
                  <input
                    type="text"
                    id="projectName"
                    name="projectName"
                    value={formData.projectName}
                    onChange={handleInputChange}
                    className="form-input"
                    placeholder="e.g., Downtown Office Tower"
                    required
                  />
                </div>
              </div>
            </div>

            {/* Project Description */}
            <div className="form-section">
              <h3 className="section-title">Project Description</h3>
              <div className="form-group">
                <label htmlFor="description" className="form-label">
                  Describe Your Project in Detail *
                </label>
                <textarea
                  id="description"
                  name="description"
                  value={formData.description}
                  onChange={handleInputChange}
                  className="form-textarea"
                  placeholder="Describe your project requirements, features, and any specific needs. For example: '5-story office building with 2 elevators, open floor plans, glass facade, rooftop garden, and underground parking for 50 cars.'"
                  rows={4}
                  required
                />
                <div className="character-count">
                  {formData.description.length}/500 characters
                </div>
              </div>
            </div>

            {/* Project Specifications */}
            <div className="form-section">
              <h3 className="section-title">Specifications</h3>
              <div className="form-grid">
                <div className="form-group">
                  <label htmlFor="floors" className="form-label">
                    Number of Floors
                  </label>
                  <input
                    type="number"
                    id="floors"
                    name="floors"
                    value={formData.floors}
                    onChange={handleInputChange}
                    className="form-input"
                    placeholder="e.g., 10"
                    min="1"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="area" className="form-label">
                    Total Area (m²)
                  </label>
                  <input
                    type="number"
                    id="area"
                    name="area"
                    value={formData.area}
                    onChange={handleInputChange}
                    className="form-input"
                    placeholder="e.g., 5000"
                    min="1"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="location" className="form-label">
                    Location
                  </label>
                  <input
                    type="text"
                    id="location"
                    name="location"
                    value={formData.location}
                    onChange={handleInputChange}
                    className="form-input"
                    placeholder="e.g., New York, USA"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="budget" className="form-label">
                    Estimated Budget ($)
                  </label>
                  <input
                    type="number"
                    id="budget"
                    name="budget"
                    value={formData.budget}
                    onChange={handleInputChange}
                    className="form-input"
                    placeholder="e.g., 5000000"
                    min="0"
                  />
                </div>
              </div>
            </div>

            {/* Timeline & Requirements */}
            <div className="form-section">
              <h3 className="section-title">Timeline & Requirements</h3>
              <div className="form-grid">
                <div className="form-group">
                  <label htmlFor="timeline" className="form-label">
                    Project Timeline
                  </label>
                  <select
                    id="timeline"
                    name="timeline"
                    value={formData.timeline}
                    onChange={handleInputChange}
                    className="form-select"
                  >
                    <option value="">Select timeline</option>
                    <option value="1-3 months">1-3 months</option>
                    <option value="3-6 months">3-6 months</option>
                    <option value="6-12 months">6-12 months</option>
                    <option value="12+ months">12+ months</option>
                  </select>
                </div>

                <div className="form-group">
                  <label htmlFor="contactEmail" className="form-label">
                    Contact Email *
                  </label>
                  <input
                    type="email"
                    id="contactEmail"
                    name="contactEmail"
                    value={formData.contactEmail}
                    onChange={handleInputChange}
                    className="form-input"
                    placeholder="your.email@company.com"
                    required
                  />
                </div>
              </div>

              <div className="form-group">
                <label htmlFor="specialRequirements" className="form-label">
                  Special Requirements
                </label>
                <textarea
                  id="specialRequirements"
                  name="specialRequirements"
                  value={formData.specialRequirements}
                  onChange={handleInputChange}
                  className="form-textarea"
                  placeholder="Any specific building codes, sustainability requirements, accessibility needs, or other special considerations..."
                  rows={3}
                />
              </div>
            </div>

            {/* Form Actions */}
            <div className="form-actions">
              <button 
                type="button" 
                className="btn btn--secondary"
                onClick={() => navigate('/demo')}
              >
                ← Back to Demo
              </button>
              <button 
                type="submit" 
                className="btn btn--primary btn--generate"
                disabled={isSubmitting}
              >
                {isSubmitting ? (
                  <>
                    <div className="loading-spinner"></div>
                    Generating Model...
                  </>
                ) : (
                  ' Generate BIM Model'
                )}
              </button>
            </div>

            {/* Features Highlight */}
            <div className="features-highlight">
              <h4>What You'll Get</h4>
              <div className="features-grid">
                <div className="feature">
                  <span className="feature-icon">📐</span>
                  <div>
                    <strong>IFC 4.3 Compliant Model</strong>
                    <p>Industry-standard file format ready for any BIM software</p>
                  </div>
                </div>
                <div className="feature">
                  <span className="feature-icon">🛡️</span>
                  <div>
                    <strong>Automated Compliance</strong>
                    <p>Built-in checks for building codes and regulations</p>
                  </div>
                </div>
                <div className="feature">
                  <span className="feature-icon">📊</span>
                  <div>
                    <strong>Quantity Takeoff</strong>
                    <p>Automatic material and cost calculations</p>
                  </div>
                </div>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default GenerateModelPage;