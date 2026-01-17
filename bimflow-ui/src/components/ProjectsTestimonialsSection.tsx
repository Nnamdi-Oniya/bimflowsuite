import React from "react";
import "../assets/ProjectsTestimonialsSection.css";

// ✅ Import all images properly
import ModernLivingRoom from "../assets/images/ModernLivingRoom.jpg";
import Bedroom from "../assets/images/Bedroom.jpg";
import LivingSpace from "../assets/images/LivingSpace.jpg";
import MinimalistInterior from "../assets/images/MinimalistInterior.jpg";
import InteriorDesign from "../assets/images/InteriorDesign.jpg";
import ModernDesign from "../assets/images/ModernDesign.jpg";
import ContemporaryDesign from "../assets/images/ContemporaryDesign.jpg";

const ProjectsTestimonialsSection: React.FC = () => {
  return (
    <>
      {/* 🌟 Latest Projects Section */}
      <section className="latest-projects">
        <div className="latest-projects__container">
          <h2 className="latest-projects__title">Our Latest Projects</h2>
          <div className="latest-projects__grid">
            <div className="latest-projects__item">
              <img
                src={ModernLivingRoom}
                alt="Modern living room with refined textures"
                className="latest-projects__image"
              />
            </div>
            <div className="latest-projects__item">
              <img
                src={Bedroom}
                alt="Elegant and serene bedroom design"
                className="latest-projects__image"
              />
            </div>
            <div className="latest-projects__item">
              <img
                src={LivingSpace}
                alt="Spacious living area with minimal aesthetic"
                className="latest-projects__image"
              />
            </div>
            <div className="latest-projects__item">
              <img
                src={MinimalistInterior}
                alt="Minimalist interior with sleek details"
                className="latest-projects__image"
              />
            </div>
          </div>
        </div>
      </section>

      {/* 💎 Unique Design Section */}
      <section className="unique-design">
        <div className="unique-design__container">
          <div className="unique-design__images">
            <div className="unique-design__image-large">
              <img
                src={InteriorDesign}
                alt="Unique interior design showcase"
                className="unique-design__img"
              />
            </div>
            <div className="unique-design__image-grid">
              <img
                src={ModernDesign}
                alt="Modern design perspective"
                className="unique-design__img"
              />
              <img
                src={ContemporaryDesign}
                alt="Contemporary living inspiration"
                className="unique-design__img"
              />
              <img
                src={InteriorDesign}
                alt="Luxury interior detail"
                className="unique-design__img"
              />
            </div>
          </div>

          <div className="unique-design__content">
            <h2 className="unique-design__title">We Create Distinctive Spaces</h2>
            <p className="unique-design__text">
               we believe every space tells a story. Our designs
              blend functionality with elegance — balancing natural textures,
              modern aesthetics, and sustainable materials to craft experiences
              that feel as good as they look.
            </p>
          </div>
        </div>
      </section>

      {/* 💬 Testimonials Section */}
      <section className="testimonials">
        <div className="testimonials__container">
          <h2 className="testimonials__title">What Our Clients Say</h2>
          <div className="testimonials__grid">
            <div className="testimonials__card">
              <div className="testimonials__quote-icon">
                <svg width="40" height="32" viewBox="0 0 40 32" fill="#F8780F">
                  <path d="M0 32V16C0 7.168 4.8 0 16 0v6.4C10.4 6.4 8 10.4 8 16h8v16H0zm24 0V16c0-8.832 4.8-16 16-16v6.4c-5.6 0-8 4-8 9.6h8v16H24z"/>
                </svg>
              </div>
              <p className="testimonials__text">
                “Elefthéros completely transformed our home. Every detail feels intentional and inspiring — it’s more than design, it’s a lifestyle upgrade.”
              </p>
              <div className="testimonials__author">
                <h4 className="testimonials__name">Giaza Zakarberg</h4>
                <p className="testimonials__role">Homeowner</p>
              </div>
            </div>

            <div className="testimonials__card">
              <div className="testimonials__quote-icon">
                <svg width="40" height="32" viewBox="0 0 40 32" fill="#F8780F">
                  <path d="M0 32V16C0 7.168 4.8 0 16 0v6.4C10.4 6.4 8 10.4 8 16h8v16H0zm24 0V16c0-8.832 4.8-16 16-16v6.4c-5.6 0-8 4-8 9.6h8v16H24z"/>
                </svg>
              </div>
              <p className="testimonials__text">
                “Their creativity and attention to detail exceeded our expectations.
                Our new office now reflects who we are — sleek, modern, and efficient.”
              </p>
              <div className="testimonials__author">
                <h4 className="testimonials__name">Robert Arejino</h4>
                <p className="testimonials__role">Product Manager</p>
              </div>
            </div>

            <div className="testimonials__card">
              <div className="testimonials__quote-icon">
                <svg width="40" height="32" viewBox="0 0 40 32" fill="#F8780F">
                  <path d="M0 32V16C0 7.168 4.8 0 16 0v6.4C10.4 6.4 8 10.4 8 16h8v16H0zm24 0V16c0-8.832 4.8-16 16-16v6.4c-5.6 0-8 4-8 9.6h8v16H24z"/>
                </svg>
              </div>
              <p className="testimonials__text">
                “From consultation to execution, delivered perfection.
                The ambiance they created is both timeless and breathtaking.”
              </p>
              <div className="testimonials__author">
                <h4 className="testimonials__name">Mahmud Pardo</h4>
                <p className="testimonials__role">CEO, Pardo Group</p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </>
  );
};

export default ProjectsTestimonialsSection;
