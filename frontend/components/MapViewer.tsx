import React, { useEffect, useRef } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

interface MapViewerProps {
  geojsonUrl: string;
}

const MapViewer: React.FC<MapViewerProps> = ({ geojsonUrl }) => {
  const mapRef = useRef<HTMLDivElement>(null);
  const leafletMap = useRef<L.Map | null>(null);

  useEffect(() => {
    if (!mapRef.current) return;

    if (leafletMap.current) {
      leafletMap.current.remove(); // reset map if it already exists
    }

    // 🌍 Init map
    leafletMap.current = L.map(mapRef.current).setView([14.6928, -17.4467], 10); // Dakar par défaut

    // 🗺️ Add OpenStreetMap layer
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "© OpenStreetMap contributors",
    }).addTo(leafletMap.current);

    // 🔄 Load GeoJSON
    fetch(geojsonUrl)
      .then((res) => res.json())
      .then((geojson) => {
        const layer = L.geoJSON(geojson, {
          style: {
            color: "#C19F33",
            weight: 2,
          },
        }).addTo(leafletMap.current!);

        leafletMap.current!.fitBounds(layer.getBounds());
      })
      .catch((err) => {
        console.error("Erreur chargement GeoJSON :", err);
      });
  }, [geojsonUrl]);

  return (
    <div
      ref={mapRef}
      style={{
        width: "100%",
        height: "400px",
        marginTop: "20px",
        borderRadius: 8,
        border: "1px solid #ccc",
      }}
    />
  );
};

export default MapViewer;
