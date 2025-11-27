import React, { useEffect, useState } from 'react';
import { getOptimalStrategy } from './services/api';
import StrategyChart from './components/StrategyChart';
import RaceEngineerBot from './components/RaceEngineerBot'; // Import the Bot
import './App.css';

function App() {
  const [strategy, setStrategy] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      const data = await getOptimalStrategy();
      setStrategy(data);
      setLoading(false);
    };

    fetchData();
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>🏎️ F1 Virtual Pit Wall</h1>
        <p>Real-Time Strategy Optimizer</p>
      </header>

      <main className="dashboard">
        {loading ? (
          <h2>Calculating Optimal Strategy...</h2>
        ) : (
          <div className="content-grid"> 
            {/* Left Column: Strategy Data */}
            <div className="strategy-card">
              {strategy && strategy.recommended ? (
                  <>
                      <div className="recommendation-box">
                          <h2>🚀 Recommended: {strategy.recommended.name}</h2>
                          <p className="time-display">
                              Total Time: <strong>{strategy.recommended.total_time}s</strong>
                          </p>
                          <div className="stint-list">
                              {strategy.recommended.details.map((stint, index) => (
                                  <span key={index} className="stint-badge">
                                      {stint}
                                  </span>
                              ))}
                          </div>
                      </div>
                      
                      <div className="chart-section">
                          <StrategyChart strategyData={strategy} />
                      </div>
                  </>
              ) : (
                  <p>No strategy data available.</p>
              )}
            </div>

            {/* Right Column: AI Bot */}
            {strategy && <RaceEngineerBot strategyData={strategy} />}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;