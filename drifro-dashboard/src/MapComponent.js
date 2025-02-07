import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import axios from 'axios';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix default icon issues in Leaflet when using Webpack:
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl:
    'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl:
    'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

function MapComponent() {
  const [zones, setZones] = useState([]);

  useEffect(() => {
    // Fetch optimized resource allocations from the API.
    axios
      .get("http://localhost:8000/optimize/")
      .then((response) => {
        // Dummy positions for demonstration.
        const markers = Object.keys(response.data.allocations).map((zone, idx) => ({
          zone,
          allocation: response.data.allocations[zone],
          position: [40.7128 + idx * 0.01, -74.0060 + idx * 0.01]
        }));
        setZones(markers);
      })
      .catch((error) => console.error("Error fetching zones:", error));
  }, []);

  return (
    <MapContainer center={[40.7128, -74.0060]} zoom={12} style={{ height: "80vh", width: "100%" }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {zones.map((zone, idx) => (
        <Marker key={idx} position={zone.position}>
          <Popup>
            {zone.zone}: {zone.allocation} resources allocated.
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}

export default MapComponent;
