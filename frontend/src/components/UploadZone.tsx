import React, { useState } from 'react';

interface Props {
  onComplete: (
    geojsons: any,
    iaSummary: string,
    links: { pdf: string; excel: string },
    stats: any,
    filename: string
  ) => void;
}

const UploadZone: React.FC<Props> = ({ onComplete }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const ext = file.name.split('.').pop()?.toLowerCase();
    if (!['shp', 'geojson', 'gpkg', 'dxf', 'dgn'].includes(ext || '')) {
      setError('Format non supporté. Veuillez envoyer un fichier SIG ou DAO (.shp, .geojson, .gpkg, .dxf, .dgn)');
      return;
    }

    setLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('file', file);

    const route = ext === 'dxf' ? 'dxf' : ext === 'dgn' ? 'dgn' : 'sig';

    try {
      const response = await fetch(`http://localhost:8000/${route}/upload`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Erreur lors de l’analyse');
      }

      const geojsons = Object.fromEntries(
        Object.entries(data.nb_erreurs).map(([key]) => [key, data.errors?.[key] || null])
      );

      onComplete(geojsons, data.resume_ia, data.downloads, data.nb_erreurs, data.filename);
    } catch (err: any) {
      setError(err.message || 'Erreur inconnue');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white p-4 rounded-lg shadow border">
      <label className="block font-semibold text-gray-700 mb-2">
        📥 Téléverser un fichier SIG / DXF / DGN
      </label>
      <input
        type="file"
        onChange={handleFileUpload}
        accept=".shp,.geojson,.gpkg,.dxf,.dgn"
        className="block w-full border border-gray-300 p-2 rounded"
      />
      {loading && <p className="text-blue-600 mt-2">Analyse en cours… ⏳</p>}
      {error && <p className="text-red-600 mt-2">{error}</p>}
    </div>
  );
};

export default UploadZone;
