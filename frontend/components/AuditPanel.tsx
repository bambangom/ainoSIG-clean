import React from "react";
import { Bar, Pie } from "react-chartjs-2";
import {
  Chart as ChartJS,
  ArcElement,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(ArcElement, BarElement, CategoryScale, LinearScale, Tooltip, Legend);

interface Props {
  stats: {
    doublons_geom: number;
    doublons_nicad: number;
    invalides: number;
    vides: number;
    surfaces_nulles: number;
    total: number;
  };
}

const AuditPanel: React.FC<Props> = ({ stats }) => {
  const labels = [
    "Doublons géométriques",
    "Doublons NICAD",
    "Géométries invalides",
    "Géométries vides",
    "Surfaces nulles"
  ];

  const values = [
    stats.doublons_geom,
    stats.doublons_nicad,
    stats.invalides,
    stats.vides,
    stats.surfaces_nulles
  ];

  const barData = {
    labels,
    datasets: [
      {
        label: "Nombre d'erreurs",
        data: values,
        backgroundColor: "#0d4e32",
      },
    ],
  };

  const pieData = {
    labels,
    datasets: [
      {
        label: "Répartition",
        data: values,
        backgroundColor: [
          "#0d4e32",
          "#C19F33",
          "#888",
          "#bbb",
          "#444"
        ],
        borderColor: "#fff",
        borderWidth: 1,
      },
    ],
  };

  return (
    <div style={{ marginTop: "40px" }}>
      <h3 style={{ color: "#0d4e32" }}>📊 Synthèse des erreurs détectées</h3>

      <div style={{ display: "flex", flexWrap: "wrap", gap: "40px" }}>
        <div style={{ flex: "1 1 300px" }}>
          <Bar data={barData} options={{ responsive: true }} />
        </div>
        <div style={{ flex: "1 1 300px" }}>
          <Pie data={pieData} options={{ responsive: true }} />
        </div>
      </div>

      <p style={{ marginTop: "20px", fontSize: "0.9rem", color: "#555" }}>
        Total des entités analysées : <strong>{stats.total}</strong>
      </p>
    </div>
  );
};

export default AuditPanel;
