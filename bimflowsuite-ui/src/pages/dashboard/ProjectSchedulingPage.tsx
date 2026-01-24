// src/pages/dashboard/ProjectSchedulingPage.tsx
import React, { useRef } from "react";
import Plot from "react-plotly.js";
import type { PlotParams } from "react-plotly.js";
import "../../assets/ProjectSchedulingPage.css";

// 1. Define custom interface for the internal Plotly methods
interface PlotlyCustomRef {
  plotly: {
    toImage: (options: { format: string; height: number; width: number; scale?: number }) => Promise<string>;
  };
}

// Proper ref type for the Component
type PlotlyRef = React.ElementRef<typeof Plot>;

const ProjectSchedulingPage: React.FC = () => {
  const plotRef = useRef<PlotlyRef>(null);

  const tasks = [
    { Task: "Project Kick-off", Start: "2026-01-01", Finish: "2026-01-07", Type: "Milestone", Color: "#10b981", Critical: false },
    { Task: "Site Preparation & Mobilization", Start: "2026-01-08", Finish: "2026-01-31", Type: "Task", Color: "#f8780f", Critical: false },
    { Task: "Piling & Deep Foundations", Start: "2026-02-01", Finish: "2026-03-15", Type: "Task", Color: "#10b981", Critical: true },
    { Task: "Foundation Raft & Basement", Start: "2026-03-01", Finish: "2026-04-30", Type: "Task", Color: "#3b82f6", Critical: true },
    { Task: "Ground Floor Slab", Start: "2026-05-01", Finish: "2026-05-20", Type: "Task", Color: "#3b82f6", Critical: false },
    { Task: "Structural Frame (Columns & Core)", Start: "2026-04-15", Finish: "2026-08-31", Type: "Task", Color: "#1e40af", Critical: true },
    { Task: "Floor Slabs (Level 1–10)", Start: "2026-06-01", Finish: "2026-11-30", Type: "Task", Color: "#2563eb", Critical: true },
    { Task: "Facade & Envelope", Start: "2026-09-01", Finish: "2027-03-15", Type: "Task", Color: "#7c3aed", Critical: false },
    { Task: "MEP Rough-In (Per Floor)", Start: "2026-07-01", Finish: "2027-02-28", Type: "Task", Color: "#8b5cf6", Critical: false },
    { Task: "Interior Partitions & Drywall", Start: "2026-11-01", Finish: "2027-04-15", Type: "Task", Color: "#f59e0b", Critical: false },
    { Task: "Architectural Finishes", Start: "2027-02-01", Finish: "2027-05-20", Type: "Task", Color: "#f97316", Critical: true },
    { Task: "MEP Final Fit-Out & Testing", Start: "2027-03-01", Finish: "2027-05-31", Type: "Task", Color: "#a855f7", Critical: false },
    { Task: "Testing & Commissioning", Start: "2027-05-15", Finish: "2027-06-15", Type: "Task", Color: "#ec4899", Critical: true },
    { Task: "Handover & Closeout", Start: "2027-06-16", Finish: "2027-06-30", Type: "Milestone", Color: "#ef4444", Critical: false },
  ];

  const data: PlotParams["data"] = [{
    x: tasks.map(t => t.Start),
    y: tasks.map(t => t.Task),
    text: tasks.map(t => `${t.Task}<br>${t.Start} → ${t.Finish}`),
    mode: "lines+markers",
    name: "Schedule",
    type: "bar",
    orientation: "h",
    marker: {
      color: tasks.map(t => t.Color),
      line: {
        color: tasks.map(t => t.Critical ? "#ef4444" : "#ffffff"),
        width: tasks.map(t => t.Critical ? 4 : 1),
      },
      opacity: 0.9,
    },
    hovertemplate: "<b>%{y}</b><br>%{text}<extra></extra>",
  }];

  const layout: Partial<PlotParams["layout"]> = {
    title: {
      text: "<b>Project Gantt Chart – Auto-Generated from IFC Model</b>",
      font: { size: 24, color: "#1a1a1a" },
    },
    xaxis: {
      // 2. FIX: Changed from string "Timeline" to object { text: "Timeline" }
      title: { text: "Timeline" },
      type: "date",
      tickformat: "%b %Y",
      gridcolor: "#e5e7eb",
    },
    yaxis: {
      automargin: true,
      gridcolor: "#e5e7eb",
    },
    height: 700,
    paper_bgcolor: "rgba(0,0,0,0)",
    plot_bgcolor: "rgba(0,0,0,0)",
    margin: { l: 300, r: 50, t: 100, b: 80 },
    showlegend: false,
    hovermode: "closest",
  };

  const config: Partial<PlotParams["config"]> = {
    displayModeBar: true,
    displaylogo: false,
    responsive: true,
    modeBarButtonsToRemove: ["lasso2d", "select2d", "zoomIn2d", "zoomOut2d"] as const,
    toImageButtonOptions: {
      format: "png" as const,
      filename: "Project_Gantt_Chart",
      height: 800,
      width: 1400,
      scale: 2,
    },
  };

  const handleExportPDF = async () => {
    if (!plotRef.current) return;

    try {
      const plotlyDiv = plotRef.current as unknown as PlotlyCustomRef;
      
      const url: string = await plotlyDiv.plotly.toImage({
        format: "pdf", 
        height: 1080, 
        width: 1920, 
        scale: 2 
      });

      const a = document.createElement("a");
      a.href = url;
      a.download = "Project_Gantt_Chart.pdf";
      a.click();
    } catch (err) {
      console.error("PDF export failed:", err);
    }
  };

  const handleExportCSV = () => {
    let csv = "Task,Start,Finish,Duration (days),Critical\n";
    tasks.forEach(t => {
      const start = new Date(t.Start);
      const finish = new Date(t.Finish);
      const duration = Math.round((finish.getTime() - start.getTime()) / (1000 * 60 * 60 * 24)) + 1;
      csv += `"${t.Task}","${t.Start}","${t.Finish}",${duration},${t.Critical ? "Yes" : "No"}\n`;
    });

    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "Project_Schedule.csv";
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="dashboard-schedule-pro">
      <div className="dashboard-schedule-pro__header">
        <h1>Project Scheduling</h1>
        <p>Interactive 18-month construction schedule auto-generated from IFC elements and 4D logic</p>
        <div className="schedule-summary">
          <div className="summary-item"><span>Start Date</span><strong>January 1, 2026</strong></div>
          <div className="summary-item"><span>Planned Finish</span><strong>June 30, 2027</strong></div>
          <div className="summary-item"><span>Total Duration</span><strong>546 days</strong></div>
          <div className="summary-item critical"><span>Critical Path</span><strong>482 days</strong></div>
        </div>
      </div>

      <div className="gantt-container">
        <Plot
          ref={plotRef}
          data={data}
          layout={layout}
          config={config}
          style={{ width: "100%", height: "100%" }}
        />
      </div>

      <div className="gantt-actions-pro">
        <button onClick={handleExportPDF} className="btn primary">
          Export as PDF
        </button>
        <button onClick={handleExportCSV} className="btn secondary">
          Export CSV
        </button>
        <button className="btn outline">
          Link to Primavera P6
        </button>
      </div>

      <div className="legend">
        <span><i style={{background:"#ef4444"}}></i> Critical Path</span>
        <span><i style={{background:"#10b981"}}></i> Foundation</span>
        <span><i style={{background:"#3b82f6"}}></i> Structure</span>
        <span><i style={{background:"#8b5cf6"}}></i> MEP</span>
        <span><i style={{background:"#f59e0b"}}></i> Finishes</span>
      </div>
    </div>
  );
};

export default ProjectSchedulingPage;