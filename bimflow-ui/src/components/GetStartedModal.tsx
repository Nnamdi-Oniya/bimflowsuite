// src/components/GetStartedModal.tsx – UPDATED NOV 2025 (Book Demo replaces IFC upload)
import React from "react";
import { useNavigate } from "react-router-dom";
import "../assets/GetStartedModal.css";

interface GetStartedModalProps {
  isOpen: boolean;
  onClose: () => void;
}

const GetStartedModal: React.FC<GetStartedModalProps> = ({ isOpen, onClose }) => {
  const navigate = useNavigate();

  const handleCreateFromScratch = () => {
    onClose();
    navigate("/generate-model"); // Intent-driven model generation wizard
  };

  const handleBookDemoViaIFC = () => {
    onClose();
    navigate("/book-demo"); // Now redirects to book-demo page (as requested)
  };

  if (!isOpen) return null;

  return (
    <div className="get-started-modal-overlay" onClick={onClose}>
      <div className="get-started-modal" onClick={(e) => e.stopPropagation()}>
        <div className="get-started-modal-header">
          <h2>Get Started with BIMFlow Suite</h2>
          <button onClick={onClose} className="close-btn" aria-label="Close modal">
            ×
          </button>
        </div>

        <div className="get-started-content">
          <p className="get-started-description">
            Choose the fastest way to experience open source BIM automation for your projects.
          </p>

          <div className="get-started-options">
            {/* Option 1 – Create New Model */}
            <button onClick={handleCreateFromScratch} className="option-btn option-btn--create">
              <div className="option-icon">🏗️</div>
              <div className="option-details">
                <h3>Create New Model</h3>
                <p>
                  Start from scratch — describe your building, bridge, road or high-rise using simple inputs or natural language. 
                  Instantly generate a fully compliant IFC 4.3 model.
                </p>
              </div>
            </button>

            {/* Option 2 – Already Have an IFC? → Now leads to Book Demo */}
            <button onClick={handleBookDemoViaIFC} className="option-btn option-btn--upload">
              <div className="option-icon">📁</div>
              <div className="option-details">
                <h3>Already Have an IFC File?</h3>
                <p>
                  Perfect! Let us show you exactly what BIMFlow Suite can do with your model — 
                  validation, compliance, quantities, costs, scheduling and more — in a personalized live demo.
                </p>
              </div>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GetStartedModal;