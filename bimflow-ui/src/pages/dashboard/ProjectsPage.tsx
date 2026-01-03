// src/pages/dashboard/ProjectsPage.tsx
import React, { useState } from "react";
import { Link } from "react-router-dom";
import {
  Search,
  Plus,
  Users,
  Calendar,
  DollarSign,
  CheckCircle,
} from "lucide-react";

// Local thumbnail images
import officeTower from "../../assets/images/office-tower.jpg";
import bridgeExpansion from "../../assets/images/bridge-expansion.jpg";
import urbanRoad from "../../assets/images/urban-road.jpg";

import "../../assets/ProjectsDash.css";
import ProjectModal from "../../components/ProjectModal";

// ──────────────────────────────────────────────────────────────
// Shared Project interface – matches what ProjectModal expects
// ──────────────────────────────────────────────────────────────
export interface Project {
  id: number;
  title: string;
  type: string;
  status: "Active" | "Completed" | "Pending Review" | "Compliance Pending";
  compliance: string;
  budget: string;
  teamSize: number;
  lastUpdated: string;
  thumbnail: string;
  description: string;
  assets: string; // ← REQUIRED: ProjectModal expects this to always exist
}

// Optional: If you want to reuse this type elsewhere, you can move it to a types file later
// e.g., src/types/Project.ts

const ProjectsPage: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [filterType, setFilterType] = useState("all");
  const [filterStatus, setFilterStatus] = useState("all");
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);
  const [showModal, setShowModal] = useState(false);

  const projects: Project[] = [
    {
      id: 1,
      title: "Downtown Office Tower",
      type: "High-Rise Building",
      status: "Active",
      compliance: "95%",
      budget: "$150M",
      teamSize: 12,
      lastUpdated: "Nov 18, 2025",
      thumbnail: officeTower,
      description: "45-story mixed-use tower with LEED Platinum target",
      assets: "IFC Model + Schedules",
    },
    {
      id: 2,
      title: "River Bridge Expansion",
      type: "Bridge Infrastructure",
      status: "Compliance Pending",
      compliance: "87%",
      budget: "$75M",
      teamSize: 18,
      lastUpdated: "Nov 17, 2025",
      thumbnail: bridgeExpansion,
      description: "Twin-span bridge with seismic retrofitting",
      assets: "Alignment + Cross-sections",
    },
    {
      id: 3,
      title: "Urban Road Corridor",
      type: "Road Infrastructure",
      status: "Completed",
      compliance: "100%",
      budget: "$40M",
      teamSize: 10,
      lastUpdated: "Oct 30, 2025",
      thumbnail: urbanRoad,
      description: "Complete street redesign with smart traffic systems",
      assets: "Corridor Model + QTO",
    },
  ];

  const filteredProjects = projects.filter((p) => {
    const matchesSearch = p.title.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesType =
      filterType === "all" || p.type.toLowerCase().includes(filterType.toLowerCase());
    const matchesStatus = filterStatus === "all" || p.status === filterStatus;
    return matchesSearch && matchesType && matchesStatus;
  });

  const openModal = (project: Project) => {
    setSelectedProject(project);
    setShowModal(true);
  };

  return (
    <div className="projects-dashboard-pro">
      {/* Header */}
      <div className="projects-header-pro">
        <div className="header-content">
          <h1>Projects</h1>
          <p>Manage all your BIM projects • Track compliance, cost & schedule in real-time</p>
        </div>
        <Link to="/dashboard/upload" className="new-project-btn-pro">
          <Plus size={24} />
          New Project
        </Link>
      </div>

      {/* Controls */}
      <div className="projects-controls-pro">
        <div className="search-bar-pro">
          <Search size={20} />
          <input
            type="text"
            placeholder="Search projects..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>

        <div className="filters-pro">
          <select value={filterType} onChange={(e) => setFilterType(e.target.value)}>
            <option value="all">All Types</option>
            <option value="building">Buildings</option>
            <option value="bridge">Bridges</option>
            <option value="road">Roads</option>
            <option value="high-rise">High-Rises</option>
          </select>

          <select value={filterStatus} onChange={(e) => setFilterStatus(e.target.value)}>
            <option value="all">All Status</option>
            <option value="Active">Active</option>
            <option value="Completed">Completed</option>
            <option value="Pending Review">Pending Review</option>
            <option value="Compliance Pending">Compliance Pending</option>
          </select>
        </div>
      </div>

      {/* Projects Grid */}
      <div className="projects-grid-pro">
        {filteredProjects.map((project) => (
          <div
            key={project.id}
            className="project-card-pro"
            onClick={() => openModal(project)}
          >
            <div className="project-thumbnail-pro">
              <img src={project.thumbnail} alt={project.title} />
              <div
                className={`status-badge-pro status-${project.status
                  .toLowerCase()
                  .replace(/ /g, "-")}`}
              >
                {project.status}
              </div>
            </div>

            <div className="project-content-pro">
              <div className="project-header-pro">
                <h3>{project.title}</h3>
                <span className="project-type-pro">{project.type}</span>
              </div>

              <div className="project-metrics-pro">
                <div className="metric-pro">
                  <CheckCircle size={18} />
                  <span>Compliance: {project.compliance}</span>
                </div>
                <div className="metric-pro">
                  <DollarSign size={18} />
                  <span>{project.budget}</span>
                </div>
                <div className="metric-pro">
                  <Users size={18} />
                  <span>Team: {project.teamSize}</span>
                </div>
                <div className="metric-pro">
                  <Calendar size={18} />
                  <span>Updated: {project.lastUpdated}</span>
                </div>
              </div>

              <p className="project-desc-pro">{project.description}</p>

              <div className="project-actions-pro">
                <button className="view-btn-pro">View Details →</button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Modal */}
      {showModal && selectedProject && (
        <ProjectModal
          project={selectedProject}
          mode="view"
          onClose={() => setShowModal(false)}
          onSave={() => {}}
        />
      )}
    </div>
  );
};

export default ProjectsPage;