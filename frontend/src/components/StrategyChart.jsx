import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const StrategyChart = ({ strategyData }) => {
  if (!strategyData) return <p className="text-center">Loading Strategy Data...</p>;

  // Prepare data for the chart
  // We want to plot lap numbers (x) vs predicted race time (y) is tricky for pure degradation.
  // Instead, let's visualize the "Stint Plan" as a stepped line or just text for MVP.
  // For a visual graph, we usually plot "Lap Time per Lap".
  
  // Since our MVP backend returns total time, let's make a simplified visual:
  // Comparing Total Race Time of options.
  
  const labels = strategyData.alternatives.map(s => s.name);
  const times = strategyData.alternatives.map(s => s.total_time);

  const data = {
    labels,
    datasets: [
      {
        label: 'Total Race Time (seconds)',
        data: times,
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
        borderWidth: 2,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { position: 'top' },
      title: { display: true, text: 'Strategy Comparison: Lower is Better' },
    },
    scales: {
        y: {
            min: Math.min(...times) - 10, // Zoom in on the difference
        }
    }
  };

  return (
    <div style={{ maxWidth: '600px', margin: '0 auto' }}>
      <Line options={options} data={data} />
    </div>
  );
};

export default StrategyChart;