// src/pages/SenderPage.tsx
import React, { useState } from "react";
import axios from "axios";

const SenderPage: React.FC = () => {
  const [inputData, setInputData] = useState("");
  const [status, setStatus] = useState("");

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://127.0.0.1:5000/save-input", {
        inputData,
      });
      setStatus(response.data.message);
    } catch (err) {
      console.error(err);
      setStatus("Error sending data");
    }
  };

  return (
    <div className="p-8 text-white">
      <h2 className="text-3xl font-bold mb-4">🔐 Sender Page</h2>
      <form onSubmit={handleSend} className="space-y-4 w-full max-w-md">
        <input
          type="text"
          placeholder="Enter secret data..."
          className="w-full p-2 rounded text-black"
          value={inputData}
          onChange={(e) => setInputData(e.target.value)}
        />
        <button
          type="submit"
          className="bg-blue-600 hover:bg-blue-800 px-4 py-2 rounded"
          disabled={!inputData}
        >
          Encrypt & Send
        </button>
      </form>

      {inputData && (
        <div className="mt-8 bg-gray-900 p-4 rounded shadow">
          <h3 className="font-semibold text-lg mb-2">🔍 Data Preview</h3>
          <p className="text-green-300 break-words">{inputData}</p>
        </div>
      )}

      {status && <p className="mt-4 text-blue-400">{status}</p>}
    </div>
  );
};

export default SenderPage;
