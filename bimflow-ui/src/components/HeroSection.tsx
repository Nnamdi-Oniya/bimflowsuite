// src/components/HeroSection.tsx

import React, { useState } from "react";
import GetStartedModal from "./GetStartedModal";  // Same modal as Header
import "../assets/HeroSection.css";
import heroVideoMp4 from "../assets/videos/hero-bim-demo.mp4";
import heroFallback from "../assets/images/HeroBackground.png";

const HeroSection: React.FC = () => {
  const [isGetStartedModalOpen, setIsGetStartedModalOpen] = useState(false);

  const openGetStartedModal = () => setIsGetStartedModalOpen(true);
  const closeGetStartedModal = () => setIsGetStartedModalOpen(false);

  return (
    <>
      <section className="hero" role="main" aria-label="BIMFlow Suite BIM Automation Platform">

        {/* VIDEO BACKGROUND */}
        <div className="hero__video-wrapper" aria-hidden="true">
          <video
            className="hero__video"
            autoPlay
            muted
            loop
            playsInline
            poster={heroFallback}
            preload="auto"
          >
            <source src={heroVideoMp4} type="video/mp4" />
            <img src={heroFallback} alt="BIMFlow Suite Digital Construction Automation" />
          </video>
        </div>

        {/* DARK GRADIENT OVERLAY */}
        <div className="hero__overlay" aria-hidden="true"></div>

        {/* MAIN CONTENT */}
        <div className="hero__container">
          <div className="hero__content">
            <h1 className="hero__title">
              BIM Automation <span className="hero__title-accent">for Buildings and Infrastructure</span>
            </h1>

            <p className="hero__subtitle">
              The intent driven platform that converts project requirements into detailed IFC 4.3 models ready for coordination, review and seamless delivery across building and infrastructure projects.
            </p>

            {/* CTA */}
            <div className="hero__buttons">
              <button
                onClick={openGetStartedModal}
                className="hero__btn hero__btn--primary"
                aria-label="Get started with BIMFlow Suite"
              >
                Get Started
              </button>
            </div>

            {/* FEATURES GRID */}
            <div className="hero__features">
              <div className="hero__feature">
                <span className="hero__feature-icon">✓</span> IFC Model Creation
              </div>
              <div className="hero__feature">
                <span className="hero__feature-icon">✓</span> Coordination and Issue Checking
              </div>
              <div className="hero__feature">
                <span className="hero__feature-icon">✓</span> Design Review Support
              </div>
              <div className="hero__feature">
                <span className="hero__feature-icon">✓</span> Parametric Modelling
              </div>
              <div className="hero__feature">
                <span className="hero__feature-icon">✓</span> Quantity and Cost Insights
              </div>
              <div className="hero__feature">
                <span className="hero__feature-icon">✓</span> Project Timeline Preparation
              </div>
            </div>
          </div>

          <div className="hero__visual"></div>
        </div>
      </section>

      {/* MODAL */}
      <GetStartedModal
        isOpen={isGetStartedModalOpen}
        onClose={closeGetStartedModal}
      />
    </>
  );
};

export default HeroSection;
