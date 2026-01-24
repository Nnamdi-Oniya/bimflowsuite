import React, { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { useNavigate } from "react-router-dom";
import { 
  UploadCloud, FileCheck, CheckCircle, AlertCircle, 
  DollarSign, Calendar, Zap, X, Loader2,
  Building2, Hospital, School, LandPlot
} from "lucide-react";
import "../../assets/UploadIFCPage.css";

// Demo building types
const DEMO_BUILDINGS = [
  { id: 'mansion', name: 'Ultra Luxury Mansion', icon: Building2, description: '3-floor luxury estate with pool and premium amenities' },
  { id: 'hospital', name: 'Futuristic Hospital', icon: Hospital, description: 'Advanced medical facility with MRI and surgical theaters' },
  { id: 'office', name: 'Corporate Tower', icon: School, description: '20-story premium office with visible floor layouts' },
  { id: 'bridge', name: 'Engineering Bridge', icon: LandPlot, description: 'Architectural marvel with suspension design' }
];

const UploadIFCPage: React.FC = () => {
  const navigate = useNavigate();
  
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [selectedDemo, setSelectedDemo] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [isProcessed, setIsProcessed] = useState(false);
  const [showDemoSelector, setShowDemoSelector] = useState(false);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      const file = acceptedFiles[0];
      setUploadedFile(file);
      setIsProcessed(false);
      setProgress(0);
      setSelectedDemo(null);
      
      // Auto-select demo based on filename or show selector
      const fileName = file.name.toLowerCase();
      if (fileName.includes('house') || fileName.includes('residential') || fileName.includes('mansion')) {
        setSelectedDemo('mansion');
      } else if (fileName.includes('hospital') || fileName.includes('medical') || fileName.includes('clinic')) {
        setSelectedDemo('hospital');
      } else if (fileName.includes('office') || fileName.includes('commercial') || fileName.includes('tower')) {
        setSelectedDemo('office');
      } else if (fileName.includes('bridge') || fileName.includes('infrastructure')) {
        setSelectedDemo('bridge');
      } else {
        setShowDemoSelector(true);
      }
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 
      "model/ifc": [".ifc", ".IFC"],
      "application/octet-stream": [".ifc", ".IFC"]
    },
    maxFiles: 1,
    maxSize: 104857600, // 100MB
  });

  const handleProcess = () => {
    if (!uploadedFile) return;
    
    setIsProcessing(true);
    setProgress(0);

    // Enhanced simulation with realistic progress updates
    const stages = [
      { name: "Validating IFC Structure", duration: 1000 },
      { name: "Analyzing Building Components", duration: 1500 },
      { name: "Generating 3D Visualization", duration: 2000 },
      { name: "Calculating Quantities", duration: 1000 },
      { name: "Estimating Costs", duration: 1500 },
      { name: "Finalizing Report", duration: 1000 }
    ];

    let currentStage = 0;
    const totalDuration = stages.reduce((sum, stage) => sum + stage.duration, 0);
    
    const processStages = () => {
      if (currentStage < stages.length) {
        const stage = stages[currentStage];
        const stageProgress = (stage.duration / totalDuration) * 100;
        
        const interval = setInterval(() => {
          setProgress(prev => {
            const newProgress = prev + (stageProgress / 20);
            if (newProgress >= ((currentStage + 1) / stages.length) * 100) {
              clearInterval(interval);
              currentStage++;
              processStages();
              return Math.min(newProgress, 100);
            }
            return newProgress;
          });
        }, stage.duration / 20);
      } else {
        setIsProcessing(false);
        setIsProcessed(true);
        
        // Save project to localStorage for user to access later
        const projectData = {
          id: Date.now().toString(),
          name: uploadedFile.name,
          type: selectedDemo || 'mansion',
          uploadedAt: new Date().toISOString(),
          fileSize: uploadedFile.size,
          status: 'processed',
          complianceScore: 98.7,
          clashes: 8,
          estimatedCost: 4830000,
          duration: '18 mo'
        };
        
        // Get existing projects or initialize empty array
        const existingProjects = JSON.parse(localStorage.getItem('userProjects') || '[]');
        const updatedProjects = [...existingProjects, projectData];
        localStorage.setItem('userProjects', JSON.stringify(updatedProjects));
      }
    };

    processStages();
  };

  const handleNewUpload = () => {
    setUploadedFile(null);
    setSelectedDemo(null);
    setIsProcessed(false);
    setProgress(0);
    setShowDemoSelector(false);
  };

  const handleDemoSelect = (demoId: string) => {
    setSelectedDemo(demoId);
    setShowDemoSelector(false);
  };

  const getBuildingIcon = (buildingId: string) => {
    const building = DEMO_BUILDINGS.find(b => b.id === buildingId);
    return building ? React.createElement(building.icon, { size: 48 }) : <Building2 size={48} />;
  };

  const getBuildingName = (buildingId: string) => {
    const building = DEMO_BUILDINGS.find(b => b.id === buildingId);
    return building ? building.name : 'Building';
  };

  // --- SUCCESS STATE (DEMO DASHBOARD) ---
  if (isProcessed && uploadedFile) {
    return (
      <div className="upload-ifc-pro">
        <div className="upload-header-pro success">
          <CheckCircle size={64} className="success-icon" />
          <h1>Analysis Complete!</h1>
          <p>
            <strong>{uploadedFile.name}</strong> has been successfully processed as{" "}
            <strong>{getBuildingName(selectedDemo || 'mansion')}</strong>.
          </p>
        </div>

        {/* 3D MODEL PREVIEW SECTION */}
        <div className="model-preview-section">
          <h3>3D Model Preview</h3>
          <div className="model-preview-container">
            <div className="model-placeholder">
              {getBuildingIcon(selectedDemo || 'mansion')}
              <h4>{getBuildingName(selectedDemo || 'mansion')}</h4>
              <p>Hyper-realistic 3D model generated from your IFC file</p>
              <button 
                className="btn primary"
                onClick={() => {
                  // Show the 3D model in an embedded viewer instead of navigating to demo page
                  const viewerWindow = window.open('', '_blank');
                  if (viewerWindow) {
                    viewerWindow.document.write(`
                      <!DOCTYPE html>
                      <html>
                      <head>
                        <title>3D Model Viewer - ${uploadedFile.name}</title>
                        <style>
                          body { margin: 0; padding: 0; background: #1a1a1a; color: white; font-family: Arial, sans-serif; }
                          .viewer-header { padding: 1rem; background: #2a2a2a; text-align: center; }
                          .viewer-container { width: 100vw; height: calc(100vh - 60px); display: flex; align-items: center; justify-content: center; }
                          .model-info { max-width: 600px; text-align: center; }
                        </style>
                      </head>
                      <body>
                        <div class="viewer-header">
                          <h2>3D BIM Model Viewer - ${uploadedFile.name}</h2>
                          <p>Building Type: ${getBuildingName(selectedDemo || 'mansion')}</p>
                        </div>
                        <div class="viewer-container">
                          <div class="model-info">
                            <h3>🚀 3D Model Generated Successfully!</h3>
                            <p>Your IFC file has been processed and converted into a detailed 3D BIM model.</p>
                            <p><strong>Features:</strong></p>
                            <ul style="text-align: left; display: inline-block;">
                              <li>Full 3D visualization with orbit controls</li>
                              <li>Building component analysis</li>
                              <li>Material and texture mapping</li>
                              <li>Structural element identification</li>
                            </ul>
                            <p style="margin-top: 2rem; color: #888;">
                              Note: In a production environment, this would display your actual 3D model using Three.js or similar technology.
                            </p>
                          </div>
                        </div>
                      </body>
                      </html>
                    `);
                  }
                }}
              >
                🚀 View 3D Model
              </button>
            </div>
          </div>
        </div>

        <div className="success-grid-pro">
          <div className="metric-card-pro compliance">
            <Zap size={32} />
            <strong>98.7%</strong>
            <span>Model Compliance</span>
          </div>
          <div className="metric-card-pro clashes">
            <AlertCircle size={32} />
            <strong>8</strong>
            <span>Clashes Detected</span>
          </div>
          <div className="metric-card-pro cost">
            <DollarSign size={32} />
            <strong>$4.83M</strong>
            <span>Estimated Cost</span>
          </div>
          <div className="metric-card-pro schedule">
            <Calendar size={32} />
            <strong>18 mo</strong>
            <span>Project Duration</span>
          </div>
        </div>

        <div className="success-actions-pro">
          <button 
            className="btn primary large"
            onClick={() => {
              // Show the 3D model in an embedded viewer
              const viewerWindow = window.open('', '_blank');
              if (viewerWindow) {
                viewerWindow.document.write(`
                  <!DOCTYPE html>
                  <html>
                  <head>
                    <title>3D BIM Model - ${uploadedFile.name}</title>
                    <style>
                      body { margin: 0; padding: 0; background: #1a1a1a; color: white; font-family: Arial, sans-serif; }
                      .viewer-header { padding: 1rem; background: #2a2a2a; text-align: center; }
                      .viewer-content { padding: 2rem; text-align: center; }
                      .features { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 2rem 0; }
                      .feature { background: #333; padding: 1rem; border-radius: 8px; }
                    </style>
                  </head>
                  <body>
                    <div class="viewer-header">
                      <h1>🏗️ 3D BIM Model Viewer</h1>
                      <p>Project: ${uploadedFile.name} | Type: ${getBuildingName(selectedDemo || 'mansion')}</p>
                    </div>
                    <div class="viewer-content">
                      <h2>Interactive 3D Model Ready</h2>
                      <p>Your building model has been successfully processed and is ready for exploration.</p>
                      
                      <div class="features">
                        <div class="feature">
                          <h3>🔍 Explore Components</h3>
                          <p>Click on building elements to see detailed information</p>
                        </div>
                        <div class="feature">
                          <h3>📐 Take Measurements</h3>
                          <p>Measure distances and areas directly in the 3D view</p>
                        </div>
                        <div class="feature">
                          <h3>🎨 Material View</h3>
                          <p>Toggle between different material representations</p>
                        </div>
                        <div class="feature">
                          <h3>📊 Data Insights</h3>
                          <p>Access BIM data for each building component</p>
                        </div>
                      </div>
                      
                      <p style="color: #F8780F; font-weight: bold;">
                        This 3D viewer would display your actual building model in a production environment.
                      </p>
                    </div>
                  </body>
                  </html>
                `);
              }
            }}
          >
            🏗️ Open 3D Model
          </button>
          <button 
            className="btn secondary large" 
            onClick={() => navigate("/dashboard/compliance", { 
              state: { 
                projectName: uploadedFile.name,
                buildingType: selectedDemo || 'mansion',
                file: uploadedFile
              }
            })}
          >
            📊 Run Compliance Analysis
          </button>
          <button className="btn outline large" onClick={handleNewUpload}>
            📁 Upload Another IFC
          </button>
        </div>
      </div>
    );
  }

  // --- DEMO SELECTOR MODAL ---
  if (showDemoSelector) {
    return (
      <div className="upload-ifc-pro">
        <div className="upload-header-pro">
          <h1>Select Building Type</h1>
          <p>Choose the type of building for 3D visualization</p>
        </div>

        <div className="demo-selector-grid">
          {DEMO_BUILDINGS.map((building) => (
            <div
              key={building.id}
              className={`demo-building-card ${selectedDemo === building.id ? 'selected' : ''}`}
              onClick={() => handleDemoSelect(building.id)}
            >
              <div className="building-icon">
                {React.createElement(building.icon, { size: 48 })}
              </div>
              <h3>{building.name}</h3>
              <p>{building.description}</p>
              <div className="building-features">
                {building.id === 'mansion' && (
                  <>🏊 Pool • 🎬 Cinema • 🏋️ Gym • 🌿 Garden</>
                )}
                {building.id === 'hospital' && (
                  <>🏥 MRI • 🏥 Surgery • 🏥 ICU • 🏥 Pharmacy</>
                )}
                {building.id === 'office' && (
                  <>🏢 Floors • 💼 Offices • ☕ Lounge • 🌿 Terrace</>
                )}
                {building.id === 'bridge' && (
                  <>🌉 Suspension • 🏗️ Pillars • 🛣️ Roadway • 💡 Lighting</>
                )}
              </div>
            </div>
          ))}
        </div>

        <div className="demo-selector-actions">
          <button className="btn outline" onClick={handleNewUpload}>
            ← Back to Upload
          </button>
          <button
            className="btn primary large"
            onClick={() => setShowDemoSelector(false)}
            disabled={!selectedDemo}
          >
            Confirm Selection
          </button>
        </div>
      </div>
    );
  }

  // --- MAIN UPLOAD STATE ---
  return (
    <div className="upload-ifc-pro">
      <div className="upload-header-pro">
        <h1>Upload IFC Model</h1>
        <p>Drop your .ifc file to instantly validate structure and generate 5D insights</p>
      </div>

      <div className="upload-card-pro">
        {/* DROPZONE AREA */}
        <div className="upload-dropzone" {...getRootProps()}>
          <input {...getInputProps()} />
          
          {!uploadedFile ? (
            <div className={`dropzone-content ${isDragActive ? "active" : ""}`}>
              <UploadCloud size={64} className="upload-icon" />
              <h3>{isDragActive ? "Drop here..." : "Drag & drop your IFC file"}</h3>
              <p>or <span className="browse-link">click to browse</span></p>
              <small>Supports .ifc • Max 100MB • Auto 3D model generation</small>
            </div>
          ) : (
            <div className="file-preview-pro">
              <FileCheck size={48} className="file-icon valid" />
              
              <div className="file-details">
                <h4>{uploadedFile.name}</h4>
                <p>{(uploadedFile.size / 1024 / 1024).toFixed(2)} MB</p>
                
                {selectedDemo && (
                  <div className="demo-selection-info">
                    <span className="demo-badge">
                      {getBuildingIcon(selectedDemo)}
                      {getBuildingName(selectedDemo)}
                    </span>
                    <button 
                      className="change-demo-btn"
                      onClick={(e) => {
                        e.stopPropagation();
                        setShowDemoSelector(true);
                      }}
                    >
                      Change
                    </button>
                  </div>
                )}
                
                <span className="status-text valid">
                  ✅ Ready for 3D Model Generation
                </span>
              </div>

              <button className="remove-file" onClick={(e) => { e.stopPropagation(); handleNewUpload(); }}>
                <X size={24} />
              </button>
            </div>
          )}
        </div>

        {/* PROCESSING BAR */}
        {isProcessing && (
          <div className="processing-bar">
            <div className="progress-fill" style={{ width: `${progress}%` }}></div>
            <div className="progress-text">
              Generating 3D Model & Analysis... {Math.round(progress)}%
            </div>
          </div>
        )}

        {/* DEMO BUILDING PREVIEW */}
        {selectedDemo && !isProcessing && (
          <div className="demo-preview-section">
            <h3>3D Model Preview</h3>
            <div className="demo-preview-card">
              <div className="demo-preview-icon">
                {getBuildingIcon(selectedDemo)}
              </div>
              <div className="demo-preview-info">
                <h4>{getBuildingName(selectedDemo)}</h4>
                <p>Hyper-realistic 3D model will be generated with:</p>
                <ul>
                  {selectedDemo === 'mansion' && (
                    <>
                      <li>🏊 Infinity pool & water features</li>
                      <li>🎬 Private cinema room</li>
                      <li>🏋️ Personal gym & spa</li>
                      <li>🌿 Landscaped gardens</li>
                    </>
                  )}
                  {selectedDemo === 'hospital' && (
                    <>
                      <li>🏥 Advanced MRI center</li>
                      <li>🏥 Surgical theaters</li>
                      <li>🏥 ICU & patient suites</li>
                      <li>🏥 Research laboratories</li>
                    </>
                  )}
                  {selectedDemo === 'office' && (
                    <>
                      <li>🏢 Visible floor layouts</li>
                      <li>💼 Executive offices</li>
                      <li>☕ Breakout lounges</li>
                      <li>🌿 Rooftop terrace</li>
                    </>
                  )}
                  {selectedDemo === 'bridge' && (
                    <>
                      <li>🌉 Suspension design</li>
                      <li>🏗️ Structural pillars</li>
                      <li>🛣️ Roadway markings</li>
                      <li>💡 Night lighting</li>
                    </>
                  )}
                </ul>
              </div>
            </div>
          </div>
        )}

        {/* FEATURES LIST */}
        <div className="features-pro">
          <h3>Automatic Analysis Includes</h3>
          <div className="features-grid-pro">
            <div className="feature-item active">
              <CheckCircle size={20} /> 
              <span>IFC Schema Validation</span>
            </div>
            <div className="feature-item active">
              <CheckCircle size={20} /> 
              <span>3D Model Generation</span>
            </div>
            <div className="feature-item">
              <CheckCircle size={20} /> 
              <span>Clash Detection (Hard/Soft)</span>
            </div>
            <div className="feature-item">
              <CheckCircle size={20} /> 
              <span>Compliance Checking</span>
            </div>
            <div className="feature-item">
              <CheckCircle size={20} /> 
              <span>Quantity Takeoff</span>
            </div>
            <div className="feature-item">
              <CheckCircle size={20} /> 
              <span>5D Cost Estimation</span>
            </div>
            <div className="feature-item">
              <CheckCircle size={20} /> 
              <span>4D Schedule Generation</span>
            </div>
            <div className="feature-item">
              <CheckCircle size={20} /> 
              <span>BCF & PDF Reports</span>
            </div>
          </div>
        </div>

        <div className="upload-actions-pro">
          <button className="btn outline" onClick={() => navigate("/dashboard")}>
            ← Back to Dashboard
          </button>
          
          <button
            className="btn primary large"
            onClick={handleProcess}
            disabled={!uploadedFile || isProcessing || !selectedDemo}
          >
            {isProcessing ? (
              <>
                <Loader2 size={20} className="animate-spin" />
                Processing...
              </>
            ) : (
              "🚀 Generate 3D Model & Analyze"
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default UploadIFCPage;