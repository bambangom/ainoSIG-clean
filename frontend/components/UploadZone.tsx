import React, { useState } from "react";
import axios from "axios";
import MapViewer from "./MapViewer";
import ChatPanel from "./ChatPanel";
import AuditPanel from "./AuditPanel";

const UploadZone: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [response, setResponse] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    setSelectedFile(file || null);
    setResponse(null);
  };

  const handleUpload = async () => {
    if (!selectedFile) return;
    const formData = new FormData();
    formData.append("file", selectedFile);

    setLoading(true);
    try {
      const res = await axios.post("http://localhost:8000/dgn/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResponse(res.data);
    } catch (err) {
      console.error("Erreur lors de l’upload :", err);
      alert("❌ Erreur lors de l’audit du fichier.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        border: "2px dashed #ccc",
        padding: "30px",
        borderRadius: "8px",
        backgroundColor: "#fff",
        maxWidth: "700px",
        margin: "auto",
      }}
    >
      <h2 style={{ color: "#0d4e32" }}>📂 Téléverser un fichier SIG/DGN</h2>

      <input
        type="file"
        onChange={handleFileChange}
        accept=".shp,.dgn,.geojson,.gpkg,.zip"
        style={{ marginBottom: "20px" }}
      />

      <button
        onClick={handleUpload}
        disabled={!selectedFile || loading}
        style={{
          padding: "10px 20px",
          backgroundColor: "#0d4e32",
          color: "#fff",
          border: "none",
          cursor: "pointer",
          borderRadius: "4px",
        }}
      >
        {loading ? "Analyse en cours..." : "Lancer l’audit"}
      </button>

      {response?.downloads?.geojson && (
        <div style={{ marginTop: 30 }}>
          <h4>🗺️ Carte de prévisualisation</h4>
          <MapViewer geojsonUrl={`http://localhost:8000${response.downloads.geojson}`} />
        </div>
      )}

      {response?.resume_ia && (
        <ChatPanel resumeIa={response.resume_ia} />
      )}

      {response?.nb_erreurs && (
        <AuditPanel stats={response.nb_erreurs} />
      )}

      {response?.downloads && (
        <div style={{ marginTop: 30 }}>
          <h4>📥 Téléchargements</h4>
          <ul>
            {response.downloads.pdf && (
              <li>
                <a href={`http://localhost:8000${response.downloads.pdf}`} target="_blank" rel="noreferrer">
                  📝 Rapport PDF
                </a>
              </li>
            )}
            {response.downloads.excel && (
              <li>
                <a href={`http://localhost:8000${response.downloads.excel}`} target="_blank" rel="noreferrer">
                  📊 Rapport Excel
                </a>
              </li>
            )}
            {response.downloads.gpkg && (
              <li>
                <a href={`http://localhost:8000${response.downloads.gpkg}`} target="_blank" rel="noreferrer">
                  🗂️ Fichier GPKG converti
                </a>
              </li>
            )}
          </ul>
        </div>
      )}
    </div>
  );
};

export default UploadZone;
