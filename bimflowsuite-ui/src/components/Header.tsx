// src/components/Header.tsx – FINAL NOV 2025 (Image Logo Version)
import React, { useState, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import GetStartedModal from "./GetStartedModal";
import logo from "../assets/images/bimflow-logo.png";   // ← YOUR LOGO HERE
import "../assets/Header.css";

type NavLink = { href: string; label: string };

const Header: React.FC = () => {
  const [open, setOpen] = useState<boolean>(false);
  const [isGetStartedModalOpen, setIsGetStartedModalOpen] = useState(false);
  const location = useLocation();

  const links: NavLink[] = [
    { href: "/", label: "Home" },
    { href: "/about", label: "About" },
    { href: "/features", label: "Features" },
    { href: "/projects", label: "Projects" },
    { href: "/blog", label: "Blog" },
    { href: "/#faq-section", label: "Faq" }, // CHANGED: "FAQ" to "Faq"
  ];

  const toggleMobile = () => setOpen(prev => !prev);
  const openGetStartedModal = () => setIsGetStartedModalOpen(true);

  // Effect to scroll to the hash section when the URL changes (e.g., after clicking Faq)
  useEffect(() => {
    if (location.hash) {
      const element = document.getElementById(location.hash.substring(1));
      if (element) {
        // Use setTimeout to ensure the element is rendered and DOM is ready
        // especially important if navigating from a different page to a hash on this page
        setTimeout(() => {
          element.scrollIntoView({ behavior: 'smooth' });
        }, 100); 
      }
    } else {
      // Optional: if you want to scroll to top when hash is cleared or on a new page without hash
      // window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  }, [location]); // Rerun this effect when location changes

  const NavItem = ({ href, label }: NavLink) => {
    // For hash links, check if the base path matches and the hash is present
    const isActive = location.pathname === href.split('#')[0] && 
                     (location.hash === (href.split('#')[1] ? `#${href.split('#')[1]}` : '')) ||
                     (location.pathname === href && !href.includes('#'));
    
    const handleClick = () => {
      setOpen(false); // Close mobile menu
      if (href.includes('#')) {
        // If it's a hash link, use Link component's default behavior,
        // which will update location.hash and trigger the useEffect above.
        // We don't need manual scroll here as useEffect handles it.
      }
    };

    return (
      <Link
        to={href}
        className={`nav__link ${isActive ? "nav__link--active" : ""}`}
        onClick={handleClick}
      >
        {label}
      </Link>
    );
  };

  return (
    <>
      <header className="header" role="banner">
        <div className="header__container">

          {/* LOGO WITH IMAGE */}
          <Link to="/" className="logo" aria-label="BIMFlow Suite Home">
            <img src={logo} alt="BIMFlow Suite" className="logo__image" />
            <span className="logo__text">BIMFlow Suite</span>
          </Link>

          <nav className="nav" aria-label="Primary navigation">
            {links.map(link => (
              <NavItem key={link.href} {...link} />
            ))}
          </nav>

          <div className="actions">
            <Link to="/login" className="btn btn--secondary">Login</Link>
            <button onClick={openGetStartedModal} className="btn btn--primary">
              Get Started
            </button>
          </div>

          <button
            className="menu-toggle"
            aria-label={open ? "Close menu" : "Open menu"}
            aria-expanded={open}
            onClick={toggleMobile}
          >
            <span></span><span></span><span></span>
          </button>
        </div>

        {/* Mobile menu */}
        <div className={`mobile-menu ${open ? "mobile-menu--open" : ""}`}>
          <nav className="mobile-nav">
            {links.map(link => (
              <NavItem key={link.href} {...link} />
            ))}
            <div className="mobile-actions">
              <Link to="/login" className="btn btn--secondary" onClick={toggleMobile}>
                Login
              </Link>
              <button
                onClick={() => { openGetStartedModal(); toggleMobile(); }}
                className="btn btn--primary"
              >
                Get Started
              </button>
            </div>
          </nav>
        </div>
      </header>

      <GetStartedModal
        isOpen={isGetStartedModalOpen}
        onClose={() => setIsGetStartedModalOpen(false)}
      />
    </>
  );
};

export default Header;