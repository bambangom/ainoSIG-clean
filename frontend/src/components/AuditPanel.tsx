import React from 'react';

interface Props {
  resume: string;
  stats: Record<string, number>;
  downloads: {
    pdf: string;
    excel: string;
  } | null;
}

const AuditPanel: React.FC<Props> = ({ resume, stats, downloads }) => {
  return (
    <div className="bg-white p-4 rounded-lg shadow border space-y-4">
      <h2 className="text-xl font-bold text-blue-700">📊 Résultat de l’audit</h2>

      <div className="grid grid-cols-2 gap-2 text-sm">
        <div>🔁 Doublons géométriques : <strong>{stats?.doublons_geom || 0}</strong></div>
        <div>🆔 Doublons NICAD : <strong>{stats?.doublons_nicad || 0}</strong></div>
        <div>🚫 Géométries invalides : <strong>{stats?.invalides || 0}</strong></div>
        <div>⭕ Géométries vides : <strong>{stats?.vides || 0}</strong></div>
        <div>📏 Surfaces nulles : <strong>{stats?.surfaces_nulles || 0}</strong></div>
        <div>📦 Total des entités : <strong>{stats?.total || 0}</strong></div>
      </div>

      <div>
        <h3 className="text-md font-semibold mt-2 mb-1">🧠 Recommandations de l’IA :</h3>
        <div className="text-sm bg-gray-50 border border-gray-200 p-3 rounded overflow-y-auto max-h-60 whitespace-pre-wrap">
          {resume}
        </div>
      </div>

      {downloads && (
        <div className="flex flex-col space-y-2 pt-3 text-sm">
          <a
            href={downloads.pdf}
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 hover:underline"
          >
            📄 Télécharger le rapport PDF
          </a>
          <a
            href={downloads.excel}
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 hover:underline"
          >
            📊 Télécharger le fichier Excel des erreurs
          </a>
        </div>
      )}
    </div>
  );
};

export default AuditPanel;
