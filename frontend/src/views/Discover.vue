<template>
  <div class="min-h-screen bg-gray-50 font-sans flex flex-col">
    
    <!-- Top Header (Sticky at top of window) -->
    <header class="sticky top-0 h-16 bg-white/90 backdrop-blur-md border-b border-gray-100 flex justify-between items-center px-8 z-50 shrink-0 shadow-sm">
        <div class="flex items-center">
            <img src="/assets/logo.jpg" alt="BLR Hive Logo" class="h-10 w-auto mr-4">
            <div>
                <h1 class="text-lg font-bold text-gray-800 leading-none">Discover</h1>
                <p class="text-[10px] text-gray-400 mt-1 uppercase tracking-wider">Bengaluru's Lifestyle Hub</p>
            </div>
        </div>
        <div class="flex items-center space-x-3">
            <button 
                @click="showSavedOnly = !showSavedOnly"
                class="text-xs font-bold px-4 py-2 rounded-lg transition-all flex items-center border shadow-sm"
                :class="showSavedOnly ? 'bg-orange-600 text-white border-orange-600' : 'bg-white text-gray-700 border-gray-200 hover:border-orange-200 hover:text-orange-600'"
            >
                <svg class="w-3.5 h-3.5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"></path>
                </svg>
                {{ showSavedOnly ? 'Show All' : 'Saved' }}
            </button>

            <button @click="$router.push('/profile')" class="text-xs text-gray-700 hover:text-orange-600 font-bold px-4 py-2 bg-white border border-gray-200 rounded-lg shadow-sm hover:border-orange-200 transition-all flex items-center">
                <svg class="w-3.5 h-3.5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>
                Profile
            </button>
            <button @click="logout" class="text-xs text-red-500 hover:text-red-700 font-bold px-3 py-2 border border-red-100 rounded-lg hover:bg-red-50 transition-colors">
                Logout
            </button>
        </div>
    </header>

    <!-- Main Discovery Section (Split Layout) -->
    <div class="px-8 py-6 flex gap-8">
        
        <!-- Left: Map Panel (Sticky at top-20) -->
        <div class="w-3/5">
            <div class="sticky top-24 h-[calc(100vh-theme(spacing.32))] relative rounded-3xl overflow-hidden border border-gray-200 shadow-2xl bg-white group">
                <MapView 
                    class="w-full h-full transform scale-100 group-hover:scale-[1.002] transition-transform duration-700"
                    :events="allEvents" 
                    :selectedCluster="selectedCluster"
                    @selectCluster="handleClusterSelect"
                />
                
                <!-- Floating Navigation -->
                <div class="absolute top-6 left-6 flex flex-col space-y-3 z-[1000]">
                    <button 
                        v-if="selectedCluster"
                        @click="selectedCluster = null"
                        class="bg-white/90 backdrop-blur-md text-gray-800 px-5 py-2.5 rounded-2xl shadow-xl border border-white/50 text-sm font-black hover:bg-white flex items-center transform hover:-translate-y-0.5 transition-all active:scale-95"
                    >
                        <svg class="w-4 h-4 mr-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
                        Back to All Events
                    </button>
                </div>
            </div>
        </div>

        <!-- Right: Event Feed (Natural Scrolling) -->
        <div class="w-2/5 flex flex-col pt-1">
            <div class="space-y-12">
                
                <!-- Filters Section -->
                <div class="sticky top-16 z-40 bg-gray-50/90 backdrop-blur-md pb-4 pt-1 ml-[-8px]">
                    <Filters 
                        :categories="categories"
                        :interests="vendorInterests"
                        @change="handleFilterChange"
                    />
                </div>

                <!-- Feed Context -->
                <div class="flex items-center justify-between group px-1">
                    <div>
                        <h2 class="text-2xl font-black text-gray-900 tracking-tight">
                            {{ selectedCluster ? `In ${selectedCluster}` : 'Live Feed' }}
                        </h2>
                        <p class="text-xs text-gray-400 mt-1 flex items-center">
                            <span class="w-1.5 h-1.5 bg-green-500 rounded-full mr-2 animate-pulse"></span>
                            Showing latest events in your area
                        </p>
                    </div>
                    <div class="flex flex-col items-end">
                        <span class="text-2xl font-black text-orange-600 leading-none">{{ filteredEvents.length }}</span>
                        <span class="text-[10px] font-bold text-gray-400 uppercase tracking-widest mt-1">Events</span>
                    </div>
                </div>

                <!-- Featured Recommendations -->
                <Recommendations 
                    v-if="recommendations.length > 0" 
                    :events="recommendations" 
                    @viewAll="scrollToResults"
                />

                <!-- Main Grid -->
                <div id="results-grid" class="space-y-6 px-1">
                    <EventCard 
                        v-for="event in displayedEvents" 
                        :key="event.id || event._id" 
                        :event="event"
                        :isSaved="savedEventIds.has(event.id || event._id)"
                        @toggleSave="handleToggleSave"
                        class="transform hover:scale-[1.02] transition-transform duration-300"
                    />
                </div>
                
                <!-- Empty State -->
                <div v-if="displayedEvents.length === 0" class="flex flex-col items-center justify-center py-24 px-12 bg-white rounded-[2rem] border-2 border-dashed border-gray-100 shadow-inner">
                    <div class="w-24 h-24 bg-orange-50 rounded-full flex items-center justify-center mb-6">
                        <svg class="w-12 h-12 text-orange-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
                        </svg>
                    </div>
                    <h3 class="text-xl font-black text-gray-900">No events found</h3>
                    <p class="text-gray-500 text-sm text-center mt-3 max-w-[240px]">We couldn't find any events matching these filters in {{ selectedCluster || 'this area' }}.</p>
                    <button @click="resetFilters" class="mt-8 px-6 py-3 bg-gray-900 text-white text-xs font-black uppercase tracking-widest rounded-xl hover:bg-orange-600 transition-colors shadow-lg active:scale-95">
                        Clear Filters
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Full-Width Bottom Sections (Below everything) -->
    <div class="bg-white border-t border-gray-100 mt-12 py-24">
        <div class="px-8 max-w-[1920px] mx-auto space-y-32">
            
            <!-- Explore by Date -->
            <section>
                <div class="flex items-center space-x-3 mb-12">
                    <div class="w-2 h-10 bg-orange-500 rounded-full"></div>
                    <h2 class="text-4xl font-black text-gray-900 tracking-tight">Explore by Date</h2>
                </div>
                <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6">
                    <button v-for="opt in dateOptions" :key="opt.label"
                        @click="handleDateSelect(opt.value)"
                        class="group p-8 rounded-[2.5rem] border-2 border-transparent bg-gray-50/50 hover:bg-white hover:shadow-2xl hover:border-orange-500 transition-all text-left flex flex-col justify-between h-48 relative overflow-hidden"
                        :class="{'bg-white border-orange-500 shadow-orange-100 ring-8 ring-orange-50': filters.dateRange === opt.value}"
                    >
                        <div class="z-10">
                            <span class="text-xs font-black text-gray-400 uppercase tracking-[0.2em] block mb-2">Schedule</span>
                            <span class="text-2xl font-black text-gray-900 group-hover:text-orange-600 transition-colors">{{ opt.label }}</span>
                        </div>
                        <div class="z-10 flex items-center justify-between">
                            <span class="text-sm font-bold text-gray-500">{{ opt.subtext }}</span>
                            <div class="w-12 h-12 rounded-2xl bg-white flex items-center justify-center shadow-sm group-hover:bg-orange-50 transition-colors">
                                <svg class="w-6 h-6 text-gray-300 group-hover:text-orange-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                                </svg>
                            </div>
                        </div>
                        <div class="absolute -right-6 -top-6 w-32 h-32 bg-orange-50/50 rounded-full blur-3xl group-hover:bg-orange-100/50 transition-all opacity-0 group-hover:opacity-100"></div>
                    </button>
                </div>
            </section>

            <!-- Popular Events Slider (Full Width) -->
            <section>
                <div class="flex items-center justify-between mb-12">
                    <div class="flex items-center space-x-3">
                        <div class="w-2 h-10 bg-orange-500 rounded-full"></div>
                        <h2 class="text-4xl font-black text-gray-900 tracking-tight">Trending in Bangalore</h2>
                    </div>
                    <button class="text-sm font-black uppercase tracking-widest text-orange-600 hover:text-orange-700 bg-orange-50 px-6 py-3 rounded-xl transform hover:scale-105 transition-all">View All Events</button>
                </div>
                <div class="flex overflow-x-auto space-x-8 pb-12 -mx-4 px-4 hide-scrollbar">
                    <div v-for="event in popularEvents" :key="'pop-'+(event.id || event._id)" class="flex-shrink-0 w-[420px]">
                        <EventCard 
                            :event="event" 
                            :isSaved="savedEventIds.has(event.id || event._id)"
                            @toggleSave="handleToggleSave"
                            class="shadow-xl"
                        />
                    </div>
                </div>
            </section>

            <!-- Top Vendors -->
            <section>
                 <div class="flex items-center space-x-3 mb-12">
                    <div class="w-2 h-10 bg-blue-500 rounded-full"></div>
                    <h2 class="text-4xl font-black text-gray-900 tracking-tight">Our Premium Vendors</h2>
                </div>
                 <div class="grid grid-cols-2 lg:grid-cols-4 gap-8">
                     <div v-for="i in 4" :key="'vend-'+i" class="bg-gray-50 rounded-[3rem] p-10 border border-transparent hover:bg-white hover:shadow-2xl hover:border-blue-100 transition-all cursor-pointer group flex flex-col items-center text-center">
                         <div class="w-24 h-24 bg-white rounded-[2rem] mb-6 flex items-center justify-center shadow-sm group-hover:bg-blue-50 transition-colors">
                             <svg class="w-12 h-12 text-gray-200 group-hover:text-blue-200" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd"></path></svg>
                         </div>
                         <h3 class="text-2xl font-black text-gray-900 leading-tight">Elite Partner</h3>
                         <p class="text-xs font-black text-gray-400 mt-2 uppercase tracking-widest">Premium Service</p>
                         <div class="flex mt-6 space-x-1.5">
                             <div v-for="star in 5" :key="star" class="w-3 h-3 rounded-full bg-orange-400 shadow-sm"></div>
                         </div>
                     </div>
                 </div>
            </section>

        </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { format, addDays, startOfWeek, endOfWeek, isSameDay, isWithinInterval, parseISO } from 'date-fns' 
import MapView from '../components/MapView.vue'
import EventCard from '../components/EventCard.vue'
import Filters from '../components/Filters.vue'
import Recommendations from '../components/Recommendations.vue'
import api from '../utils/api'

// Core State
const router = useRouter()
const allEvents = ref([])
const recommendations = ref([])
const vendorInterests = ref([])
const selectedCluster = ref(null)
const showSavedOnly = ref(false)
const savedEventIds = ref(new Set())

const filters = ref({
    keyword: '',
    category: '',
    radius: 10,
    selectedInterests: [],
    dateRange: '' 
})

// Date Options
const today = new Date()
const dateOptions = computed(() => [
    { label: 'Today', value: 'today', subtext: format(today, 'MMM d') },
    { label: 'Tomorrow', value: 'tomorrow', subtext: format(addDays(today, 1), 'MMM d') },
    { label: 'This Weekend', value: 'weekend', subtext: 'Fri - Sun' },
    { label: 'This Week', value: 'week', subtext: 'Mon - Sun' },
    { label: 'Upcoming', value: 'custom', subtext: 'Next 30 Days' }
])

// --- Methods ---

const handleDateSelect = async (val) => {
    if (filters.value.dateRange === val) {
        filters.value.dateRange = '' 
    } else {
        filters.value.dateRange = val
        window.scrollTo({ top: 0, behavior: 'smooth' })
    }
}

const scrollToResults = () => {
    const el = document.getElementById('results-grid')
    if (el) {
        const offset = 120
        const bodyRect = document.body.getBoundingClientRect().top
        const elementRect = el.getBoundingClientRect().top
        const elementPosition = elementRect - bodyRect
        const offsetPosition = elementPosition - offset

        window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
        })
    }
}

const resetFilters = () => {
    filters.value = {
        keyword: '',
        category: '',
        radius: 10,
        selectedInterests: [],
        dateRange: ''
    }
    showSavedOnly.value = false
    selectedCluster.value = null
}

const logout = () => {
    localStorage.removeItem('token')
    savedEventIds.value.clear()
    router.push('/')
}

const handleClusterSelect = (clusterName) => {
    selectedCluster.value = clusterName
    fetchRecommendations()
    window.scrollTo({ top: 0, behavior: 'smooth' })
}

const handleFilterChange = (newFilters) => {
    filters.value = { ...filters.value, ...newFilters }
    fetchRecommendations()
}

const handleToggleSave = (event) => {
    const id = event.id || event._id
    if (savedEventIds.value.has(id)) {
        savedEventIds.value.delete(id)
    } else {
        savedEventIds.value.add(id)
    }
}

// --- Computed ---

const popularEvents = computed(() => {
    let events = [...allEvents.value]
    events.sort((a, b) => (b.interested_count || 0) - (a.interested_count || 0))
    return events.slice(0, 10)
})

const categories = computed(() => {
    const cats = new Set(allEvents.value
        .map(e => e.category ? e.category.trim() : '')
        .filter(c => c && !c.toLowerCase().includes('all categories') && c.length <= 50)
    )
    return Array.from(cats).sort()
})

const normalizeZone = (zone) => {
    if (!zone) return 'Bengaluru'
    const z = zone.toLowerCase()
    if (z.includes('indiranagar')) return 'Indiranagar'
    if (z.includes('koramangala')) return 'Koramangala'
    if (z.includes('whitefield')) return 'Whitefield'
    if (z.includes('hsr')) return 'HSR Layout'
    if (z.includes('jayanagar')) return 'Jayanagar'
    if (z.includes('mg road')) return 'MG Road'
    return zone 
}

const filteredEvents = computed(() => {
    let events = allEvents.value
    if (selectedCluster.value) {
        events = events.filter(e => normalizeZone(e.main_zone) === selectedCluster.value)
    }
    if (filters.value.category) {
        events = events.filter(e => e.category === filters.value.category)
    }
    if (filters.value.keyword) {
        const k = filters.value.keyword.toLowerCase()
        events = events.filter(e => e.title.toLowerCase().includes(k) || e.description.toLowerCase().includes(k))
    }
    if (showSavedOnly.value) {
        events = events.filter(e => savedEventIds.value.has(e.id || e._id))
    }
    if (filters.value.dateRange) {
        const type = filters.value.dateRange
        const now = new Date()
        events = events.filter(e => {
            const eDate = parseISO(e.start_time)
            if (type === 'today') return isSameDay(eDate, now)
            if (type === 'tomorrow') return isSameDay(eDate, addDays(now, 1))
            if (type === 'weekend') {
                const day = now.getDay()
                const diffNextFri = (5 - day + 7) % 7
                const nextFri = addDays(now, diffNextFri)
                const nextSun = addDays(nextFri, 2)
                return isWithinInterval(eDate, { start: nextFri, end: nextSun })
            }
            if (type === 'week') {
                return isWithinInterval(eDate, { start: startOfWeek(now), end: endOfWeek(now) })
            }
            return true
        })
    }
    return events
})

const displayedEvents = computed(() => {
    return filteredEvents.value.map(e => ({
        ...e,
        description: e.description ? e.description.replace(/All\?ref=cityhome_viewall/g, 'General All Categories') : e.description
    }))
})

const fetchData = async () => {
    try {
        const [eventsRes, vendorRes] = await Promise.all([
            api.getEvents(),
            api.getVendorProfile()
        ])
        allEvents.value = eventsRes.data
        vendorInterests.value = vendorRes.data.interests || []
        savedEventIds.value = new Set(vendorRes.data.saved_events || [])
    } catch (e) {
        console.error("Failed to fetch data", e)
    }
}

const fetchRecommendations = async () => {
    try {
        const res = await api.getRecommendations()
        let recs = res.data
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

<style scoped>
.hide-scrollbar::-webkit-scrollbar {
    display: none;
}
.hide-scrollbar {
    -ms-overflow-style: none;
    scrollbar-width: none;
}
</style>
