import React from "react";
import "../../assets/AnalyticsPage.css";

// --- TypeScript Fix: Define a flexible style interface for CSS Custom Properties ---
/**
 * Extends React.CSSProperties to allow for custom CSS variables (e.g., '--segment-size').
 * This resolves the TypeScript error TS(2353) and TS(2747) for the Pie Chart.
 */
interface CustomCSSProperties extends React.CSSProperties {
  [key: `--${string}`]: string | number;
}
// -----------------------------------------------------------------------------------

const AnalyticsPage: React.FC = () => {
  // Define data inline for the charts
  const pieChartData = {
    onTime: 95,
    delayed: 5,
  };
  
  // Define data inline for the Doughnut chart (Sum: 40 + 30 + 15 + 15 = 100)
  const doughnutChartData = [
    { name: "Steel", percent: 40, color: "#f8780f" }, // Orange
    { name: "Concrete", percent: 30, color: "#3b82f6" }, // Blue
    { name: "Glass", percent: 15, color: "#10b981" }, // Green
    { name: "Other", percent: 15, color: "#ef4444" }, // Red
  ];

  // --- Doughnut Chart Dynamic Calculation ---
  const radius = 45;
  const circumference = 2 * Math.PI * radius; // Approx 282.74
  let offset = 0; // Tracks the accumulated length for the strokeDashoffset

  const doughnutCircles = doughnutChartData.map((item, index) => {
    // 1. Calculate the length of the segment's stroke
    const dashLength = (item.percent / 100) * circumference;
    
    // 2. Set the current offset for this segment (where it starts)
    const strokeDashoffset = index === 0 ? 0 : circumference - offset;

    // 3. Update the running total for the next segment's calculation
    offset += dashLength;
    
    // 4. Determine the strokeDasharray: segment length, then remaining circumference
    const strokeDasharray = `${dashLength} ${circumference - dashLength}`;

    return (
      <circle
        key={index}
        cx="60"
        cy="60"
        r={radius}
        fill="none"
        stroke={item.color}
        strokeWidth="12"
        strokeDasharray={strokeDasharray}
        strokeDashoffset={strokeDashoffset}
        // Rotation is crucial to make the segments stack correctly from the top (12 o'clock)
        style={{ transform: 'rotate(-90deg)', transformOrigin: '60px 60px' }}
      />
    );
  });
  // --------------------------------------------

  return (
    <div className="analytics-page">
      <h1 className="page-title">BIM Analytics Dashboard</h1>
      <div className="analytics-grid">
        
        {/* Cost Estimation Trends - CSS Line Chart */}
        <div className="chart-card">
          <h2>Cost Estimation Trends</h2>
          <div className="chart-container line-chart">
            <div className="chart-line-svg">
              <svg viewBox="0 0 300 150" preserveAspectRatio="none">
                <polyline
                  points="20,130 60,100 100,120 140,80 180,90 220,60 260,70 300,50"
                  fill="none"
                  stroke="#f8780f"
                  strokeWidth="3"
                  strokeLinecap="round"
                />
                <circle cx="20" cy="130" r="4" fill="#f8780f" />
                <circle cx="60" cy="100" r="4" fill="#f8780f" />
                <circle cx="100" cy="120" r="4" fill="#f8780f" />
                <circle cx="140" cy="80" r="4" fill="#f8780f" />
                <circle cx="180" cy="90" r="4" fill="#f8780f" />
                <circle cx="220" cy="60" r="4" fill="#f8780f" />
                <circle cx="260" cy="70" r="4" fill="#f8780f" />
                <circle cx="300" cy="50" r="4" fill="#f8780f" />
              </svg>
            </div>
            <div className="chart-labels">
              <span>Jan</span>
              <span>Feb</span>
              <span>Mar</span>
              <span>Apr</span>
              <span>May</span>
              <span>Jun</span>
            </div>
          </div>
          <p className="chart-caption">Average savings: 12% YTD across projects</p>
        </div>

        {/* Compliance Metrics - CSS Bar Chart */}
        <div className="chart-card">
          <h2>Compliance Metrics</h2>
          <div className="chart-container bar-chart">
            <div className="bar-group">
              <div className="bar-label">Office Tower</div>
              <div className="bar-container">
                <div className="bar" style={{ height: '95%', background: '#10b981' }}></div>
              </div>
            </div>
            <div className="bar-group">
              <div className="bar-label">Bridge Exp.</div>
              <div className="bar-container">
                <div className="bar" style={{ height: '87%', background: '#3b82f6' }}></div>
              </div>
            </div>
            <div className="bar-group">
              <div className="bar-label">Road Corr.</div>
              <div className="bar-container">
                <div className="bar" style={{ height: '100%', background: '#f8780f' }}></div>
              </div>
            </div>
            <div className="bar-group">
              <div className="bar-label">Res. High-Rise</div>
              <div className="bar-container">
                <div className="bar" style={{ height: '92%', background: '#ef4444' }}></div>
              </div>
            </div>
          </div>
          <p className="chart-caption">96% average IFC compliance across active projects</p>
        </div>

        {/* Schedule Performance - CSS Pie Chart */}
        <div className="chart-card">
          <h2>Schedule Performance</h2>
          <div className="chart-container pie-chart">
            <div className="pie-wrapper">
              <div 
                className="pie-segment on-time" 
                // Using CustomCSSProperties type definition here
                style={{ '--segment-size': `${pieChartData.onTime}%` } as CustomCSSProperties} 
              ></div>
              <div 
                className="pie-segment delayed" 
                // Using CustomCSSProperties type definition here
                style={{ '--segment-size': `${pieChartData.delayed}%` } as CustomCSSProperties}
              ></div>
            </div>
            <div className="pie-legend">
              <div className="legend-item">
                <span className="legend-color on-time"></span>
                <span>On Time: {pieChartData.onTime}%</span>
              </div>
              <div className="legend-item">
                <span className="legend-color delayed"></span>
                <span>Delayed: {pieChartData.delayed}%</span>
              </div>
            </div>
          </div>
          <p className="chart-caption">{pieChartData.onTime}% of milestones on schedule; {pieChartData.delayed}% delayed</p>
        </div>

        {/* Material Usage - Enhanced CSS Doughnut Chart */}
        <div className="chart-card">
          <h2>Material Usage Breakdown</h2>
          <div className="chart-container doughnut-chart">
            <div className="doughnut-wrapper">
              <svg viewBox="0 0 120 120" className="doughnut-svg">
                {/* Background circle */}
                <circle cx="60" cy="60" r={radius} fill="none" stroke="#e5e7eb" strokeWidth="12" />
                {/* Dynamically generated segment circles (now using the calculated offset) */}
                {doughnutCircles}
              </svg>
              <div className="doughnut-center">
                <span className="center-value">100%</span>
                <span className="center-text">Total</span>
              </div>
            </div>
            <div className="doughnut-legend">
              {doughnutChartData.map((item, index) => (
                <div key={index} className="legend-item">
                  <span className="legend-color" style={{ backgroundColor: item.color }}></span>
                  <span>{item.name}: {item.percent}%</span>
                </div>
              ))}
            </div>
          </div>
          <p className="chart-caption">Distribution of materials in current portfolio</p>
        </div>

        {/* Project Timeline - CSS Area Chart */}
        <div className="chart-card">
          <h2>Project Activity Timeline</h2>
          <div className="chart-container area-chart">
            <svg viewBox="0 0 300 150" preserveAspectRatio="none">
              <path d="M20 130 L60 100 L100 80 L140 60 L180 70 L220 50 L260 40 L300 30 L300 150 L20 150 Z" fill="#fff5eb" stroke="#f8780f" strokeWidth="2" />
              <polyline points="20,130 60,100 100,80 140,60 180,70 220,50 260,40 300,30" fill="none" stroke="#f8780f" strokeWidth="2" strokeLinecap="round" />
              <circle cx="20" cy="130" r="3" fill="#f8780f" />
              <circle cx="60" cy="100" r="3" fill="#f8780f" />
              <circle cx="100" cy="80" r="3" fill="#f8780f" />
              <circle cx="140" cy="60" r="3" fill="#f8780f" />
              <circle cx="180" cy="70" r="3" fill="#f8780f" />
              <circle cx="220" cy="50" r="3" fill="#f8780f" />
              <circle cx="260" cy="40" r="3" fill="#f8780f" />
              <circle cx="300" cy="30" r="3" fill="#f8780f" />
            </svg>
            <div className="chart-labels">
              <span>Jan</span>
              <span>Feb</span>
              <span>Mar</span>
              <span>Apr</span>
              <span>May</span>
              <span>Jun</span>
            </div>
          </div>
          <p className="chart-caption">Active projects per month; peak in Q2</p>
        </div>

        {/* Risk Assessment - CSS Radar Chart */}
        <div className="chart-card">
          <h2>Risk Assessment Radar</h2>
          <div className="chart-container radar-chart">
            <svg viewBox="0 0 200 200" className="radar-svg">
              <defs>
                <polygon id="radar-polygon" points="100,10 130,50 170,50 140,80 150,120 100,130 50,120 50,80 30,50 70,50" fill="none" stroke="#e5e7eb" strokeWidth="1" />
              </defs>
              <use href="#radar-polygon" />
              <polygon points="100,30 120,50 140,50 125,65 130,85 100,90 70,85 75,65 60,50 80,50" fill="#fff5eb" stroke="#f8780f" strokeWidth="2" opacity="0.6" />
              <polygon points="100,20 115,40 130,40 115,50 120,70 100,75 80,70 85,50 70,40 85,40" fill="#ecfdf5" stroke="#10b981" strokeWidth="2" opacity="0.6" />
              <circle cx="100" cy="100" r="5" fill="#f8780f" />
              <circle cx="120" cy="50" r="3" fill="#f8780f" />
              <circle cx="140" cy="50" r="3" fill="#f8780f" />
              <circle cx="125" cy="65" r="3" fill="#f8780f" />
              <circle cx="130" cy="85" r="3" fill="#f8780f" />
              <circle cx="100" cy="90" r="3" fill="#f8780f" />
              <circle cx="70" cy="85" r="3" fill="#f8780f" />
              <circle cx="75" cy="65" r="3" fill="#f8780f" />
              <circle cx="60" cy="50" r="3" fill="#f8780f" />
              <circle cx="80" cy="50" r="3" fill="#f8780f" />
              <text x="100" y="180" textAnchor="middle" fill="#6b7280" fontSize="10">Cost | Schedule | Compliance | Material | Safety</text>
            </svg>
          </div>
          <p className="chart-caption">Risk scores: Current vs. Target benchmarks</p>
        </div>

        {/* Full-span Integrated Dashboard */}
        <div className="chart-card full-span">
          <h2>Integrated BIM Dashboard</h2>
          <div className="integrated-dashboard">
            <div className="dashboard-kpi">
              <span className="kpi-value">12</span>
              <span className="kpi-label">Active Projects</span>
            </div>
            <div className="dashboard-kpi">
              <span className="kpi-value">96%</span>
              <span className="kpi-label">Compliance</span>
            </div>
            <div className="dashboard-kpi">
              <span className="kpi-value">$45K</span>
              <span className="kpi-label">Savings</span>
            </div>
            <div className="dashboard-kpi">
              <span className="kpi-value">28</span>
              <span className="kpi-label">Models Gen.</span>
            </div>
            <div className="alert-section">
              <h3>Alerts</h3>
              <ul>
                <li>Bridge Project: Compliance Issue</li>
                <li>Road Corridor: On Schedule</li>
                <li>Office Tower: Cost Alert</li>
              </ul>
            </div>
          </div>
          <p className="chart-caption">Holistic view: Combine all metrics for executive summary</p>
        </div>
      </div>
      <div className="analytics-actions">
        <button className="analytics-action-btn">Export Data (CSV/PDF)</button>
        <button className="analytics-action-btn secondary">Customize Views</button>
        <button className="analytics-action-btn">Generate Report</button>
      </div>
    </div>
  );
};

export default AnalyticsPage;