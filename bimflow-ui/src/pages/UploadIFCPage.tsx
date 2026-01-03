// src/pages/UploadIFCPage.tsx
import React, { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { useNavigate } from "react-router-dom";
import "../assets/UploadIFCPage.css";
import uploadHero from "../assets/images/uploadHero.jpg"; // Add your own hero image

const UploadIFCPage: React.FC = () => {
  const navigate = useNavigate();
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isProcessed, setIsProcessed] = useState(false);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      setUploadedFile(acceptedFiles[0]);
      setIsProcessed(false);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { "model/ifc": [".ifc", ".IFC"] },
    maxFiles: 1,
    maxSize: 104857600, // 100MB
  });

  const handleProcess = () => {
    if (!uploadedFile) return;
    setIsProcessing(true);
    // Simulate processing
    setTimeout(() => {
      setIsProcessing(false);
      setIsProcessed(true);
    }, 3000);
  };

  const handleNewUpload = () => {
    setUploadedFile(null);
    setIsProcessed(false);
  };

  if (isProcessed) {
    return (
      <div className="upload-page">
        <section className="upload-hero" style={{ backgroundImage: `linear-gradient(rgba(78, 68, 60, 0.7), rgba(42, 36, 32, 0.7)), url(${uploadHero})` }}>
          <div className="upload-hero__content">
            <h1>Processing Complete!</h1>
            <p>Your IFC file has been fully analyzed</p>
          </div>
        </section>

        <div className="upload-container">
          <div className="success-state">
            <div className="success-icon">✅</div>
            <h2>Analysis Complete</h2>
            <p className="file-name">{uploadedFile?.name}</p>

            <div className="results-summary">
              <div className="summary-card">
                <span className="card-icon">✓</span>
                <div>
                  <strong>Schema Validation</strong>
                  <p>IFC4.3 compliant — No errors</p>
                </div>
              </div>
              <div className="summary-card warning">
                <span className="card-icon">⚠️</span>
                <div>
                  <strong>12 Clashes Detected</strong>
                  <p>MEP vs Structure conflicts</p>
                </div>
              </div>
              <div className="summary-card success">
                <span className="card-icon">✓</span>
                <div>
                  <strong>Compliance Check</strong>
                  <p>98% code compliance</p>
                </div>
              </div>
            </div>

            <div className="detailed-results">
              <h3>What Was Analyzed</h3>
              <div className="results-grid">
                <div className="result-item">
                  <span>Clash Detection</span>
                  <strong>12 issues found</strong>
                </div>
                <div className="result-item">
                  <span>Quantity Takeoff</span>
                  <strong>2,847 elements quantified</strong>
                </div>
                <div className="result-item">
                  <span>Cost Estimation</span>
                  <strong>$4.8M projected</strong>
                </div>
                <div className="result-item">
                  <span>Gantt Schedule</span>
                  <strong>18-month timeline generated</strong>
                </div>
              </div>
            </div>

            <div className="success-actions">
              <button className="btn btn--primary" onClick={() => navigate("/dashboard/projects")}>
                View Full Report in Dashboard
              </button>
              <button className="btn btn--secondary" onClick={handleNewUpload}>
                Upload Another File
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="upload-page">
      {/* Hero */}
      <section className="upload-hero" style={{ backgroundImage: `linear-gradient(rgba(78, 68, 60, 0.7), rgba(42, 36, 32, 0.7)), url(${uploadHero})` }}>
        <div className="upload-hero__content">
          <h1>Upload Your IFC File</h1>
          <p>Get instant validation, clash detection, compliance checks, cost estimates and project schedule</p>
        </div>
      </section>

      <div className="upload-container">
        <div className="upload-box">
          {!uploadedFile ? (
            <div
              {...getRootProps()}
              className={`dropzone ${isDragActive ? "dropzone--active" : ""}`}
            >
              <input {...getInputProps()} />
              <div className="dropzone-icon">📁</div>
              <h3>{isDragActive ? "Drop your IFC file here" : "Drag & drop your IFC file"}</h3>
              <p>or click to browse</p>
              <span className="dropzone-info">
                Supports .ifc files up to 100MB
              </span>
            </div>
          ) : (
            <div className="file-preview">
              <div className="file-icon">📄</div>
              <div className="file-details">
                <h4>{uploadedFile.name}</h4>
                <p>{(uploadedFile.size / 1024 / 1024).toFixed(2)} MB</p>
              </div>
              <button onClick={handleNewUpload} className="remove-file">×</button>
            </div>
          )}

          <div className="upload-features">
            <h3>Instant Analysis Includes</h3>
            <div className="features-grid">
              <div className="feature">
                <span className="icon">✓</span> IFC Schema Validation
              </div>
              <div className="feature">
                <span className="icon">🔍</span> Clash Detection
              </div>
              <div className="feature">
                <span className="icon">⚖️</span> Compliance Checking
              </div>
              <div className="feature">
                <span className="icon">📊</span> Quantity Takeoff
              </div>
              <div className="feature">
                <span className="icon">💰</span> Cost Estimation
              </div>
              <div className="feature">
                <span className="icon">📅</span> Gantt Schedule
              </div>
            </div>
          </div>

          <div className="upload-actions">
            <button className="btn btn--secondary" onClick={() => navigate("/")}>
              ← Back Home
            </button>
            <button
              className="btn btn--primary btn--large"
              onClick={handleProcess}
              disabled={!uploadedFile || isProcessing}
            >
              {isProcessing ? (
                <>
                  <div className="spinner"></div>
                  Processing IFC File...
                </>
              ) : (
                "Start Analysis"
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UploadIFCPage;