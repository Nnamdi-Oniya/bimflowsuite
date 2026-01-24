import React from "react";
import { useNavigate } from "react-router-dom";
import aboutHero from "../assets/images/aboutHero.jpg";

import "../assets/AboutPage.css";

const AboutPage: React.FC = () => {
  const navigate = useNavigate();

  const teamMembers = [
    {
      name: "Nnamdi Innocent Oniya",
      role: "Founder & Chief Architect",
      bio: "Visionary leader democratizing BIM for SMEs worldwide",
      avatar: "👨‍💼"
    },
    {
      name: "Engineering Team",
      role: "Core Development",
      bio: "Building the future of open-source construction tech",
      avatar: "👨‍💻"
    },
    {
      name: "Community",
      role: "Contributors & Partners",
      bio: "Global network of innovators and early adopters",
      avatar: "🌍"
    }
  ];

  const milestones = [
    { year: "2024", title: "Foundation", description: "BIMFlow Suite concept and initial development" },
    { year: "2025", title: "Launch", description: "Public release and open-source community building" },
    { year: "2026", title: "Growth", description: "150+ GitHub stars, 10 SME pilots, global adoption" },
    { year: "2027+", title: "Scale", description: "Industry standard for accessible BIM automation" }
  ];

  const values = [
    {
      icon: "🌟",
      title: "Open & Accessible",
      description: "100% open-source commitment. No hidden costs, no vendor lock-in."
    },
    {
      icon: "🎯",
      title: "Innovation First",
      description: "Pushing boundaries with advanced automation and intent-based modeling."
    },
    {
      icon: "🤝",
      title: "Community Driven",
      description: "Built by the industry, for the industry. Your feedback shapes our roadmap."
    },
    {
      icon: "⚡",
      title: "Performance Focused",
      description: "Enterprise-grade speed and reliability without enterprise pricing."
    }
  ];

  return (
    <div className="app-container">
     
      <main className="main-content" role="main">
        <div className="about-page">
          {/* Hero Section */}
          <section 
            className="about-hero"
            style={{
              backgroundImage: `linear-gradient(rgba(78, 68, 60, 0.6), rgba(42, 36, 32, 0.6)), url(${aboutHero})`,
              backgroundSize: 'cover',
              backgroundPosition: 'center',
              backgroundAttachment: 'fixed'
            }}
          >
            <div className="about-hero__overlay"></div>
            <div className="about-hero__content">
              <h1 className="about-hero__title">
                Democratizing Digital Construction
              </h1>
              <p className="about-hero__subtitle">
                BIMFlow Suite is on a mission to make Building Information Modeling 
                accessible to every SME, architect, and engineer worldwide through 
                open-source innovation and advanced automation.
              </p>
            </div>
          </section>

          {/* Mission & Vision */}
          <section className="mission-section">
            <div className="section-container">
              <div className="mission-grid">
                <div className="mission-card mission-card--primary">
                  <div className="mission-icon">🎯</div>
                  <h2>Our Mission</h2>
                  <p>
                    To eliminate barriers preventing SMEs from adopting BIM by providing 
                    a free, powerful, and intuitive platform that automates model generation, 
                    compliance checking, and project analytics across all construction asset types.
                  </p>
                </div>
                <div className="mission-card mission-card--secondary">
                  <div className="mission-icon">🏗️</div>
                  <h2>Our Vision</h2>
                  <p>
                    To become the global standard for accessible BIM automation, empowering 
                    millions of construction professionals to deliver better projects faster 
                    while fostering a thriving open-source ecosystem.
                  </p>
                </div>
              </div>
            </div>
          </section>

          {/* The Problem */}
          <section className="problem-section">
            <div className="section-container">
              <div className="section-header">
                <h2 className="section-title">The Challenge We're Solving</h2>
                <p className="section-subtitle">
                  Despite industry-wide digital transformation initiatives, BIM adoption 
                  among SMEs remains critically low
                </p>
              </div>
              <div className="problem-stats">
                <div className="problem-stat">
                  <span className="stat-number">&lt;35%</span>
                  <span className="stat-label">SME BIM Adoption Rate</span>
                </div>
                <div className="problem-stat">
                  <span className="stat-number">$10K+</span>
                  <span className="stat-label">Annual Software Costs</span>
                </div>
                <div className="problem-stat">
                  <span className="stat-number">6+ months</span>
                  <span className="stat-label">Training Time Required</span>
                </div>
              </div>
              <div className="problem-list">
                <div className="problem-item">
                  <span className="problem-icon">💰</span>
                  <div>
                    <h3>High Costs</h3>
                    <p>Enterprise BIM suites cost thousands annually, excluding training</p>
                  </div>
                </div>
                <div className="problem-item">
                  <span className="problem-icon">🎓</span>
                  <div>
                    <h3>Steep Learning Curve</h3>
                    <p>Complex interfaces require months of specialized training</p>
                  </div>
                </div>
                <div className="problem-item">
                  <span className="problem-icon">🔒</span>
                  <div>
                    <h3>Vendor Lock-in</h3>
                    <p>Proprietary formats limit interoperability and flexibility</p>
                  </div>
                </div>
                <div className="problem-item">
                  <span className="problem-icon">⚙️</span>
                  <div>
                    <h3>Manual Processes</h3>
                    <p>Compliance checking and validation remain time-consuming</p>
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* Our Values */}
          <section className="values-section">
            <div className="section-container">
              <div className="section-header">
                <h2 className="section-title">Our Core Values</h2>
                <p className="section-subtitle">
                  Principles that guide every decision we make
                </p>
              </div>
              <div className="values-grid">
                {values.map((value, index) => (
                  <div key={index} className="value-card">
                    <div className="value-icon">{value.icon}</div>
                    <h3>{value.title}</h3>
                    <p>{value.description}</p>
                  </div>
                ))}
              </div>
            </div>
          </section>

          {/* Timeline */}
          <section className="timeline-section">
            <div className="section-container">
              <div className="section-header">
                <h2 className="section-title">Our Journey</h2>
                <p className="section-subtitle">
                  From concept to global impact
                </p>
              </div>
              <div className="timeline">
                {milestones.map((milestone, index) => (
                  <div key={index} className="timeline-item">
                    <div className="timeline-marker"></div>
                    <div className="timeline-content">
                      <span className="timeline-year">{milestone.year}</span>
                      <h3 className="timeline-title">{milestone.title}</h3>
                      <p className="timeline-description">{milestone.description}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </section>

          {/* Team */}
          <section className="team-section">
            <div className="section-container">
              <div className="section-header">
                <h2 className="section-title">Meet the Team</h2>
                <p className="section-subtitle">
                  Passionate innovators building the future of construction
                </p>
              </div>
              <div className="team-grid">
                {teamMembers.map((member, index) => (
                  <div key={index} className="team-card">
                    <div className="team-avatar">{member.avatar}</div>
                    <h3 className="team-name">{member.name}</h3>
                    <p className="team-role">{member.role}</p>
                    <p className="team-bio">{member.bio}</p>
                  </div>
                ))}
              </div>
            </div>
          </section>

          {/* CTA */}
          <section className="about-cta">
            <div className="cta-container">
              <h2>Join Our Mission</h2>
              <p>
                Be part of the movement democratizing digital construction. 
                Whether you're a developer, architect, or SME owner, there's a place for you.
              </p>
              <div className="cta-buttons">
                <button 
                  className="cta-btn cta-btn--primary"
                  onClick={() => navigate('/book-demo')}
                >
                  Get Involved
                </button>
                <button 
                  className="cta-btn cta-btn--secondary"
                  onClick={() => window.open('https://github.com', '_blank')}
                >
                  View on GitHub
                </button>
              </div>
            </div>
          </section>
        </div>
      </main>
     
    </div>
  );
};

export default AboutPage;