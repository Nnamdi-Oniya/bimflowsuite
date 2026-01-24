// src/components/ProjectModal.tsx
import React, { useState } from "react";
import "../assets/ProjectModal.css";

interface Project {
  id: number;
  title: string;
  type: string;
  status: string;
  compliance: string;
  assets: string;
  lastUpdated: string;
  teamSize: number;
  thumbnail: string;
  // Extended for modal details (add more as needed)
  description?: string;
  budget?: string;
}

interface ProjectModalProps {
  project: Project | null;
  mode: "view" | "edit";
  onClose: () => void;
  onSave?: (updatedProject: Partial<Project>) => void;
}

const ProjectModal: React.FC<ProjectModalProps> = ({ project, mode, onClose, onSave }) => {
  const [formData, setFormData] = useState({
    title: project?.title || "",
    type: project?.type || "",
    status: project?.status || "",
    compliance: project?.compliance || "",
    assets: project?.assets || "",
    teamSize: project?.teamSize || 0,
    description: project?.description || "",
    budget: project?.budget || "",
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSave = (e?: React.FormEvent<HTMLFormElement> | React.MouseEvent<HTMLButtonElement>) => {
    e?.preventDefault();
    if (onSave) {
      onSave({ ...formData, id: project?.id });
    }
    onClose(); // Close after save
    // Mock success: navigate or toast
    console.log("Project updated:", formData);
  };

  if (!project) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{mode === "view" ? "Project Details" : "Edit Project"}</h2>
          <button className="modal-close" onClick={onClose}>×</button>
        </div>
        <div className="modal-body">
          {mode === "view" ? (
            // View mode: Read-only details
            <div className="project-details-view">
              <img src={project.thumbnail} alt={project.title} className="modal-thumbnail" />
              <div className="detail-section">
                <h3>{project.title}</h3>
                <p><strong>Type:</strong> {project.type}</p>
                <p><strong>Status:</strong> <span className={`status-badge status-${project.status.toLowerCase().replace(' ', '-')}`}>{project.status}</span></p>
                <p><strong>Compliance:</strong> {project.compliance}</p>
                <p><strong>Assets:</strong> {project.assets}</p>
                <p><strong>Team Size:</strong> {project.teamSize}</p>
                <p><strong>Last Updated:</strong> {project.lastUpdated}</p>
                {project.description && <p><strong>Description:</strong> {project.description}</p>}
                {project.budget && <p><strong>Budget:</strong> {project.budget}</p>}
              </div>
            </div>
          ) : (
            // Edit mode: Form
            <form onSubmit={handleSave} className="project-edit-form">
              <div className="form-group">
                <label>Title</label>
                <input type="text" name="title" value={formData.title} onChange={handleInputChange} required />
              </div>
              <div className="form-group">
                <label>Type</label>
                <select name="type" value={formData.type} onChange={handleInputChange} required>
                  <option>High-Rise Building</option>
                  <option>Bridge Infrastructure</option>
                  <option>Road Infrastructure</option>
                </select>
              </div>
              <div className="form-group">
                <label>Status</label>
                <select name="status" value={formData.status} onChange={handleInputChange} required>
                  <option>Active</option>
                  <option>Completed</option>
                  <option>Compliance Pending</option>
                  <option>In Planning</option>
                </select>
              </div>
              <div className="form-group">
                <label>Compliance (%)</label>
                <input type="text" name="compliance" value={formData.compliance} onChange={handleInputChange} />
              </div>
              <div className="form-group">
                <label>Assets</label>
                <input type="text" name="assets" value={formData.assets} onChange={handleInputChange} />
              </div>
              <div className="form-group">
                <label>Team Size</label>
                <input type="number" name="teamSize" value={formData.teamSize} onChange={handleInputChange} min="1" />
              </div>
              <div className="form-group">
                <label>Description</label>
                <textarea name="description" value={formData.description} onChange={handleInputChange} rows={3} />
              </div>
              <div className="form-group">
                <label>Budget</label>
                <input type="text" name="budget" value={formData.budget} onChange={handleInputChange} placeholder="$0M" />
              </div>
            </form>
          )}
        </div>
        <div className="modal-footer">
          {mode === "view" ? (
            <button className="btn-secondary" onClick={onClose}>Close</button>
          ) : (
            <>
              <button type="button" className="btn-secondary" onClick={onClose}>Cancel</button>
              <button type="submit" className="btn-primary" onClick={handleSave}>Save Changes</button>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProjectModal;