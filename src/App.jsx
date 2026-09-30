import { useState } from "react";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [analyzed, setAnalyzed] = useState(false);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // -----------------------------------------
  // FILE SELECTION
  // -----------------------------------------

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];

    if (selectedFile) {
      setFile(selectedFile);
      setAnalyzed(false);
      setResult(null);
      setError("");
    }
  };

  // -----------------------------------------
  // ANALYZE DATASET
  // -----------------------------------------

  const handleAnalyze = async () => {
    if (!file) {
      setError("Please select a CSV or Excel file first.");
      return;
    }

    try {
      setLoading(true);
      setError("");

      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch("/api/analyze", {
        method: "POST",
        body: formData,
      });

      const data = await response.json().catch(() => null);

      if (!response.ok || !data) {
        const message = data?.detail || data?.error || "Analysis failed.";
        throw new Error(message);
      }

      console.log("Backend Response:", data);

      setResult(data);
      setAnalyzed(true);
    } catch (error) {
      console.error("Error:", error);
      setError(
        error.message.includes("Failed to fetch")
          ? "Backend is not reachable. Start the FastAPI server and refresh the page."
          : error.message
      );
    } finally {
      setLoading(false);
    }
  };

  // -----------------------------------------
  // FORMAT NUMBER
  // -----------------------------------------

  const formatNumber = (number) => {
    if (number === undefined || number === null) {
      return "N/A";
    }

    return Number(number).toLocaleString("en-IN", {
      maximumFractionDigits: 2,
    });
  };

  // -----------------------------------------
  // RETURN UI
  // -----------------------------------------

  return (
    <div className="app">

      {/* =====================================
          HEADER
      ====================================== */}

      <header className="header">

        <div className="logo">

          <div className="logo-icon">
            DS
          </div>

          <div>
            <h2>Dataset Storyteller</h2>
            <p>Insight Narrator</p>
          </div>

        </div>

        <nav>
          <a href="#dashboard">Dashboard</a>
          <a href="#insights">Insights</a>
          <a href="#story">Story</a>
        </nav>

      </header>


      {/* =====================================
          HERO SECTION
      ====================================== */}

      <section className="hero" id="dashboard">

        <h1>
          Dataset Storyteller
          <span> & Insight Narrator</span>
        </h1>

        <p>
          Upload your dataset and automatically discover
          meaningful insights, visualizations and data stories.
        </p>


        {/* =================================
            UPLOAD BOX
        ================================== */}

        <div className="upload-box">

          <div className="upload-icon">
            📊
          </div>

          <h2>
            Upload Your Dataset
          </h2>

          <p>
            Upload a CSV or Excel file to analyze your data.
          </p>

          <input
            type="file"
            accept=".csv,.xlsx,.xls"
            onChange={handleFileChange}
          />

          {file && (
            <p className="file-name">
              Selected file:
              <strong> {file.name}</strong>
            </p>
          )}

          <button
            onClick={handleAnalyze}
            disabled={loading}
          >
            {loading
              ? "Analyzing..."
              : "Analyze Dataset"}
          </button>

          {error && (
            <p className="error-message" role="alert">
              {error}
            </p>
          )}

        </div>

      </section>


      {/* =====================================
          RESULTS
      ====================================== */}

      {analyzed && result && (

        <>

          {/* =================================
              DATASET OVERVIEW
          ================================== */}

          <section className="section">

            <h2>
              Dataset Overview
            </h2>

            <div className="stats-grid">

              <div className="stat-card">

                <h3>
                  {result.analysis.rows}
                </h3>

                <p>
                  Total Records
                </p>

              </div>


              <div className="stat-card">

                <h3>
                  {result.analysis.columns}
                </h3>

                <p>
                  Total Columns
                </p>

              </div>


              <div className="stat-card">

                <h3>
                  {result.cleaning.missing_values_before}
                </h3>

                <p>
                  Missing Values
                </p>

              </div>


              <div className="stat-card">

                <h3>
                  {result.cleaning.duplicate_rows_before}
                </h3>

                <p>
                  Duplicate Rows
                </p>

              </div>

            </div>

          </section>


          {/* =================================
              ANALYSIS INFORMATION
          ================================== */}

          <section className="section">

            <h2>
              Dataset Analysis
            </h2>

            <div className="charts-grid">

              <div className="chart-card">

                <h3>
                  Numerical Columns
                </h3>

                {result.analysis.numerical_columns.length > 0 ? (

                  <ul>

                    {result.analysis.numerical_columns.map(
                      (column) => (
                        <li key={column}>
                          {column}
                        </li>
                      )
                    )}

                  </ul>

                ) : (

                  <p>
                    No numerical columns found.
                  </p>

                )}

              </div>


              <div className="chart-card">

                <h3>
                  Categorical Columns
                </h3>

                {result.analysis.categorical_columns.length > 0 ? (

                  <ul>

                    {result.analysis.categorical_columns.map(
                      (column) => (
                        <li key={column}>
                          {column}
                        </li>
                      )
                    )}

                  </ul>

                ) : (

                  <p>
                    No categorical columns found.
                  </p>

                )}

              </div>

            </div>

          </section>


          {/* =================================
              NUMERICAL SUMMARY
          ================================== */}

          <section className="section">

            <h2>
              Numerical Summary
            </h2>

            <div className="charts-grid">

              {Object.entries(
                result.analysis.numerical_summary
              ).map(([column, values]) => (

                <div
                  className="chart-card"
                  key={column}
                >

                  <h3>
                    {column}
                  </h3>

                  <p>
                    <strong>Average:</strong>{" "}
                    {formatNumber(values.mean)}
                  </p>

                  <p>
                    <strong>Median:</strong>{" "}
                    {formatNumber(values.median)}
                  </p>

                  <p>
                    <strong>Minimum:</strong>{" "}
                    {formatNumber(values.minimum)}
                  </p>

                  <p>
                    <strong>Maximum:</strong>{" "}
                    {formatNumber(values.maximum)}
                  </p>

                </div>

              ))}

            </div>

          </section>


          {/* =================================
              INSIGHTS
          ================================== */}

          <section
            className="section"
            id="insights"
          >

            <h2>
              Key Insights
            </h2>

            <div className="insights-grid">

              {result.insights.map(
                (insight, index) => (

                  <div
                    className="insight-card"
                    key={index}
                  >

                    <h3>
                      💡 Insight {index + 1}
                    </h3>

                    <p>
                      {insight}
                    </p>

                  </div>

                )
              )}

            </div>

          </section>


          {/* =================================
              DATA PREVIEW
          ================================== */}

          <section className="section">

            <h2>
              Dataset Preview
            </h2>

            <div className="table-container">

              {result.preview.length > 0 ? (

                <table>

                  <thead>

                    <tr>

                      {Object.keys(
                        result.preview[0]
                      ).map((column) => (

                        <th key={column}>
                          {column}
                        </th>

                      ))}

                    </tr>

                  </thead>

                  <tbody>

                    {result.preview.map(
                      (row, rowIndex) => (

                        <tr key={rowIndex}>

                          {Object.keys(row).map(
                            (column) => (

                              <td key={column}>
                                {String(
                                  row[column]
                                )}
                              </td>

                            )
                          )}

                        </tr>

                      )
                    )}

                  </tbody>

                </table>

              ) : (

                <p>
                  No preview available.
                </p>

              )}

            </div>

          </section>


          {/* =================================
              STORY
          ================================== */}

          <section
            className="section"
            id="story"
          >

            <h2>
              AI Generated Story
            </h2>

            <div className="story-card">

              <h3>
                📖 Data Story
              </h3>

              <p>
                {result.story}
              </p>

            </div>

          </section>

        </>

      )}


      {/* =====================================
          FOOTER
      ====================================== */}

      <footer>

        <h3>
          Dataset Storyteller & Insight Narrator
        </h3>

        <p>
          AI-Powered Data Analysis Platform
        </p>

      </footer>

    </div>
  );
}

export default App;