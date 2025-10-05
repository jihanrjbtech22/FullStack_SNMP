import React, { useEffect, useRef, useState } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  TimeScale,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import 'chartjs-adapter-date-fns';
import './Charts.css';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  TimeScale
);

/**
 * Charts Component
 * Displays time-series charts for engine parameters
 */
const Charts = ({ enginesData, selectedParameter, timeRange = 60 }) => {
  const [chartData, setChartData] = useState({});
  const [isVisible, setIsVisible] = useState(false);
  const chartRef = useRef(null);

  // Get Y-axis label based on parameter
  const getYAxisLabel = (parameter) => {
    const labels = {
      temperature: 'Temperature (°C)',
      rpm: 'RPM',
      current: 'Current (A)',
      power: 'Power (W)',
    };
    return labels[parameter] || parameter;
  };

  // Chart configuration
  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
      intersect: false,
      mode: 'index',
    },
    plugins: {
      legend: {
        position: 'top',
        labels: {
          usePointStyle: true,
          padding: 20,
        },
      },
      tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleColor: 'white',
        bodyColor: 'white',
        borderColor: 'rgba(255, 255, 255, 0.2)',
        borderWidth: 1,
        cornerRadius: 8,
        displayColors: true,
      },
    },
    scales: {
      x: {
        type: 'time',
        time: {
          displayFormats: {
            minute: 'HH:mm',
            second: 'HH:mm:ss',
          },
        },
        title: {
          display: true,
          text: 'Time',
          color: '#666',
          font: {
            size: 12,
            weight: 'bold',
          },
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.1)',
        },
      },
      y: {
        title: {
          display: true,
          text: getYAxisLabel(selectedParameter),
          color: '#666',
          font: {
            size: 12,
            weight: 'bold',
          },
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.1)',
        },
      },
    },
    elements: {
      point: {
        radius: 3,
        hoverRadius: 6,
      },
      line: {
        tension: 0.1,
        borderWidth: 2,
      },
    },
  };

  // Generate chart data from engines data
  useEffect(() => {
    if (!enginesData || !enginesData.data) return;

    const now = new Date();
    const timeRangeMs = timeRange * 1000; // Convert to milliseconds
    const cutoffTime = new Date(now.getTime() - timeRangeMs);

    const datasets = Object.entries(enginesData.data).map(([engineId, engine], index) => {
      const color = getEngineColor(index);
      
      return {
        label: engineId,
        data: generateTimeSeriesData(engine, selectedParameter, cutoffTime),
        borderColor: color,
        backgroundColor: color + '20', // Add transparency
        fill: false,
        tension: 0.1,
      };
    });

    setChartData({
      datasets,
    });
  }, [enginesData, selectedParameter, timeRange]);

  // Generate time series data for a specific parameter
  const generateTimeSeriesData = (engine, parameter, cutoffTime) => {
    const data = [];
    const now = new Date();
    
    // Generate sample data points for the time range
    const points = 20; // Number of data points to show
    const interval = (now.getTime() - cutoffTime.getTime()) / points;
    
    for (let i = 0; i < points; i++) {
      const timestamp = new Date(cutoffTime.getTime() + (i * interval));
      const value = getParameterValue(engine, parameter, i);
      
      data.push({
        x: timestamp,
        y: value,
      });
    }
    
    return data;
  };

  // Get parameter value with some variation for visualization
  const getParameterValue = (engine, parameter, index) => {
    const baseValue = engine[parameter] || 0;
    const variation = Math.sin(index * 0.5) * (baseValue * 0.1); // 10% variation
    return baseValue + variation;
  };

  // Get engine color based on index
  const getEngineColor = (index) => {
    const colors = [
      '#3b82f6', // Blue
      '#ef4444', // Red
      '#10b981', // Green
      '#f59e0b', // Yellow
      '#8b5cf6', // Purple
      '#06b6d4', // Cyan
    ];
    return colors[index % colors.length];
  };

  // Get chart title based on parameter
  const getChartTitle = (parameter) => {
    const titles = {
      temperature: 'Engine Temperature Trends',
      rpm: 'Engine RPM Trends',
      current: 'Engine Current Trends',
      power: 'Engine Power Output Trends',
    };
    return titles[parameter] || `${parameter} Trends`;
  };

  return (
    <div className="charts-container">
      <div className="chart-header">
        <h3>{getChartTitle(selectedParameter)}</h3>
        <div className="chart-controls">
          <select
            value={timeRange}
            onChange={(e) => setTimeRange(parseInt(e.target.value))}
            className="time-range-select"
          >
            <option value={30}>Last 30 seconds</option>
            <option value={60}>Last 1 minute</option>
            <option value={300}>Last 5 minutes</option>
            <option value={600}>Last 10 minutes</option>
          </select>
        </div>
      </div>
      
      <div className="chart-wrapper">
        {chartData.datasets && chartData.datasets.length > 0 ? (
          <Line
            ref={chartRef}
            data={chartData}
            options={chartOptions}
            onElementsClick={() => setIsVisible(!isVisible)}
          />
        ) : (
          <div className="chart-placeholder">
            <div className="placeholder-icon">📊</div>
            <p>No data available for {selectedParameter}</p>
            <small>Waiting for engine data...</small>
          </div>
        )}
      </div>
      
      <div className="chart-footer">
        <div className="chart-info">
          <span className="info-item">
            <span className="info-label">Engines:</span>
            <span className="info-value">
              {chartData.datasets ? chartData.datasets.length : 0}
            </span>
          </span>
          <span className="info-item">
            <span className="info-label">Time Range:</span>
            <span className="info-value">{timeRange}s</span>
          </span>
          <span className="info-item">
            <span className="info-label">Last Update:</span>
            <span className="info-value">
              {enginesData?.timestamp ? 
                new Date(enginesData.timestamp * 1000).toLocaleTimeString() : 
                'Never'
              }
            </span>
          </span>
        </div>
      </div>
    </div>
  );
};

export default Charts;
