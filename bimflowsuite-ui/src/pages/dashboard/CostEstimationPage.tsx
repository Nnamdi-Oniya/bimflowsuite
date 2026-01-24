import React, { useRef } from "react";
import Plot from "react-plotly.js";
import type { PlotParams } from "react-plotly.js";
import { Download, FileSpreadsheet, TrendingUp, DollarSign } from "lucide-react";
import "../../assets/CostEstimationPage.css";

// Define a custom interface for the internal Plotly instance method we need
interface PlotlyCustomRef {
  plotly: {
    toImage: (options: { format: string; height: number; width: number }) => Promise<string>;
  };
}

// Proper ref type for react-plotly.js
type PlotlyRef = React.ElementRef<typeof Plot>;

const CostEstimationPage: React.FC = () => {
  const plotRef = useRef<PlotlyRef>(null);

  const totalCost = 4827450;
  const baselineCost = 4715000;
  const variance = ((totalCost - baselineCost) / baselineCost * 100).toFixed(2);

  const breakdown = [
    { category: "Concrete & Rebar", amount: 1840000, percentage: 38, color: "#f8780f" },
    { category: "MEP Systems", amount: 1210000, percentage: 25, color: "#3b82f6" },
    { category: "Finishes & Facade", amount: 980000, percentage: 20, color: "#8b5cf6" },
    { category: "Structural Steel", amount: 620000, percentage: 13, color: "#10b981" },
    { category: "Contingency & Overhead", amount: 197450, percentage: 4, color: "#f59e0b" },
  ];

  // Fully typed Plotly data
  const donutData: PlotParams["data"] = [
    {
      values: breakdown.map(i => i.amount),
      labels: breakdown.map(i => i.category),
      hole: 0.5,
      type: "pie",
      marker: { colors: breakdown.map(i => i.color) },
      textinfo: "label+percent",
      textposition: "outside",
      automargin: true,
      hovertemplate: "<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>",
    },
  ];

  const barData: PlotParams["data"] = [
    {
      x: breakdown.map(i => i.category),
      y: breakdown.map(i => i.amount),
      type: "bar",
      marker: { color: breakdown.map(i => i.color) },
      text: breakdown.map(i => `$${i.amount.toLocaleString()}`),
      textposition: "outside",
      hovertemplate: "<b>%{x}</b><br>$%{y:,.0f}<extra></extra>",
    },
  ];

  const layout: Partial<PlotParams["layout"]> = {
    title: { text: "<b>Cost Distribution Breakdown</b>", font: { size: 20, family: "Inter, sans-serif" } },
    paper_bgcolor: "rgba(0,0,0,0)",
    plot_bgcolor: "rgba(0,0,0,0)",
    margin: { t: 60, b: 40, l: 40, r: 40 },
    legend: { orientation: "h" as const, y: -0.15 },
    height: 400,
    font: { family: "Inter, sans-serif" },
  };

  const config: Partial<PlotParams["config"]> = {
    displayModeBar: true,
    displaylogo: false,
    modeBarButtonsToRemove: ["lasso2d", "select2d"] as const,
    toImageButtonOptions: {
      format: "png" as const,
      filename: "BIM_Cost_Estimation",
      scale: 2,
    },
  };

  const handleExportPDF = async () => {
    if (!plotRef.current) return;

    try {
      // Cast to unknown first, then to our custom interface
      const plotlyDiv = plotRef.current as unknown as PlotlyCustomRef;
      
      const url: string = await plotlyDiv.plotly.toImage({
        format: "pdf",
        height: 800,
        width: 1200,
      });

      const a = document.createElement("a");
      a.href = url;
      a.download = "Cost_Estimation_Report.pdf";
      a.click();
    } catch (err) {
      console.error("PDF export failed:", err);
    }
  };

  const handleExportExcel = () => {
    const csv = [
      ["Category", "Amount", "Percentage"],
      ...breakdown.map(i => [i.category, i.amount, `${i.percentage}%`]),
      ["", "", ""],
      ["Total Estimated Cost", totalCost, "100%"],
      ["Baseline Cost", baselineCost, ""],
      ["Variance", `$${Math.abs(totalCost - baselineCost).toLocaleString()} (${variance}%)`, ""],
    ].map(row => row.join(",")).join("\n");

    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "Cost_Estimation.csv";
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="cost-estimation-pro">
      <div className="cost-header-pro">
        <div className="header-content">
          <h1>Cost Estimation</h1>
          <p>5D BIM Cost Analysis • Auto-generated from IFC model quantities • Updated 2 hours ago</p>
        </div>
        <div className="status-badge">
          <TrendingUp size={20} />
          <span>Live Cost Tracking</span>
        </div>
      </div>

      <div className="cost-summary-grid">
        <div className="summary-card total">
          <div className="card-icon">
            <DollarSign size={32} />
          </div>
          <div className="card-content">
            <span>Total Project Cost</span>
            <strong>${totalCost.toLocaleString()}</strong>
            <small className={Number(variance) > 0 ? "up" : "down"}>
              {Number(variance) > 0 ? "↑" : "↓"} {Math.abs(Number(variance))}% vs baseline
            </small>
          </div>
        </div>
        <div className="summary-card">
          <span>Cost per m²</span>
          <strong>$2,847</strong>
        </div>
        <div className="summary-card">
          <span>Contingency</span>
          <strong>4.0%</strong>
        </div>
        <div className="summary-card">
          <span>Confidence Level</span>
          <strong>92%</strong>
        </div>
      </div>

      <div className="cost-charts-grid">
        <div className="chart-card donut">
          <Plot
            ref={plotRef}
            data={donutData}
            layout={layout}
            config={config}
            style={{ width: "100%", height: "100%" }}
          />
        </div>

        <div className="chart-card bar">
          <Plot
            data={barData}
            layout={{
              ...layout,
              title: { text: "<b>Detailed Cost Breakdown</b>", font: { size: 20, family: "Inter, sans-serif" } },
              xaxis: { tickangle: -45 },
            }}
            config={config}
            style={{ width: "100%", height: "500px" }}
          />
        </div>
      </div>

      <div className="detailed-breakdown">
        <h3>Detailed Breakdown</h3>
        {breakdown.map((item) => (
          <div key={item.category} className="breakdown-row">
            <div className="row-label">
              <span>{item.category}</span>
              <strong>${item.amount.toLocaleString()}</strong>
            </div>
            <div className="progress-container">
              <div
                className="progress-bar"
                style={{ width: `${item.percentage}%`, backgroundColor: item.color }}
              />
            </div>
            <span className="percentage">{item.percentage}%</span>
          </div>
        ))}
      </div>

      <div className="cost-actions-pro">
        <button onClick={handleExportPDF} className="btn primary">
          <Download size={18} />
          Export PDF Report
        </button>
        <button onClick={handleExportExcel} className="btn success">
          <FileSpreadsheet size={18} />
          Export Excel
        </button>
        <button className="btn outline">
          <TrendingUp size={18} />
          View Historical Trends
        </button>
      </div>

      <div className="cost-legend">
        <span><i style={{ background: "#f8780f" }}></i> Concrete & Formwork</span>
        <span><i style={{ background: "#3b82f6" }}></i> MEP Systems</span>
        <span><i style={{ background: "#8b5cf6" }}></i> Architectural Finishes</span>
        <span><i style={{ background: "#10b981" }}></i> Structural Steel</span>
        <span><i style={{ background: "#f59e0b" }}></i> Contingency</span>
      </div>
    </div>
  );
};

export default CostEstimationPage;