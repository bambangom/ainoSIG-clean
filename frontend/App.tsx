import React, { useState } from "react";
import UploadZone from "./components/UploadZone";
import MapViewer from "./components/MapViewer"; // ✅ Assurez-vous que ce composant existe

function App() {
  const [response, setResponse] = useState<any>(null); // ← pour récupérer la réponse de l’upload

  return (
    <div style={{ padding: "20px" }}>
      <UploadZone onUploadSuccess={(res) => setResponse(res)} />

      {response?.downloads?.geojson && (
        <div style={{ marginTop: 30 }}>
          <h4>🗺️ Carte de prévisualisation</h4>
          <MapViewer geojsonUrl={`http://localhost:8000${response.downloads.geojson}`} />
        </div>
      )}
    </div>
  );
}

export default App;
