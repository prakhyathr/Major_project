<template>
  <div class="min-h-screen bg-gray-50 flex flex-col items-center py-12 px-4 sm:px-6 lg:px-8">
    
    <!-- Profile Card -->
    <div class="max-w-3xl w-full bg-white rounded-2xl shadow-xl overflow-hidden transition-all duration-300 hover:shadow-2xl">
      
      <!-- Header / Banner -->
      <div class="bg-gradient-to-r from-orange-500 to-red-600 h-32 relative flex items-center justify-center overflow-hidden">
          <!-- Background Pattern or existing content -->
          <img src="/assets/logo.jpg" alt="BLR Hive" class="h-24 w-auto opacity-20 absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 mix-blend-overlay">
          
          <button @click="$router.push('/discover')" class="absolute top-4 left-4 bg-white/20 hover:bg-white/30 text-white px-3 py-1 rounded-full text-sm font-medium backdrop-blur-sm transition-colors flex items-center z-10">
             <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
             Back to Dashboard
          </button>
      </div>

      <div class="px-8 pb-8">
          
          <!-- Avatar & Identity -->
          <div class="relative -mt-16 mb-6 flex flex-col items-center">
              <div class="w-32 h-32 rounded-full border-4 border-white bg-gray-900 text-white flex items-center justify-center text-4xl font-bold shadow-lg">
                  {{ getInitials(profile.business_name) }}
              </div>
              <h1 class="mt-4 text-3xl font-bold text-gray-900">{{ profile.business_name || 'Loading...' }}</h1>
              <p class="text-gray-500">{{ profile.email }}</p>
              <span class="mt-2 px-3 py-1 bg-orange-100 text-orange-800 rounded-full text-xs font-semibold tracking-wide uppercase">
                  {{ profile.category || 'Vendor' }}
              </span>
          </div>

          <!-- Divider -->
          <div class="border-t border-gray-100 my-8"></div>

          <!-- Interests Section -->
          <div class="space-y-6">
              <div class="text-center sm:text-left">
                  <h2 class="text-xl font-bold text-gray-900">Your Interests</h2>
                  <p class="text-sm text-gray-500 mt-1">
                      Update your preferences to get better event recommendations tailored to your business.
                  </p>
              </div>

              <!-- Checkboxes Grid -->
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div 
                    v-for="interest in availableInterests" 
                    :key="interest"
                    class="relative flex items-center p-4 rounded-xl border-2 transition-all cursor-pointer"
                    :class="selectedInterests.includes(interest) ? 'border-orange-500 bg-orange-50' : 'border-gray-200 hover:border-orange-200'"
                    @click="toggleInterest(interest)"
                  >
                      <div class="flex-shrink-0 h-5 w-5 flex items-center justify-center rounded border"
                           :class="selectedInterests.includes(interest) ? 'bg-orange-500 border-orange-500' : 'border-gray-300 bg-white'"
                      >
                          <svg v-if="selectedInterests.includes(interest)" class="w-3.5 h-3.5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"></path></svg>
                      </div>
                      <span class="ml-3 font-medium text-gray-900 select-none">{{ interest }}</span>
                  </div>
              </div>
              
              <!-- Action Button -->
              <div class="mt-8 flex justify-end">
                   <button 
                      @click="updateProfile" 
                      :disabled="isSaving"
                      class="w-full sm:w-auto px-8 py-3 bg-gray-900 text-white rounded-xl font-bold hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-900 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:-translate-y-1 shadow-md"
                   >
                      <span v-if="isSaving" class="flex items-center">
                          <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                          Saving Changes...
                      </span>
                      <span v-else>Update Profile</span>
                   </button>
              </div>

          </div>

          <!-- Saved Events Section -->
          <div class="border-t border-gray-100 my-8"></div>
          
          <div>
              <h2 class="text-xl font-bold text-gray-900 mb-6 font-display">Saved Events</h2>
              
              <div v-if="loadingSaved" class="text-center py-12">
                   <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-orange-500 mx-auto"></div>
              </div>
              
              <div v-else-if="savedEvents.length === 0" class="bg-gray-50 rounded-xl p-8 text-center">
                  <p class="text-gray-500">You haven't saved any events yet.</p>
                  <router-link to="/discover" class="text-orange-600 font-medium hover:text-orange-700 mt-2 inline-block">
                      Browse Events
                  </router-link>
              </div>
              
              <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <EventCard 
                      v-for="event in savedEvents" 
                      :key="event.id || event._id" 
                      :event="event"
                      :isSaved="true" 
                      @toggleSave="handleUnsave"
                  />
              </div>
          </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../utils/api'
import EventCard from '../components/EventCard.vue'

const profile = ref({})
const selectedInterests = ref([])
const isSaving = ref(false)
const savedEvents = ref([])
const loadingSaved = ref(false)
const router = useRouter()

const availableInterests = [
    "High Footfall",
    "Corporate Crowd",
    "Family Friendly",
    "Music Festivals",
    "Tech Conferences",
    "Outdoor Markets"
]

const getInitials = (name) => {
    if (!name) return 'MB' // My Business
    return name.split(' ').map(n => n[0]).slice(0, 2).join('').toUpperCase()
}

const toggleInterest = (interest) => {
    if (selectedInterests.value.includes(interest)) {
        selectedInterests.value = selectedInterests.value.filter(i => i !== interest)
    } else {
        selectedInterests.value.push(interest)
    }
}

const fetchProfile = async () => {
    try {
        const res = await api.getVendorProfile()
        profile.value = res.data
        selectedInterests.value = res.data.interests || []
    } catch (e) {
        console.error("Failed to load profile", e)
        alert("Failed to load profile data.")
    }
}

const updateProfile = async () => {
    isSaving.value = true
    try {
        const res = await api.updateVendorProfile({
            interests: selectedInterests.value
        })
        profile.value = res.data // Update local data with server response
        alert("Profile updated successfully! Recommendations will be refreshed.")
    } catch (e) {
        console.error("Failed to update profile", e)
        alert("Failed to update profile.")
    } finally {
        isSaving.value = false
    }
}

const fetchSavedEvents = async () => {
    loadingSaved.value = true
    try {
        const res = await api.getSavedEvents()
        savedEvents.value = res.data
    } catch (e) {
        console.error("Failed to load saved events", e)
    } finally {
        loadingSaved.value = false
    }
}

const handleUnsave = (event) => {
    // Remove from local list immediately
    const id = event.id || event._id
    savedEvents.value = savedEvents.value.filter(e => (e.id || e._id) !== id)
}

onMounted(() => {
    fetchProfile()
    fetchSavedEvents()
})
</script>
