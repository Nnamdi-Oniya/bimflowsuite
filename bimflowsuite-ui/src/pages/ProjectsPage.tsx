import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../assets/ProjectsPage.css";
import projectsHero from "../assets/images/projects-hero.jpg";
import residentialBuilding from "../assets/images/ResidentialBuilding.jpg";
import modernOffice from "../assets/images/ModernOffice.jpg";
import bridge from "../assets/images/Bridge.jpg";
import urbanTransportation from "../assets/images/UrbanTransportation.jpg";
import highRise from "../assets/images/HighRise.jpg";
import hospital from "../assets/images/Hospital.jpg";

const ProjectsPage: React.FC = () => {
  const navigate = useNavigate();
  const [activeCategory, setActiveCategory] = useState<string>("all");

  const categories = [
    { id: "all", label: "All Projects", icon: "🏗️" },
    { id: "buildings", label: "Buildings", icon: "🏢" },
    { id: "bridges", label: "Bridges", icon: "🌉" },
    { id: "roads", label: "Roads", icon: "🛣️" },
    { id: "highrise", label: "High-Rise", icon: "🏙️" }
  ];

  const projects = [
    {
      id: 1,
      category: "buildings",
      title: "Modern Residential Complex",
      location: "London, UK",
      year: "2025",
      description: "3-story apartment building with 12 units, solar panels, and underground parking",
      stats: { floors: "3", units: "12", area: "2,400 m²" },
      image: residentialBuilding,
      tags: ["Residential", "Sustainable", "IFC 4.3"]
    },
    {
      id: 2,
      category: "buildings",
      title: "Commercial Office Tower",
      location: "Manchester, UK",
      year: "2025",
      description: "5-story modern office with open floor plans and green spaces",
      stats: { floors: "5", capacity: "500", area: "8,000 m²" },
      image: modernOffice,
      tags: ["Commercial", "LEED Certified", "Smart Building"]
    },
    {
      id: 3,
      category: "bridges",
      title: "Highway Bridge Infrastructure",
      location: "Birmingham, UK",
      year: "2024",
      description: "150-meter concrete bridge with 4 traffic lanes and pedestrian walkways",
      stats: { span: "150m", lanes: "4", load: "HL-93" },
      image: bridge,
      tags: ["Infrastructure", "Concrete", "Heavy Load"]
    },
    {
      id: 4,
      category: "roads",
      title: "Urban Corridor Development",
      location: "Leeds, UK",
      year: "2025",
      description: "Multi-lane urban road with bike lanes and smart traffic systems",
      stats: { length: "3.5km", lanes: "6", width: "24m" },
      image: urbanTransportation,
      tags: ["Transportation", "Smart City", "Sustainable"]
    },
    {
      id: 5,
      category: "highrise",
      title: "Luxury High-Rise Tower",
      location: "Edinburgh, UK",
      year: "2025",
      description: "25-story residential tower with panoramic views and premium amenities",
      stats: { floors: "25", units: "120", height: "85m" },
      image: highRise,
      tags: ["High-Rise", "Luxury", "Mixed-Use"]
    },
    {
      id: 6,
      category: "buildings",
      title: "Healthcare Facility",
      location: "Bristol, UK",
      year: "2024",
      description: "Modern hospital with emergency department and operating theaters",
      stats: { floors: "4", beds: "200", area: "12,000 m²" },
      image: hospital,
      tags: ["Healthcare", "Critical Infrastructure", "Accessible"]
    }
  ];

  const filteredProjects = activeCategory === "all" 
    ? projects 
    : projects.filter(p => p.category === activeCategory);

  return (
    <div className="app-container">
     
      <main className="main-content" role="main">
        <div className="projects-page">
          {/* Hero Section with Background Image */}
          <section 
            className="projects-hero"
            style={{
              backgroundImage: `linear-gradient(rgba(78, 68, 60, 0.6), rgba(42, 36, 32, 0.6)), url(${projectsHero})`,
              backgroundSize: 'cover',
              backgroundPosition: 'center',
              backgroundAttachment: 'fixed'
            }}
          >
            <div className="projects-hero__overlay"></div>
            <div className="projects-hero__content">
              <div className="hero-badge">
                <span className="badge-icon">🏗️</span>
                <span>Real-World BIM Projects</span>
              </div>
              <h1 className="projects-hero__title">
                Showcase of Excellence
              </h1>
              <p className="projects-hero__subtitle">
                Explore our portfolio of BIM-automated projects across buildings, 
                bridges, roads, and high-rise structures. Each project demonstrates 
                the power of advanced automation and open standards.
              </p>
              <div className="hero-stats">
                <div className="stat-item">
                  <span className="stat-value">50+</span>
                  <span className="stat-label">Projects Completed</span>
                </div>
                <div className="stat-item">
                  <span className="stat-value">4</span>
                  <span className="stat-label">Asset Types</span>
                </div>
                <div className="stat-item">
                  <span className="stat-value">100%</span>
                  <span className="stat-label">IFC Compliant</span>
                </div>
              </div>
            </div>
          </section>

          {/* Category Filter */}
          <section className="category-filter-section">
            <div className="section-container">
              <div className="category-filters">
                {categories.map((cat) => (
                  <button
                    key={cat.id}
                    className={`category-btn ${activeCategory === cat.id ? 'category-btn--active' : ''}`}
                    onClick={() => setActiveCategory(cat.id)}
                  >
                    <span className="category-icon">{cat.icon}</span>
                    <span>{cat.label}</span>
                  </button>
                ))}
              </div>
            </div>
          </section>

          {/* Projects Grid */}
          <section className="projects-grid-section">
            <div className="section-container">
              <div className="projects-grid">
                {filteredProjects.map((project) => (
                  <div key={project.id} className="project-card">
                    <div className="project-card__image-wrapper">
                      <img 
                        src={project.image} 
                        alt={project.title}
                        className="project-card__image"
                      />
                      <div className="project-card__overlay">
                        <button className="view-details-btn">
                          View Details
                        </button>
                      </div>
                    </div>
                    <div className="project-card__content">
                      <div className="project-card__header">
                        <h3 className="project-card__title">{project.title}</h3>
                        <div className="project-card__meta">
                          <span className="meta-location">📍 {project.location}</span>
                          <span className="meta-year">📅 {project.year}</span>
                        </div>
                      </div>
                      <p className="project-card__description">{project.description}</p>
                      <div className="project-card__stats">
                        {Object.entries(project.stats).map(([key, value]) => (
                          <div key={key} className="stat-badge">
                            <span className="stat-key">{key}</span>
                            <span className="stat-value">{value}</span>
                          </div>
                        ))}
                      </div>
                      <div className="project-card__tags">
                        {project.tags.map((tag, index) => (
                          <span key={index} className="project-tag">{tag}</span>
                        ))}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </section>

          {/* CTA Section */}
          <section className="projects-cta">
            <div className="cta-container">
              <h2>Start Your Own Project</h2>
              <p>
                Ready to bring your vision to life with BIMFlow Suite? 
                Generate your first BIM model in minutes.
              </p>
              <div className="cta-buttons">
                <button 
                  className="cta-btn cta-btn--primary"
                  onClick={() => navigate('/demo')}
                >
                  Try Demo
                </button>
                <button 
                  className="cta-btn cta-btn--secondary"
                  onClick={() => navigate('/generate-model')}
                >
                  Generate Model
                </button>
              </div>
            </div>
          </section>
        </div>
      </main>
    
    </div>
  );
};

export default ProjectsPage;