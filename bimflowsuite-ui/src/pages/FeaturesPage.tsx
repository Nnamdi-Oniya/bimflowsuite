// src/pages/FeaturesPage.tsx (Updated: Contact Sales links to /book-demo)
import React, { useState } from "react";
import { Link } from "react-router-dom";
import "../assets/FeaturesPage.css";
import featuresHero from "../assets/images/features-hero.jpg";
import intentModeling from "../assets/images/intent-modeling.jpg";
import complianceCheck from "../assets/images/compliance-check.jpg";
import multiAsset from "../assets/images/multi-asset.jpg";

const FeaturesPage: React.FC = () => {
  const [activeFeature, setActiveFeature] = useState<string>("intent");

  const features = [
    {
      id: "intent",
      title: "Intent-Driven Modeling",
      description: "Transform natural language into detailed BIM models",
      icon: "🎯",
      image: intentModeling,
      details: [
        "Natural language processing for project descriptions",
        "Instant IFC 4.3 compliant model generation",
        "Support for buildings, bridges, roads, and infrastructure",
        "Real-time preview and adjustments"
      ],
      capabilities: [
        { name: "Language Understanding", value: 95 },
        { name: "Model Accuracy", value: 92 },
        { name: "Generation Speed", value: 98 }
      ]
    },
    {
      id: "compliance",
      title: "Automated Compliance",
      description: "Thousands of regulatory checks in seconds",
      icon: "🛡️",
      image: complianceCheck,
      details: [
        "Rule-based compliance engine with YAML/JSON packs",
        "Building codes and standards validation",
        "Real-time compliance scoring",
        "Detailed violation reports with suggestions"
      ],
      capabilities: [
        { name: "Check Accuracy", value: 97 },
        { name: "Processing Speed", value: 99 },
        { name: "Coverage", value: 94 }
      ]
    },
    {
      id: "multi-asset",
      title: "Multi-Asset Support",
      description: "Unified platform for all construction assets",
      icon: "🏗️",
      image: multiAsset,
      details: [
        "BuildingPack for residential and commercial structures",
        "BridgePack for span and load analysis",
        "RoadPack for alignment and corridor design",
        "HighRisePack for tall building optimization"
      ],
      capabilities: [
        { name: "Asset Types", value: 100 },
        { name: "Interoperability", value: 96 },
        { name: "Workflow Integration", value: 93 }
      ]
    },
    {
      id: "analytics",
      title: "Smart Analytics",
      description: "Advanced insights and quantity takeoffs",
      icon: "📊",
      image: intentModeling,
      details: [
        "Automatic material quantity calculations",
        "Cost estimation and scheduling",
        "Performance analytics and optimization",
        "Scenario comparison and what-if analysis"
      ],
      capabilities: [
        { name: "Calculation Accuracy", value: 96 },
        { name: "Processing Time", value: 95 },
        { name: "Insight Quality", value: 94 }
      ]
    },
    {
      id: "collaboration",
      title: "Seamless Collaboration",
      description: "Real-time teamwork across disciplines",
      icon: "🤝",
      image: complianceCheck,
      details: [
        "BCF integration for Revit and BlenderBIM",
        "Real-time commenting and markups",
        "Version control and change tracking",
        "Multi-user simultaneous editing"
      ],
      capabilities: [
        { name: "Team Coordination", value: 95 },
        { name: "File Compatibility", value: 98 },
        { name: "Real-time Sync", value: 97 }
      ]
    },
    {
      id: "open-source",
      title: "Open Source Freedom",
      description: "Community-driven innovation and transparency",
      icon: "🔓",
      image: multiAsset,
      details: [
        "MIT licensed for commercial use",
        "Extensible API for custom integrations",
        "Community rule packs and templates",
        "Transparent development process"
      ],
      capabilities: [
        { name: "Customization", value: 100 },
        { name: "Community Support", value: 90 },
        { name: "Documentation", value: 88 }
      ]
    }
  ];

  const currentFeature = features.find(f => f.id === activeFeature);

  return (
    <div className="features-page">
      {/* Hero Section */}
      <section 
  className="features-hero"
  style={{
    backgroundImage: `linear-gradient(rgba(78, 68, 60, 0.6), rgba(42, 36, 32, 0.6)), url(${featuresHero})`,
    backgroundSize: 'cover',
    backgroundPosition: 'center'
  }}
>

        <div className="features-hero__overlay"></div>
        <div className="features-hero__content">
          <h1>Powerful Features for Modern Construction</h1>
          <p>Discover how BIMFlow Suite transforms digital construction with advanced automation, compliance, and collaboration tools built for the future.</p>
          <div className="hero-stats">
            <div className="stat">
              <span className="stat-number">100%</span>
              <span className="stat-label">Open Source</span>
            </div>
            <div className="stat">
              <span className="stat-number">60s</span>
              <span className="stat-label">Model Generation</span>
            </div>
            <div className="stat">
              <span className="stat-number">10k+</span>
              <span className="stat-label">Checks/Second</span>
            </div>
          </div>
        </div>
      </section>

      {/* Features Navigation */}
      <section className="features-nav">
        <div className="container">
          <div className="features-grid">
            {features.map((feature) => (
              <button
                key={feature.id}
                className={`feature-tab ${activeFeature === feature.id ? 'feature-tab--active' : ''}`}
                onClick={() => setActiveFeature(feature.id)}
              >
                <span className="feature-tab__icon">{feature.icon}</span>
                <div className="feature-tab__content">
                  <h3>{feature.title}</h3>
                  <p>{feature.description}</p>
                </div>
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Feature Details */}
      {currentFeature && (
        <section className="feature-details">
          <div className="container">
            <div className="feature-details__content">
              <div className="feature-details__visual">
                <div className="feature-image">
                  <img src={currentFeature.image} alt={currentFeature.title} />
                  <div className="feature-badge">
                    <span className="feature-badge__icon">{currentFeature.icon}</span>
                    <span>{currentFeature.title}</span>
                  </div>
                </div>
                
                <div className="capabilities">
                  <h4>Performance Metrics</h4>
                  {currentFeature.capabilities.map((capability, index) => (
                    <div key={index} className="capability">
                      <div className="capability__header">
                        <span className="capability__name">{capability.name}</span>
                        <span className="capability__value">{capability.value}%</span>
                      </div>
                      <div className="capability__bar">
                        <div 
                          className="capability__fill" 
                          style={{ width: `${capability.value}%` }}
                        ></div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="feature-details__info">
                <h2>{currentFeature.title}</h2>
                <p className="feature-description">{currentFeature.description}</p>
                
                <div className="feature-highlights">
                  <h4>Key Capabilities</h4>
                  <ul className="highlights-list">
                    {currentFeature.details.map((detail, index) => (
                      <li key={index} className="highlight-item">
                        <span className="highlight-icon">✓</span>
                        {detail}
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="feature-actions">
                  <Link to="/demo" className="btn btn--primary">
                    Try Live Demo
                  </Link>
                  <Link to="/generate-model" className="btn btn--secondary">
                    Generate Model
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </section>
      )}

      {/* CTA Section */}
      <section className="features-cta">
        <div className="container">
          <div className="cta-content">
            <h2>Ready to Transform Your Construction Workflow?</h2>
            <p>Join thousands of architects, engineers, and contractors already using BIMFlow Suite to streamline their digital construction processes.</p>
            <div className="cta-actions">
              <Link to="/generate-model" className="btn btn--primary btn--large">
                Start Your First Project
              </Link>
              <Link to="/book-demo" className="btn btn--secondary">
                Contact Sales
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default FeaturesPage;