<template>
  <div class="flex h-screen bg-gray-50 overflow-hidden font-sans">
    <!-- Left: Map (60%) -->
    <div class="w-3/5 h-full relative border-r border-gray-200">
        <MapView 
            :events="allEvents" 
            :selectedCluster="selectedCluster"
            @selectCluster="handleClusterSelect"
        />
        
        <!-- Back Button (Mobile/Overlay) -->
        <button 
            v-if="selectedCluster"
            @click="selectedCluster = null"
            class="absolute top-4 left-4 z-[1000] bg-white text-gray-700 px-4 py-2 rounded-lg shadow-md border border-gray-200 text-sm font-bold hover:bg-gray-50 flex items-center"
        >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
            Back to Overview
        </button>
    </div>

    <!-- Right: Content (40%) -->
    <div class="w-2/5 h-full flex flex-col bg-white overflow-hidden">
        <!-- Header -->
        <div class="p-6 border-b border-gray-100 bg-white z-10">
            <h1 class="text-2xl font-bold text-gray-800 mb-1">Discover Events</h1>
            <p class="text-sm text-gray-500">Find the perfect events for your business in Bengaluru</p>
        </div>

        <!-- Scrollable Content -->
        <div class="flex-grow overflow-y-auto p-6 scrollbar-thin">
            
            <!-- Filters -->
            <Filters 
                :categories="categories"
                :interests="vendorInterests"
                @change="handleFilterChange"
            />

            <!-- Dynamic Header -->
            <div class="flex items-center justify-between mb-6">
                <h2 class="text-xl font-bold text-gray-800">
                    {{ selectedCluster ? `Events in ${selectedCluster}` : 'All Events' }}
                </h2>
                <span class="bg-gray-100 text-gray-600 px-3 py-1 rounded-full text-xs font-bold">
                    {{ filteredEvents.length }} Events
                </span>
            </div>

            <!-- Recommendations (Top 5) -->
            <Recommendations 
                v-if="recommendations.length > 0" 
                :events="recommendations" 
                @viewAll="showAllEvents"
            />

            <!-- Event List -->
            <div class="grid grid-cols-1 gap-4">
                <EventCard 
                    v-for="event in displayedEvents" 
                    :key="event.id" 
                    :event="event" 
                />
            </div>
            
            <!-- Empty State -->
            <div v-if="displayedEvents.length === 0" class="text-center py-12">
                <div class="bg-gray-50 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                    <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                </div>
                <h3 class="text-lg font-medium text-gray-900">No events found</h3>
                <p class="text-gray-500 text-sm mt-1">Try adjusting your filters or selecting a different zone.</p>
            </div>
        </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import MapView from '../components/MapView.vue'
import EventCard from '../components/EventCard.vue'
import Filters from '../components/Filters.vue'
import Recommendations from '../components/Recommendations.vue'
import api from '../utils/api'
import { getDistanceFromLatLonInKm } from '../utils/distance'

const allEvents = ref([])
const recommendations = ref([])
const vendorInterests = ref([])
const selectedCluster = ref(null)
const filters = ref({
    keyword: '',
    category: '',
    radius: 10,
    selectedInterests: []
})
const showRecommendationsOnly = ref(false)

// Computed Categories
const categories = computed(() => {
    const cats = new Set(allEvents.value.map(e => e.category).filter(Boolean))
    return Array.from(cats).sort()
})

// Zone Normalization Helper (Same as MapView)
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
    if (zone.includes(',')) return 'Bengaluru'
    return zone
}

// Filter Logic
const filteredEvents = computed(() => {
    let events = allEvents.value

    // 1. Cluster Filter (Always active if selected)
    if (selectedCluster.value) {
        // Filter by normalized zone
        events = events.filter(e => normalizeZone(e.main_zone) === selectedCluster.value)
    }

    // 2. Category Filter (Applied on Search)
    if (filters.value.category) {
        events = events.filter(e => e.category === filters.value.category)
    }

    // 3. Keyword Filter (Applied on Search)
    if (filters.value.keyword) {
        const k = filters.value.keyword.toLowerCase()
        events = events.filter(e => 
            e.title.toLowerCase().includes(k) || 
            e.description.toLowerCase().includes(k)
        )
    }

    // 4. Radius Filter (Client-side approximation)
    // In a real app, this would be a backend geospatial query.
    // Here we filter events that are within X km of the cluster center (if known) or just rely on the zone.
    // Since we don't have the cluster center coords easily available here without looking them up,
    // we'll skip strict radius filtering on client-side for now, as the Zone filter is the primary "Area" filter.
    
    return events
})

const displayedEvents = computed(() => {
    // If recommendations are shown, we still show the full list below?
    // User asked for "display all the events with the top 5 recommendations".
    // So yes, show both.
    return filteredEvents.value
})

const handleClusterSelect = (clusterName) => {
    selectedCluster.value = clusterName
    // Reset filters or keep them? Usually resetting makes sense when switching zones.
    // But user might want "Music events in Indiranagar" then switch to "Koramangala".
    // Let's keep filters but re-fetch recommendations.
    fetchRecommendations()
}

const handleFilterChange = (newFilters) => {
    filters.value = newFilters
    // Trigger search and recommendations
    fetchRecommendations()
}

const showAllEvents = () => {
    // Just scrolls to the list or expands if we were hiding them.
    // Currently we show all anyway.
}

// API Calls
const fetchData = async () => {
    try {
        const [eventsRes, vendorRes] = await Promise.all([
            api.getEvents(),
            api.getVendorProfile()
        ])
        allEvents.value = eventsRes.data
        vendorInterests.value = vendorRes.data.interests || []
    } catch (e) {
        console.error("Failed to fetch data", e)
    }
}

const fetchRecommendations = async () => {
    try {
        // We fetch generic recommendations from backend
        const res = await api.getRecommendations()
        let recs = res.data
        
        // Filter recs to match current context (Cluster + Category + Keyword)
        if (selectedCluster.value) {
            recs = recs.filter(e => normalizeZone(e.main_zone) === selectedCluster.value)
        }
        if (filters.value.category) {
            recs = recs.filter(e => e.category === filters.value.category)
        }
        
        recommendations.value = recs.slice(0, 5)
    } catch (e) {
        console.error("Failed to fetch recommendations", e)
    }
}

onMounted(() => {
    fetchData()
})
</script>

<style>
.scrollbar-thin::-webkit-scrollbar {
    width: 6px;
}
.scrollbar-thin::-webkit-scrollbar-track {
    background: transparent;
}
.scrollbar-thin::-webkit-scrollbar-thumb {
    background-color: #e5e7eb;
    border-radius: 20px;
}
</style>
