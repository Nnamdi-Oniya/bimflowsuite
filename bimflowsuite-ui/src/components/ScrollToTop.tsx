// src/components/ScrollToTop.tsx
import { useEffect } from "react";
import { useLocation } from "react-router-dom";

const ScrollToTop = () => {
  const { pathname } = useLocation();

  useEffect(() => {
    // Ensures window scrolls to top after navigation
    window.scrollTo({
      top: 0,
      behavior: "smooth", // can change to "auto" if you want instant jump
    });
  }, [pathname]);

  return null;
};

export default ScrollToTop;
