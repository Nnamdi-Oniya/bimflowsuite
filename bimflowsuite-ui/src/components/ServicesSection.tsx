import React from "react";
import { useNavigate } from "react-router-dom";
import "../assets/ServicesSection.css";
import room3 from "../assets/images/Livingdrawing.png";

const ServicesSection: React.FC = () => {
  const navigate = useNavigate();

  const handleDemoClick = () => {
    navigate('/demo');
  };

  const handleGenerateClick = () => {
    navigate('/generate-model');
  };

  return (
    <section className="services" id="services">
      <div className="services__container">
        {/* Left: BIM Project Showcase */}
        <div className="services__image-wrapper">
          <img
            src={room3}
            alt="BIM model showing detailed architectural design with structural elements"
            className="services__image"
          />
          {/* 3D Effect Overlay */}
          <div className="services__image-overlay">
            <div className="services__badge">
              <span className="services__badge-icon">🏗️</span>
              <span>Live BIM Preview</span>
            </div>
          </div>
        </div>

        {/* Right: BIM Platform Features */}
        <div className="services__content">
          <h2 className="services__title">
            Revolutionize Construction with 
            <span className="services__title-accent"> BIMFlow Suite</span>
          </h2>
          <p className="services__description">
            BIMFlow Suite transforms how architects, engineers, and contractors work. 
            Generate IFC-compliant models from simple descriptions, automate compliance 
            checks, and collaborate in real-time—all in one open-source platform built 
            for the future of digital construction.
          </p>
          
          {/* Updated Buttons with Navigation */}
          <div className="services__buttons">
            <button 
              className="services__btn services__btn--primary services__btn--gradient"
              onClick={handleDemoClick}
            >
              Try Interactive Demo
            </button>
            <button 
              className="services__btn services__btn--secondary"
              onClick={handleGenerateClick}
            >
              Generate BIM Model
            </button>
          </div>

          {/* Core BIM Capabilities */}
          <div className="services__cards">
            {/* Intent-Driven Modeling */}
            <div className="services__card" data-3d="true">
              <div className="services__card-icon">
                <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
                  <rect x="8" y="8" width="32" height="32" rx="4" stroke="#F8780F" strokeWidth="2" fill="none" />
                  <path d="M16 16L24 24L32 16" stroke="#F8780F" strokeWidth="2" fill="none" />
                  <path d="M16 32L24 24L32 32" stroke="#F8780F" strokeWidth="2" fill="none" />
                  <circle cx="24" cy="24" r="3" fill="#F8780F" />
                </svg>
              </div>
              <h3 className="services__card-title">Intent Driven Modeling</h3>
              <p className="services__card-text">
                Describe your project in plain language and instantly generate IFC 4.3 compliant 3D models for buildings, bridges, and infrastructure.
              </p>
            </div>

            {/* Automated Compliance */}
            <div className="services__card" data-3d="true">
              <div className="services__card-icon">
                <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
                  <path d="M24 4L8 14V34H40V14L24 4Z" stroke="#F8780F" strokeWidth="2" fill="none" />
                  <path d="M18 24L22 28L30 20" stroke="#F8780F" strokeWidth="3" strokeLinecap="round" />
                  <rect x="16" y="32" width="16" height="8" stroke="#F8780F" strokeWidth="2" fill="none" />
                </svg>
              </div>
              <h3 className="services__card-title">Automated Compliance</h3>
              <p className="services__card-text">
                Run thousands of regulatory checks in seconds with our rule-based engine. Ensure projects meet building codes and standards automatically.
              </p>
            </div>

            {/* Multi-Asset Support */}
            <div className="services__card" data-3d="true">
              <div className="services__card-icon">
                <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
                  <rect x="6" y="12" width="36" height="24" rx="3" stroke="#F8780F" strokeWidth="2" fill="none" />
                  <path d="M12 18H36" stroke="#F8780F" strokeWidth="2" />
                  <path d="M12 24H36" stroke="#F8780F" strokeWidth="2" />
                  <path d="M12 30H36" stroke="#F8780F" strokeWidth="2" />
                  <circle cx="18" cy="36" r="2" fill="#F8780F" />
                  <circle cx="30" cy="36" r="2" fill="#F8780F" />
                </svg>
              </div>
              <h3 className="services__card-title">Multi Asset Support</h3>
              <p className="services__card-text">
                Handle buildings, roads, bridges, and high-rise structures with unified workflows. One platform for all your construction needs.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ServicesSection;