/* eslint-disable @typescript-eslint/no-explicit-any */
// src/pages/ReceiverPage.tsx
import React, { useEffect, useState } from "react";
import axios from "axios";

const ReceiverPage: React.FC = () => {
  const [rawData, setRawData] = useState<string[]>([]);
  const [historyData, setHistoryData] = useState<any>();
  // const [decryptedData, setDecryptedData] = useState<string[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchRawData = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/rawData");
        setRawData(response.data.rawData || []);
      } catch (err) {
        setError("Failed to fetch raw data.");
        console.error(err);
      }
    };

    const fetchHist = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/history");

        const history = response.data.history || [];

        setHistoryData(history.map((item: any) => item.input));
      } catch (err) {
        setError("Failed to fetch history data.");
        console.error(err);
      }
    };

    // const fetchLogs = async () => {
    //   try {
    //     const response = await axios.get("http://127.0.0.1:5000/logs");
    //     const logs = response.data.logs || [];
    //     const decryptedLogs = logs.filter(
    //       (log: string) =>
    //         log.toLowerCase().includes("decrypted data") ||
    //         log.includes("🔓 Decrypted data added to history.") ||
    //         log.includes("Decryption completed.")
    //     );
    //     setDecryptedData(decryptedLogs);
    //   } catch (err) {
    //     setError("Failed to fetch decrypted data.");
    //     console.error(err);
    //   }
    // };

    fetchRawData();
    // fetchLogs();
    fetchHist();
  }, []);

  return (
    <div className="p-8 text-white">
      <h2 className="text-3xl font-bold mb-4">📥 Receiver Page</h2>

      {error && <p className="text-red-500">{error}</p>}

      <div className="grid grid-cols-2 gap-8">
        <div className="bg-gray-800 p-4 rounded shadow">
          <h3 className="text-xl font-semibold mb-2 text-blue-300">
            🧪 Encrypted Raw Data
          </h3>
          <div className="space-y-2 max-h-[25rem] overflow-auto">
            {rawData.map((data, index) => (
              <p key={index} className="text-sm text-gray-200 break-words">
                {data}
              </p>
            ))}
          </div>
        </div>

        <div className="bg-gray-800 p-4 rounded shadow">
          <h3 className="text-xl font-semibold mb-2 text-green-300">
            Decrypted
          </h3>
          <div className="space-y-2 max-h-[25rem] overflow-auto">
            {Array.from(new Set(historyData) as Set<string>).map(
              (data, index) => (
                <div key={index} className="bg-gray-900 p-2 rounded">
                  <p className="text-green-400 text-sm break-words">
                    <strong>Decrypted Data:</strong>{" "}
                    {data || "No data available"}
                  </p>
                </div>
              )
            )}
            {/* {decryptedData.length === 0 ? (
              <p className="text-sm text-gray-300">
                No decrypted data found yet.
              </p>
            ) : (
              decryptedData.map((data, index) => (
                <div key={index} className="bg-gray-900 p-2 rounded">
                  <p className="text-green-400 text-sm break-words">{data}</p>
                </div>
              ))
            )} */}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ReceiverPage;
