import { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [isError, setIsError] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setMessage("");
    setIsError(false);
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage("Please select a CSV file");
      setIsError(true);
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    setMessage("");
    setIsError(false);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/upload",
        formData,
        { responseType: "blob" }
      );

      const blob = new Blob([response.data], {
        type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      });

      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = "submission_analysis.xlsx";
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);

      setMessage("File processed successfully. Download started.");
    } catch (err) {
      setMessage("Upload failed. Please try again.");
      setIsError(true);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <div className="card">
        <h1>Coursera Duplicate Checker</h1>
        

        <input type="file" accept=".csv" onChange={handleFileChange} />

        <button onClick={handleUpload} disabled={loading}>
          {loading ? "Processing…" : "Upload & Process"}
        </button>

        {message && (
          <p className={`message ${isError ? "error" : "success"}`}>
            {message}
          </p>
        )}
      </div>
    </div>
  );
}

export default App;
