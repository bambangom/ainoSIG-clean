import React, { useState } from 'react';
import UploadZone from './components/UploadZone';
import MapViewer from './components/MapViewer';
import AuditPanel from './components/AuditPanel';
import ChatPanel from './components/ChatPanel';

export default function App() {
  const [geojsonData, setGeojsonData] = useState<any>(null);
  const [iaResponse, setIaResponse] = useState<string>('');
  const [downloads, setDownloads] = useState<{ pdf: string; excel: string } | null>(null);
  const [stats, setStats] = useState<any>(null);
  const [filename, setFilename] = useState<string>('');

  const handleUploadComplete = (
    geojsons: any,
    iaSummary: string,
    links: { pdf: string; excel: string },
    errorsCount: any,
    uploadedName: string
  ) => {
    setGeojsonData(geojsons);
    setIaResponse(iaSummary);
    setDownloads(links);
    setStats(errorsCount);
    setFilename(uploadedName);
  };

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 p-4">
      <header className="mb-4">
        <h1 className="text-3xl font-bold text-center text-blue-700">
          🌍 GEO-AINO SUPREME™
        </h1>
        <p className="text-center text-sm text-gray-600">
          Plateforme d’audit intelligent des fichiers géospatiaux avec IA intégrée (SIG, DXF, DGN)
        </p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="space-y-4">
          <UploadZone onComplete={handleUploadComplete} />
          {iaResponse && <AuditPanel resume={iaResponse} stats={stats} downloads={downloads} />}
          {filename && <ChatPanel filename={filename} />}
        </div>
        <div className="rounded-xl shadow border p-2 bg-white">
          <MapViewer geojsonLayers={geojsonData} />
        </div>
      </div>
    </div>
  );
}
