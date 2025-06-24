// src/App.tsx
import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import SenderPage from "./pages/SenderPage";
import ReceiverPage from "./pages/ReceiverPage";
import DashboardPage from "./pages/DashboardPage";

const App: React.FC = () => {
  return (
    <Router>
      <div className="bg-black text-white min-h-screen">
        <nav className="bg-gray-800 px-4 py-3 shadow-lg flex gap-6">
          <Link to="/" className="hover:text-blue-400">
            Sender
          </Link>
          <Link to="/receiver" className="hover:text-blue-400">
            Receiver
          </Link>
          <Link to="/dashboard" className="hover:text-blue-400">
            Dashboard
          </Link>
        </nav>

        <Routes>
          <Route path="/" element={<SenderPage />} />
          <Route path="/receiver" element={<ReceiverPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
