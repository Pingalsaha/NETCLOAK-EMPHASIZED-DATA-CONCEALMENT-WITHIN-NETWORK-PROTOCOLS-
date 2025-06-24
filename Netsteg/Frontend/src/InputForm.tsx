import React, { useState, useEffect } from "react";
import axios from "axios";

const InputForm: React.FC = () => {
  const [inputData, setInputData] = useState<
    string | number | boolean | object
  >("");
  const [statusMessage, setStatusMessage] = useState<string>("");
  const [logs, setLogs] = useState<string[]>([]);
  const [rawdata, setRawData] = useState<string[]>([]);
  

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputData(e.target.value);
  };

  const handleFormSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://localhost:5000/save-input", {
        inputData,
      });
      setStatusMessage(response.data.message);
    } catch (error) {
      console.error("Error saving data:", error);
      setStatusMessage("Failed to save data");
    }
  };

  // Fetch logs from the backend periodically
  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const responseLogs = await axios.get("http://localhost:5000/logs");
        setLogs(responseLogs.data.logs);
      } catch (error) {
        console.error("Error fetching logs:", error);
      }
    };

    // Poll the logs every 5 seconds
    const intervalId = setInterval(fetchLogs, 5000);

    // Clean up the interval on component unmount
    return () => clearInterval(intervalId);
  }, []);

  // Fetch rawData from the backend periodically
  useEffect(() => {
    const fetchRawData = async () => {
      try {
        const responseRawData = await axios.get("http://localhost:5000/rawData");
        setRawData(responseRawData.data.rawData);
      } catch (error) {
        console.error("Error fetching logs:", error);
      }
    };

    // Poll the logs every 5 seconds
    const intervalId = setInterval(fetchRawData, 5000);

    // Clean up the interval on component unmount
    return () => clearInterval(intervalId);
  }, []);

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-black">
      <h2 className="text-2xl font-semibold mb-4 text-[#fff]">Data Input</h2>
      <form
        onSubmit={handleFormSubmit}
        className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4 w-96"
      >
        <label
          htmlFor="inputField"
          className="block text-gray-700 text-sm font-bold mb-2"
        >
          Enter data:
        </label>
        <input
          type="text"
          id="inputField"
          value={String(inputData)}
          onChange={handleInputChange}
          className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
        />
        <button
          type="submit"
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline mt-4"
        >
          Save
        </button>
      </form>
      {statusMessage && <p className="text-green-500 mt-4">{statusMessage}</p>}

      <div className="w-[90%] flex flex-row gap-16 justify-between">
        <div className="mt-8 w-[30%] h-[40rem] overflow-scroll bg-white shadow-md rounded p-4">
          <h3 className="text-xl font-semibold mb-2">Backend Logs</h3>
          {logs.map((log, index) => (
            <p key={index} className="text-gray-700 text-sm">
              {log}
            </p>
          ))}
        </div>

        <div className="mt-8 w-[70%] h-[40rem] overflow-scroll bg-white shadow-md rounded p-4">
          <h3 className="text-xl font-semibold mb-2">Raw Data</h3>
          {rawdata.map((data, index) => (
            <p key={index} className="text-gray-700 text-sm">
              {data}
            </p>
          ))}
        </div>
      </div>
    </div>
  );
};

export default InputForm;
