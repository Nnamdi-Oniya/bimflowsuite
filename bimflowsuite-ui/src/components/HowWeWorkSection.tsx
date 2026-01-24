import React from "react";
import "../assets/HowWeWorkSection.css";
import bgPattern from "../assets/images/work-bg.png";
// Ensure this path matches where you placed your video file
import cityPlanningVideo from "../assets/videos/City_Planning.mp4";

const HowWeWorkSection: React.FC = () => {
  return (
    <section
      className="how-we-work"
      id="how-we-work"
      style={{
        backgroundImage: `url(${bgPattern})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
        backgroundRepeat: "no-repeat",
      }}
    >
      <div className="how-we-work__overlay">
        <div className="how-we-work__container">
          <div className="how-we-work__header">
            <h2 className="how-we-work__title">How BIMFlow Suite Works</h2>
            <p className="how-we-work__subtitle">
              Open-source automation that turns your project intent into fully compliant IFC 4.3 models — in minutes, not weeks.
            </p>
          </div>

          <div className="how-we-work__content">
            {/* Left: Steps – Updated to match actual BIMFlow workflow */}
            <div className="how-we-work__steps">
              <div className="how-we-work__step">
                <div className="how-we-work__step-number">01</div>
                <div className="how-we-work__step-content">
                  <h3 className="how-we-work__step-title">Describe Your Project</h3>
                  <p className="how-we-work__step-text">
                    Tell us what you need — buildings, bridges, roads or high-rises — using simple forms or natural language. 
                    No BIM expertise required.
                  </p>
                </div>
              </div>

              <div className="how-we-work__step">
                <div className="how-we-work__step-number">02</div>
                <div className="how-we-work__step-content">
                  <h3 className="how-we-work__step-title">Generate IFC 4.3 Model</h3>
                  <p className="how-we-work__step-text">
                    Our parametric engine instantly creates a fully compliant 3D model with spatial hierarchy, 
                    geometry, and property sets — ready for any BIM software.
                  </p>
                </div>
              </div>

              <div className="how-we-work__step">
                <div className="how-we-work__step-number">03</div>
                <div className="how-we-work__step-content">
                  <h3 className="how-we-work__step-title">Automated Validation & Compliance</h3>
                  <p className="how-we-work__step-text">
                    The model is automatically validated for schema correctness, clash detection, 
                    and regulatory compliance (accessibility, fire safety, spatial standards).
                  </p>
                </div>
              </div>

              <div className="how-we-work__step">
                <div className="how-we-work__step-number">04</div>
                <div className="how-we-work__step-content">
                  <h3 className="how-we-work__step-title">Quantity Takeoff & Cost Estimation</h3>
                  <p className="how-we-work__step-text">
                    Extract accurate quantities, map to regional unit costs, and generate detailed 
                    material, labor, and contingency breakdowns.
                  </p>
                </div>
              </div>

              <div className="how-we-work__step">
                <div className="how-we-work__step-number">05</div>
                <div className="how-we-work__step-content">
                  <h3 className="how-we-work__step-title">Project Schedule & Reports</h3>
                  <p className="how-we-work__step-text">
                    Receive an interactive Gantt chart, compliance dashboard, and downloadable reports 
                    (PDF, CSV, JSON) — all in one click.
                  </p>
                </div>
              </div>
            </div>

            {/* Right: Video */}
            <div className="how-we-work__media-wrapper">
              <div className="how-we-work__media-inner">
                <video
                  className="how-we-work__video"
                  autoPlay
                  loop
                  muted
                  playsInline
                  src={cityPlanningVideo}
                />
              </div>
              {/* Decorative element */}
              <div className="how-we-work__media-decoration"></div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HowWeWorkSection;