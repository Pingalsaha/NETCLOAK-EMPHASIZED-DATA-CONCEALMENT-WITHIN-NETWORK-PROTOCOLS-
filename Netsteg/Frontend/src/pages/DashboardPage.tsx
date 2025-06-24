/* eslint-disable @typescript-eslint/no-explicit-any */
// src/pages/DashboardPage.tsx
import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  Chart as ChartJS,
  BarElement,
  ArcElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
  Title,
} from "chart.js";
import { Bar, Pie } from "react-chartjs-2";

ChartJS.register(
  BarElement,
  ArcElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
  Title
);

interface HistoryEntry {
  input: string;
  encrypted: string;
  decrypted: string;
  protocol: string;
  timestamp: string;
}

const DashboardPage: React.FC = () => {
  const [history, setHistory] = useState<HistoryEntry[]>([]);
  const [logs, setLogs] = useState<string[]>([]);
  const [rawData, setRawData] = useState<string[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const historyRes = await axios.get("http://127.0.0.1:5000/history");
        const logsRes = await axios.get("http://127.0.0.1:5000/logs");
        const rawRes = await axios.get("http://127.0.0.1:5000/rawData");

        setHistory(historyRes.data.history || []);
        setLogs((logsRes.data.logs || []).reverse());
        setRawData(rawRes.data.rawData || []);
      } catch (err) {
        setError("Error fetching dashboard data.");
        console.error(err);
      }
    };

    fetchData();
  }, []);

  const filteredHistory = history.filter(
    (entry) =>
      entry.input.toLowerCase().includes(searchTerm.toLowerCase()) ||
      entry.protocol.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const protocolCount: Record<string, number> = {
    TCP: 0,
    HTTP: 0,
    DNS: 0,
    Other: 0,
  };

  history.forEach((item) => {
    const proto = item.protocol.toUpperCase();
    if (["TCP", "HTTP", "DNS"].includes(proto)) {
      protocolCount[proto]++;
    } else {
      protocolCount["Other"]++;
    }
  });

  const chartLabels = Object.keys(protocolCount);
  const chartValues = chartLabels.map((label) => protocolCount[label]);

  const barChartData = {
    labels: chartLabels,
    datasets: [
      {
        label: "Count",
        backgroundColor: ["#60a5fa", "#34d399", "#fbbf24", "#f472b6"],
        data: chartValues,
      },
    ],
  };

  const barChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      title: {
        display: true,
        text: "Protocol Usage (Bar Chart)",
        font: { size: 16 },
      },
      legend: { display: false },
      tooltip: {
        callbacks: {
          label: (context: any) => `Usage: ${context.parsed.y}`,
        },
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: "Protocol",
          color: "#ffffff",
        },
        ticks: { color: "#ffffff" },
      },
      y: {
        title: {
          display: true,
          text: "Usage Count",
          color: "#ffffff",
        },
        ticks: { color: "#ffffff", precision: 0 },
      },
    },
  };

  const pieChartData = {
    labels: chartLabels,
    datasets: [
      {
        label: "Protocol Share",
        data: chartValues,
        backgroundColor: ["#60a5fa", "#34d399", "#fbbf24", "#f472b6"],
        borderColor: "#1f2937",
        borderWidth: 2,
      },
    ],
  };

  const pieChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      title: {
        display: true,
        text: "Protocol Distribution (Pie Chart)",
        font: { size: 16 },
        color: "#ffffff",
      },
      legend: {
        position: "bottom" as const,
        labels: {
          color: "#ffffff",
          font: { size: 12 },
        },
      },
      tooltip: {
        callbacks: {
          label: function (context: any) {
            return `${context.label}: ${context.parsed}`;
          },
        },
      },
    },
  };

  return (
    <div className="p-8 text-white">
      <h2 className="text-3xl font-bold mb-6">📊 Dashboard</h2>

      {error && <p className="text-red-500">{error}</p>}

      <div className="mb-6">
        <input
          type="text"
          placeholder="Search by input or protocol..."
          className="w-full max-w-xl p-2 rounded text-black"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      {/* History Table */}
      <div className="mb-12">
        <h3 className="text-xl font-semibold text-blue-400 mb-4">
          🗂️ Encrypted History
        </h3>
        <div className="overflow-auto max-h-[30rem] bg-gray-800 rounded shadow p-4">
          <table className="table-auto w-full text-sm">
            <thead>
              <tr className="text-left border-b border-gray-600">
                <th className="p-2">Input</th>
                <th className="p-2">Encrypted</th>
                <th className="p-2">Protocol</th>
                <th className="p-2">Timestamp</th>
              </tr>
            </thead>
            <tbody>
              {filteredHistory.map((item, idx) => (
                <tr key={idx} className="border-b border-gray-700">
                  <td className="p-2 break-words">{item.input}</td>
                  <td className="p-2 break-words text-yellow-300">
                    {item.encrypted}
                  </td>
                  <td className="p-2">{item.protocol}</td>
                  <td className="p-2 text-xs text-gray-400">
                    {new Date(item.timestamp).toLocaleString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
        <div className="bg-gray-800 p-4 rounded shadow h-[300px]">
          <Bar data={barChartData} options={barChartOptions} />
        </div>
        <div className="bg-gray-800 p-4 rounded shadow h-[300px]">
          <Pie data={pieChartData} options={pieChartOptions} />
        </div>
      </div>

      {/* Logs and Raw Data */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-gray-800 p-4 rounded shadow max-h-[20rem] overflow-auto">
          <h3 className="text-xl font-semibold mb-2 text-yellow-300">
            📋 Recent Logs
          </h3>
          {logs.map((log, idx) => (
            <p key={idx} className="text-sm text-gray-200">
              {log}
            </p>
          ))}
        </div>

        <div className="bg-gray-800 p-4 rounded shadow max-h-[20rem] overflow-auto">
          <h3 className="text-xl font-semibold mb-2 text-purple-300">
            📡 Raw Captured Data
          </h3>
          {rawData.map((data, idx) => (
            <p key={idx} className="text-sm text-gray-200">
              {data}
            </p>
          ))}
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
