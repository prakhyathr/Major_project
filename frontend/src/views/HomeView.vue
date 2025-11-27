<template>
  <div class="h-screen w-full flex flex-col">
    <nav class="bg-white shadow p-4 flex justify-between items-center z-10">
      <h1 class="text-xl font-bold text-primary">BLR Event Discovery</h1>
      <div>
        <router-link to="/login" class="text-gray-600 hover:text-primary">Vendor Login</router-link>
      </div>
    </nav>
    <div id="map" class="flex-grow w-full z-0"></div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

onMounted(() => {
  // Initialize Leaflet Map
  const map = L.map('map').setView([12.9716, 77.5946], 12); // Bengaluru

  // Add OpenStreetMap Tile Layer (Free & Open Source)
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(map);

  // Example Marker
  L.marker([12.9716, 77.5946])
    .addTo(map)
    .bindPopup('Bengaluru Central')
    .openPopup();
})
</script>

<style>
/* Fix for Leaflet z-index issues if any */
.leaflet-pane {
    z-index: 0 !important;
}
</style>
