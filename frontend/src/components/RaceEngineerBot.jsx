import React, { useState } from 'react';
import axios from 'axios';

const RaceEngineerBot = ({ strategyData }) => {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  const askEngineer = async () => {
    if (!question) return;
    setLoading(true);
    setResponse(""); // Clear previous response

    try {
      const res = await axios.post('http://127.0.0.1:8000/strategy/chat', {
        question: question,
        strategy_data: strategyData
      });
      setResponse(res.data.reply);
    } catch (error) {
      setResponse("Radio failure. Can you repeat?");
      console.error(error);
    }
    setLoading(false);
  };

  return (
    <div className="engineer-bot-card">
      <div className="bot-header">
        <h3>🎧 AI Race Engineer</h3>
        <span className="status-dot">LIVE</span>
      </div>
      
      <div className="chat-display">
        {response ? (
            <p className="bot-msg">" {response} "</p>
        ) : (
            <p className="placeholder-text">Ask about the strategy...</p>
        )}
      </div>

      <div className="input-area">
        <input 
            type="text" 
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="e.g., Why not 2-stop?"
            onKeyPress={(e) => e.key === 'Enter' && askEngineer()}
        />
        <button onClick={askEngineer} disabled={loading}>
            {loading ? '...' : 'Talk'}
        </button>
      </div>
    </div>
  );
};

export default RaceEngineerBot;