import React, { useState } from "react";
import { Plus, CheckCircle, Clock, DollarSign, AlertTriangle, TrendingUp, X } from "lucide-react";
import "../../assets/ScenarioManagerPage.css";

interface Scenario {
  id: string;
  name: string;
  cost: number;
  duration: number; // in months
  compliance: number;
  energyEfficiency?: number;
  isActive: boolean;
  isBaseline?: boolean;
}

const ScenarioManagerPage: React.FC = () => {
  const [scenarios, setScenarios] = useState<Scenario[]>([
    { id: "baseline", name: "Baseline Design", cost: 4827450, duration: 18, compliance: 97, isActive: false, isBaseline: true },
    { id: "opt1", name: "Optimized Design B", cost: 4523000, duration: 16, compliance: 99, energyEfficiency: 94, isActive: true },
    { id: "opt2", name: "Green Premium", cost: 4980000, duration: 17, compliance: 100, energyEfficiency: 98, isActive: false },
  ]);

  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newScenarioName, setNewScenarioName] = useState("");

  const baseline = scenarios.find(s => s.isBaseline);
  const activeScenario = scenarios.find(s => s.isActive);

  const savings = baseline && activeScenario
    ? baseline.cost - activeScenario.cost
    : 0;

  const timeSaved = baseline && activeScenario
    ? baseline.duration - activeScenario.duration
    : 0;

  const handleCreateScenario = () => {
    if (newScenarioName.trim()) {
      const newScenario: Scenario = {
        id: Date.now().toString(),
        name: newScenarioName,
        cost: 4700000 + Math.floor(Math.random() * 300000),
        duration: 16 + Math.floor(Math.random() * 3),
        compliance: 95 + Math.floor(Math.random() * 6),
        energyEfficiency: 90 + Math.floor(Math.random() * 10),
        isActive: false,
      };
      setScenarios([...scenarios, newScenario]);
      setNewScenarioName("");
      setShowCreateModal(false);
    }
  };

  const setActive = (id: string) => {
    setScenarios(scenarios.map(s => ({ ...s, isActive: s.id === id })));
  };

  return (
    <div className="scenario-manager-pro">
      <div className="scenario-header-pro">
        <div className="header-content">
          <h1>Scenario Manager</h1>
          <p>Compare design alternatives • Optimize cost, time & performance</p>
        </div>

        {activeScenario && savings > 0 && (
          <div className="global-savings">
            <TrendingUp size={28} />
            <div>
              <strong>${(savings / 1000).toFixed(0)}K saved</strong> • {timeSaved > 0 ? `${timeSaved} months faster` : "On time"}
            </div>
          </div>
        )}
      </div>

      <div className="scenario-grid-pro">
        {scenarios.map((scenario) => (
          <div
            key={scenario.id}
            className={`scenario-card-pro ${scenario.isActive ? "active" : ""} ${scenario.isBaseline ? "baseline" : ""}`}
            onClick={() => !scenario.isBaseline && setActive(scenario.id)}
          >
            <div className="card-header">
              {scenario.isActive && <CheckCircle className="active-badge" size={28} />}
              {scenario.isBaseline && <span className="baseline-tag">Baseline</span>}
              <h3>{scenario.name}</h3>
            </div>

            <div className="metrics-grid">
              <div className="metric">
                <DollarSign size={20} />
                <div>
                  <small>Cost</small>
                  <strong>${(scenario.cost / 1000000).toFixed(2)}M</strong>
                </div>
              </div>
              <div className="metric">
                <Clock size={20} />
                <div>
                  <small>Duration</small>
                  <strong>{scenario.duration} months</strong>
                </div>
              </div>
              <div className="metric">
                <AlertTriangle size={20} />
                <div>
                  <small>Compliance</small>
                  <strong>{scenario.compliance}%</strong>
                </div>
              </div>
              {scenario.energyEfficiency && (
                <div className="metric highlight">
                  <TrendingUp size={20} />
                  <div>
                    <small>Energy Score</small>
                    <strong>{scenario.energyEfficiency}%</strong>
                  </div>
                </div>
              )}
            </div>

            {scenario.isActive && savings > 0 && !scenario.isBaseline && (
              <div className="savings-banner">
                <strong>Best Value</strong> • Save ${(savings / 1000).toFixed(0)}K & {timeSaved} months
              </div>
            )}
          </div>
        ))}

        {/* Create New */}
        <div className="scenario-card-pro create-new" onClick={() => setShowCreateModal(true)}>
          <div className="create-content">
            <div className="plus-circle">
              <Plus size={48} />
            </div>
            <h3>Create New Scenario</h3>
            <p>Duplicate current model & modify parameters</p>
          </div>
        </div>
      </div>

      {/* Create Modal */}
      {showCreateModal && (
        <div className="modal-overlay" onClick={() => setShowCreateModal(false)}>
          <div className="create-modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Create New Scenario</h2>
              <button onClick={() => setShowCreateModal(false)} className="close-btn">
                <X size={24} />
              </button>
            </div>
            <input
              type="text"
              placeholder="Enter scenario name..."
              value={newScenarioName}
              onChange={(e) => setNewScenarioName(e.target.value)}
              autoFocus
            />
            <div className="modal-actions">
              <button onClick={() => setShowCreateModal(false)} className="btn secondary">Cancel</button>
              <button onClick={handleCreateScenario} className="btn primary" disabled={!newScenarioName.trim()}>
                Create Scenario
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ScenarioManagerPage;