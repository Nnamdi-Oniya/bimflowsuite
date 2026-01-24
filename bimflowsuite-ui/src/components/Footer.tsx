// src/components/Footer.tsx
import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import "../assets/Footer.css";
// Import footer images
import roomfoot1 from "../assets/images/roomfoot1.png";
import roomfoot2 from "../assets/images/roomfoot2.png";
import roomfoot3 from "../assets/images/roomfoot3.png";
import roomfoot4 from "../assets/images/roomfoot4.png";
// Import the new logo image
import logo from "../assets/images/bimflow-logo.png"; 

// Scroll to Top Hook
const useScrollToTop = () => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const toggleVisibility = () => {
      if (window.pageYOffset > 300) {
        setIsVisible(true);
      } else {
        setIsVisible(false);
      }
    };

    window.addEventListener('scroll', toggleVisibility);

    return () => window.removeEventListener('scroll', toggleVisibility);
  }, []);

  return isVisible;
};

const Footer: React.FC = () => {
  const isScrollVisible = useScrollToTop();

  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: "smooth"
    });
  };

  return (
    <>
      {/* Scroll to Top Button */}
      <button 
        className={`scroll-to-top ${isScrollVisible ? 'visible' : ''}`}
        onClick={scrollToTop}
        aria-label="Scroll to top"
      >
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 20L12 4M12 4L5 11M12 4L19 11" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      </button>

      <footer className="footer" role="contentinfo">
        <div className="footer__container">
          {/* Main Footer Content - 4 Columns */}
          <div className="footer__main">
            
            {/* Column 1: Logo & Description */}
            <div className="footer__column">
              <div className="footer__brand">
                {/* Combined text and image logo within a single link */}
               <Link to="/" className="footer__logo-link">
                  <img 
                    src={logo} 
                    alt="BIMFlow Logo" 
                    className="footer__logo-image" 
                  />
                  <span className="footer__logo-text">BIMFlow Suite</span>
                </Link>
                <p className="footer__description">
                  Streamlining construction workflows with AI-powered BIM automation for architects, engineers, and construction professionals.
                </p>
              </div>
            </div>

            {/* Column 2: Service Links */}
            <div className="footer__column">
              <h4 className="footer__title">Services</h4>
              <ul className="footer__list">
                <li><Link to="/architecture" className="footer__link">3D Modeling</Link></li>
                <li><Link to="/design" className="footer__link">Design Automation</Link></li>
                <li><Link to="/analysis" className="footer__link">Structural Analysis</Link></li>
                <li><Link to="/planning" className="footer__link">Project Planning</Link></li>
              </ul>
            </div>

            {/* Column 3: About & Contact */}
            <div className="footer__column">
              <h4 className="footer__title">Company</h4>
              <ul className="footer__list">
                <li><Link to="/about" className="footer__link">About Us</Link></li>
                <li><Link to="/team" className="footer__link">Our Team</Link></li>
                <li><Link to="/testimonials" className="footer__link">Testimonials</Link></li>
                <li><Link to="/contact" className="footer__link">Contact Us</Link></li>
              </ul>
            </div>

            {/* Column 4: Recent Work */}
            <div className="footer__column">
              <h4 className="footer__title">Recent Projects</h4>
              <div className="footer__work-grid">
                <img src={roomfoot1} alt="Modern residential BIM project" className="footer__work-item" />
                <img src={roomfoot2} alt="Commercial space design" className="footer__work-item" />
                <img src={roomfoot3} alt="Structural analysis project" className="footer__work-item" />
                <img src={roomfoot4} alt="Architectural visualization" className="footer__work-item" />
              </div>
            </div>
          </div>

          {/* Bottom Bar */}
          <div className="footer__bottom">
            <div className="footer__copyright">
              <p>Copyright @ 2024 SME BIM Automation Toolkit | All rights reserved</p>
            </div>
            <div className="footer__social">
              <a 
                href="https://github.com" 
                target="_blank" 
                rel="noopener noreferrer"
                className="footer__social-link"
                aria-label="GitHub"
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                </svg>
              </a>
              <a 
                href="https://linkedin.com" 
                target="_blank" 
                rel="noopener noreferrer"
                className="footer__social-link"
                aria-label="LinkedIn"
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                </svg>
              </a>
              <a 
                href="https://instagram.com" 
                target="_blank" 
                rel="noopener noreferrer"
                className="footer__social-link"
                aria-label="Instagram"
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
                </svg>
              </a>
              <a 
                href="https://x.com" 
                target="_blank" 
                rel="noopener noreferrer"
                className="footer__social-link"
                aria-label="X (formerly Twitter)"
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
                </svg>
              </a>
            </div>
          </div>
        </div>
      </footer>
    </>
  );
};

export default Footer;