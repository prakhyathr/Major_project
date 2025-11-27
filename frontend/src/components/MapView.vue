<template>
  <div class="h-full w-full relative">
    <div id="map" class="h-full w-full z-0"></div>
    
    <!-- Cluster Chips Overlay -->
    <div class="absolute bottom-6 left-4 right-4 z-[1000] bg-white/90 backdrop-blur-sm p-2 rounded-xl shadow-lg border border-gray-200">
        <ClusterChips 
            :clusters="clusters" 
            :selectedCluster="selectedCluster"
            @select="handleClusterSelect"
        />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import 'leaflet.markercluster/dist/MarkerCluster.css'
import 'leaflet.markercluster/dist/MarkerCluster.Default.css'
import 'leaflet.markercluster'
import ClusterChips from './ClusterChips.vue'

const props = defineProps({
  events: {
    type: Array,
    default: () => []
  },
  selectedCluster: {
    type: String,
    default: null
  }
})

const emit = defineEmits(['selectCluster'])

const map = ref(null)
const markers = ref(null)
const clusters = ref([])

// Fix for Leaflet icon
const fixLeafletIcon = () => {
    delete L.Icon.Default.prototype._getIconUrl;
    L.Icon.Default.mergeOptions({
        iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
        iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
    });
}

const initMap = () => {
    fixLeafletIcon()
    // Light Theme Map (CartoDB Positron)
    map.value = L.map('map', { zoomControl: false }).setView([12.9716, 77.5946], 12)
    
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 20
    }).addTo(map.value)
    
    L.control.zoom({ position: 'topright' }).addTo(map.value)
    
    markers.value = L.markerClusterGroup({
        showCoverageOnHover: false,
        zoomToBoundsOnClick: true,
        spiderfyOnMaxZoom: true,
        iconCreateFunction: function(cluster) {
            return L.divIcon({ 
                html: `<div class="flex items-center justify-center w-10 h-10 bg-orange-500 text-white rounded-full font-bold shadow-lg border-2 border-white">${cluster.getChildCount()}</div>`, 
                className: 'custom-cluster-icon', 
                iconSize: L.point(40, 40) 
            });
        }
    })
    
    map.value.addLayer(markers.value)
    
    // Handle cluster click
    markers.value.on('clusterclick', (a) => {
        const childMarkers = a.layer.getAllChildMarkers()
        if (childMarkers.length > 0) {
            const zones = {}
            childMarkers.forEach(m => {
                const z = m.options.zoneName
                if (z) zones[z] = (zones[z] || 0) + 1
            })
            const bestZone = Object.keys(zones).reduce((a, b) => zones[a] > zones[b] ? a : b)
            emit('selectCluster', bestZone)
        }
    })
}

// Zone Normalization Helper
const normalizeZone = (zone) => {
    if (!zone) return 'Bengaluru'
    const z = zone.toLowerCase()
    if (z.includes('indiranagar')) return 'Indiranagar'
    if (z.includes('koramangala')) return 'Koramangala'
    if (z.includes('hsr')) return 'HSR Layout'
    if (z.includes('whitefield')) return 'Whitefield'
    if (z.includes('jayanagar')) return 'Jayanagar'
    if (z.includes('jp nagar')) return 'JP Nagar'
    if (z.includes('electronic city')) return 'Electronic City'
    if (z.includes('mg road') || z.includes('brigade road')) return 'MG Road'
    if (z.includes('malleshwaram')) return 'Malleshwaram'
    if (z.includes('marathahalli')) return 'Marathahalli'
    if (z.includes('bellandur')) return 'Bellandur'
    if (z.includes('sarjapur')) return 'Sarjapur Road'
    if (z.includes('yelahanka')) return 'Yelahanka'
    if (z.includes('hebbal')) return 'Hebbal'
    if (z.includes('banashankari')) return 'Banashankari'
    if (z.includes('basavanagudi')) return 'Basavanagudi'
    if (z.includes('btm')) return 'BTM Layout'
    if (z.includes('kalyan nagar')) return 'Kalyan Nagar'
    if (z.includes('new bel road')) return 'New BEL Road'
    if (z.includes('rajajinagar')) return 'Rajajinagar'
    if (z.includes('sadashivanagar')) return 'Sadashivanagar'
    if (z.includes('shantinagar')) return 'Shantinagar'
    if (z.includes('shivajinagar')) return 'Shivajinagar'
    if (z.includes('ulsoor') || z.includes('halasuru')) return 'Ulsoor'
    if (z.includes('vasanth nagar')) return 'Vasanth Nagar'
    if (z.includes('wilson garden')) return 'Wilson Garden'
    if (z.includes('yeshwanthpur')) return 'Yeshwanthpur'
    
    // If no match, return the original (or maybe 'Other'?)
    // Returning original might still result in messy chips, but better than losing data.
    // Let's try to be aggressive: if it looks like an address (contains commas), fallback to 'Bengaluru'
    if (zone.includes(',')) return 'Bengaluru'
    
    return zone
}

const updateMarkers = () => {
    if (!map.value || !markers.value) return
    
    markers.value.clearLayers()
    const clusterData = {}
    
    props.events.forEach(event => {
        if (event.location && event.location.coordinates) {
            const [lng, lat] = event.location.coordinates
            
            // Normalize the zone here
            const rawZone = event.main_zone || 'Bengaluru'
            const zone = normalizeZone(rawZone)
            
            // Override event.main_zone for consistency in UI? 
            // Better not mutate prop, but use local var for grouping.
            
            const marker = L.marker([lat, lng], { zoneName: zone })
                .bindPopup(`
                    <div class="font-sans">
                        <h3 class="font-bold text-gray-800">${event.title}</h3>
                        <p class="text-sm text-gray-600">${zone}</p>
                    </div>
                `)
            markers.value.addLayer(marker)
            
            // Aggregate for chips
            if (!clusterData[zone]) {
                clusterData[zone] = { name: zone, count: 0, lat, lng }
            }
            clusterData[zone].count++
        }
    })
    
    // Convert to array and sort by count
    clusters.value = Object.values(clusterData).sort((a, b) => b.count - a.count)
}

const handleClusterSelect = (cluster) => {
    emit('selectCluster', cluster.name)
    if (map.value) {
        map.value.setView([cluster.lat, cluster.lng], 15)
    }
}

watch(() => props.events, () => {
    updateMarkers()
}, { deep: true })

watch(() => props.selectedCluster, (newCluster) => {
    if (newCluster) {
        const cluster = clusters.value.find(c => c.name === newCluster)
        if (cluster) {
            map.value.setView([cluster.lat, cluster.lng], 15)
        }
    }
})

onMounted(() => {
    initMap()
    updateMarkers()
})
</script>

<style>
.custom-cluster-icon {
    background: transparent;
}
</style>
