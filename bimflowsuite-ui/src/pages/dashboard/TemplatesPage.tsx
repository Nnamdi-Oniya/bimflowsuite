import React from "react";
import { Link } from "react-router-dom";
import { FileText, Download, Settings, TrendingUp } from "lucide-react";
import "../../assets/TemplatesPage.css";

const TemplatesPage: React.FC = () => {
  const templates = [
    { id: 1, name: "Standard Office Building", type: "Building", description: "Basic 5-story office with parking.", packs: "BuildingPack", usage: 12 },
    { id: 2, name: "Simple Girder Bridge", type: "Bridge", description: "2-span concrete girder bridge.", packs: "BridgePack", usage: 8 },
    { id: 3, name: "Urban Road Template", type: "Road", description: "4-lane urban road with medians.", packs: "RoadPack", usage: 15 },
    { id: 4, name: "High-Rise Residential", type: "High-Rise", description: "20-story apartment with amenities.", packs: "HighRisePack", usage: 5 },
  ];

  return (
    <div className="templates-page">
      <div className="templates-header">
        <div className="header-content">
          <h1>Templates</h1>
          <p>Pre-configured BIM templates for faster project setup</p>
        </div>
        <Link to="/dashboard/settings" className="manage-templates-btn">
          <Settings size={18} />
          Manage Templates
        </Link>
      </div>

      <div className="templates-grid">
        {templates.map((template) => (
          <div key={template.id} className="template-card">
            <div className="card-header">
              <FileText size={48} className="template-icon" />
              <span className="template-type">{template.type}</span>
            </div>
            <div className="card-body">
              <h3>{template.name}</h3>
              <p>{template.description}</p>
              <div className="template-meta">
                <span className="pack">{template.packs}</span>
                <span className="usage">
                  <TrendingUp size={14} />
                  {template.usage} uses
                </span>
              </div>
            </div>
            <div className="card-footer">
              <Link to={`/dashboard/generate?template=${template.id}`} className="use-template-btn">
                <Download size={18} />
                Use Template
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TemplatesPage;