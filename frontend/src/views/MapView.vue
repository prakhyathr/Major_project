<template>
  <div class="h-screen flex flex-col">
    <!-- Header -->
    <header class="bg-white shadow z-10 p-4 flex justify-between items-center">
      <h1 class="text-xl font-bold text-gray-800">Bengaluru Event Discovery</h1>
      <div class="flex items-center space-x-4">
        <label class="flex items-center space-x-2 text-sm text-gray-700">
          <input type="checkbox" v-model="showRecommendationsOnly" class="rounded text-indigo-600 focus:ring-indigo-500">
          <span>Show Recommendations Only</span>
        </label>
        <select v-model="selectedZone" @change="flyToZone" class="form-select rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50">
          <option value="" disabled>Select Zone</option>
          <option v-for="(coords, name) in activeZones" :key="name" :value="name">{{ name }}</option>
        </select>
        <button @click="logout" class="text-sm text-red-600 hover:text-red-800">Logout</button>
      </div>
    </header>

    <!-- Map Container -->
    <div id="map" class="flex-grow z-0"></div>

    <!-- Recommendations Panel (Slide-over or Bottom Sheet) -->
    <div v-if="recommendations.length > 0" class="absolute bottom-4 left-4 right-4 bg-white p-4 rounded-lg shadow-lg z-20 max-h-64 overflow-y-auto sm:w-96 sm:left-auto sm:right-4 sm:bottom-4">
      <h3 class="font-bold text-lg mb-2">Recommended for You</h3>
      <div class="space-y-2">
        <div v-for="event in recommendations" :key="event.id" @click="flyToEvent(event)" class="border-b pb-2 last:border-0 cursor-pointer hover:bg-gray-50 p-2 rounded transition-colors">
          <h4 class="font-medium text-indigo-600">{{ event.title }}</h4>
          <p class="text-xs text-gray-500">{{ formatDate(event.start_time) }} • {{ event.main_zone }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import 'leaflet.markercluster/dist/MarkerCluster.css'
import 'leaflet.markercluster/dist/MarkerCluster.Default.css'
import 'leaflet.markercluster'

const router = useRouter()
const map = ref(null)
const markers = ref(null)
const selectedZone = ref("")
const recommendations = ref([])
const activeZones = ref({})
const allEvents = ref([])
const showRecommendationsOnly = ref(false)

const knownZones = {
  "Central (MG Road/Brigade)": [12.9756, 77.6066],
  "Indiranagar": [12.9719, 77.6412],
  "Koramangala": [12.9352, 77.6271],
  "HSR Layout": [12.9121, 77.6446],
  "Whitefield": [12.9698, 77.7499],
  "Jayanagar": [12.9250, 77.5808],
  "JP Nagar": [12.9063, 77.5857],
  "Malleshwaram": [13.0031, 77.5703],
  "Hebbal": [13.0354, 77.5988],
  "Electronic City": [12.8452, 77.6687],
  "Bannerghatta Road": [12.8958, 77.6018],
  "Bellandur/Sarjapur": [12.9260, 77.6762],
  "Yelahanka": [13.1007, 77.5963]
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString()
}

const logout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}

const flyToZone = () => {
  if (selectedZone.value && activeZones.value[selectedZone.value]) {
    map.value.setView(activeZones.value[selectedZone.value], 14)
  }
}

// Helper to calculate distance between two coords in km
const getDistanceFromLatLonInKm = (lat1, lon1, lat2, lon2) => {
  var R = 6371; // Radius of the earth in km
  var dLat = deg2rad(lat2-lat1);
  var dLon = deg2rad(lon2-lon1); 
  var a = 
    Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) * 
    Math.sin(dLon/2) * Math.sin(dLon/2)
    ; 
  var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
  var d = R * c; // Distance in km
  return d;
}

const deg2rad = (deg) => {
  return deg * (Math.PI/180)
}

const updateActiveZones = (events) => {
  const newActiveZones = {}
  
  // For each known zone, check if there's at least one event within 3km
  for (const [zoneName, coords] of Object.entries(knownZones)) {
    const hasEvent = events.some(event => {
      if (!event.location || !event.location.coordinates) return false
      const [lng, lat] = event.location.coordinates
      return getDistanceFromLatLonInKm(coords[0], coords[1], lat, lng) <= 3.0
    })
    
    if (hasEvent) {
      newActiveZones[zoneName] = coords
    }
  }
  
  activeZones.value = newActiveZones
}

// Add response interceptor logic or simple check
const handleAuthError = (response) => {
  if (response.status === 401 || response.status === 403) {
    localStorage.removeItem('token')
    router.push('/login')
    return true
  }
  return false
}

const renderMarkers = (eventsToRender) => {
    // Clear existing markers
    if (markers.value) {
      markers.value.clearLayers()
    }
    
    markers.value = L.markerClusterGroup()
    
    eventsToRender.forEach(event => {
      if (event.location && event.location.coordinates) {
        const [lng, lat] = event.location.coordinates
        const marker = L.marker([lat, lng])
          .bindPopup(`<b>${event.title}</b><br>${event.description}<br><a href="${event.source_url}" target="_blank">View Details</a>`)
        markers.value.addLayer(marker)
      }
    })
    
    map.value.addLayer(markers.value)
}

const fetchEvents = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch(`${import.meta.env.VITE_API_URL}/api/v1/events/`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    
    if (handleAuthError(response)) return
    
    const events = await response.json()
    allEvents.value = events // Store all events
    
    // Update zones based on fetched events
    updateActiveZones(events)
    
    // Initial render
    renderMarkers(events)
    
  } catch (error) {
    console.error("Failed to fetch events:", error)
  }
}

const fetchRecommendations = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch(`${import.meta.env.VITE_API_URL}/api/v1/recommendations/`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    
    if (handleAuthError(response)) return

    if (response.ok) {
      recommendations.value = await response.json()
    }
  } catch (error) {
    console.error("Failed to fetch recommendations:", error)
  }
}

watch(showRecommendationsOnly, (newValue) => {
    if (newValue) {
        // Filter events to show only those in recommendations
        // We match by ID or Title (assuming unique titles for now if IDs differ)
        // Best to use ID if available. MongoDB uses _id.
        const recIds = new Set(recommendations.value.map(r => r.id || r._id))
        const filtered = allEvents.value.filter(e => recIds.has(e.id || e._id))
        renderMarkers(filtered)
    } else {
        renderMarkers(allEvents.value)
    }
})

const flyToEvent = (event) => {
  if (event.location && event.location.coordinates) {
    const [lng, lat] = event.location.coordinates
    map.value.flyTo([lat, lng], 16)
    
    // Find marker in cluster group
    if (markers.value) {
        markers.value.eachLayer((layer) => {
            const layerLatLng = layer.getLatLng();
            if (Math.abs(layerLatLng.lat - lat) < 0.0001 && Math.abs(layerLatLng.lng - lng) < 0.0001) {
                markers.value.zoomToShowLayer(layer, () => layer.openPopup());
            }
        });
    }
  }
}

onMounted(() => {
  // Initialize Map
  map.value = L.map('map').setView([12.9716, 77.5946], 12) // Bengaluru Center
  
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map.value)
  
  fetchEvents()
  fetchRecommendations()
})
</script>
<style>
/* Fix for Leaflet icon not showing */
.leaflet-default-icon-path {
  background-image: url(https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png);
}
.cursor-pointer {
    cursor: pointer;
}
</style>
