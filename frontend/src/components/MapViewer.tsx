import React, { useEffect } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

interface Props {
  geojsonLayers: Record<string, any> | null;
}

const MapViewer: React.FC<Props> = ({ geojsonLayers }) => {
  useEffect(() => {
    const map = L.map('map', {
      center: [14.6928, -17.4467], // Dakar par défaut
      zoom: 11,
      scrollWheelZoom: true,
    });

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap',
    }).addTo(map);

    if (geojsonLayers) {
      const colors: Record<string, string> = {
        doublons_geom: 'red',
        doublons_nicad: 'orange',
        invalides: 'purple',
        vides: 'gray',
        surfaces_nulles: 'blue',
      };

      Object.entries(geojsonLayers).forEach(([key, geojson]) => {
        if (!geojson) return;

        const layer = L.geoJSON(JSON.parse(geojson), {
          style: { color: colors[key] || 'black', weight: 1 },
          onEachFeature: (feature, layer) => {
            const props = feature.properties;
            const label = props?.NICAD || props?.ID_NICAD || 'Sans NICAD';
            layer.bindPopup(`${key} : ${label}`);
          },
        });

        layer.addTo(map);
        map.fitBounds(layer.getBounds());
      });
    }

    return () => {
      map.remove();
    };
  }, [geojsonLayers]);

  return (
    <div id="map" className="h-[500px] w-full rounded shadow border" />
  );
};

export default MapViewer;
