<template>
  <div class="bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow duration-200 border border-gray-100 overflow-hidden flex flex-col h-full">
    <!-- Header / Image Placeholder -->
    <!-- Header / Image -->
    <div class="h-32 bg-gray-100 relative overflow-hidden group-hover:opacity-90 transition-opacity">
        <!-- Category Badge -->
        <span class="absolute top-3 right-3 bg-orange-500 text-white text-xs font-bold px-2 py-1 rounded-full uppercase tracking-wide z-10 shadow-sm">
            {{ event.category || 'Event' }}
        </span>
        
        <!-- Image -->
        <img 
            :src="categoryImage" 
            :alt="event.category"
            class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
            @error="handleImageError"
        >
    </div>

    <div class="p-4 flex-grow flex flex-col">
      <!-- Title -->
      <h3 class="text-lg font-bold text-gray-800 mb-1 line-clamp-1" :title="event.title">{{ event.title }}</h3>
      
      <!-- Location -->
      <div class="flex items-center text-gray-500 text-sm mb-3">
        <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
        <span class="truncate">{{ event.main_zone || 'Bengaluru' }}</span>
      </div>

      <!-- Description -->
      <p class="text-gray-600 text-sm mb-4 line-clamp-2 flex-grow">
        {{ event.description }}
      </p>

      <!-- Meta Info -->
      <div class="flex items-center justify-between text-sm text-gray-500 mb-4">
        <div class="flex items-center">
            <svg class="w-4 h-4 mr-1 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
            <span>{{ formatDate(event.start_time) }}</span>
        </div>
        <div class="flex items-center">
             <svg class="w-4 h-4 mr-1 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
             <span>{{ Math.floor(Math.random() * 500) + 50 }}</span>
        </div>
      </div>

      <!-- Price (Mock) -->
      <div class="text-gray-700 font-semibold text-sm mb-4">
        ₹{{ Math.floor(Math.random() * 2000) + 500 }} - ₹{{ Math.floor(Math.random() * 5000) + 2500 }}
      </div>

      <!-- Buttons -->
      <div class="flex space-x-2 mt-auto">
        <button 
            @click.stop="toggleSave"
            :disabled="isLoading"
            class="flex-1 border py-2 rounded-lg text-sm font-medium transition-colors flex items-center justify-center"
            :class="isSaved ? 'bg-gray-900 text-white border-gray-900 hover:bg-gray-800' : 'border-gray-300 text-gray-700 hover:bg-gray-50'"
        >
            <svg v-if="isSaved" class="w-4 h-4 mr-1 text-orange-500" fill="currentColor" viewBox="0 0 24 24"><path d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"></path></svg>
            <svg v-else class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"></path></svg>
            {{ isSaved ? 'Saved' : 'Save' }}
        </button>
        <a 
            :href="event.source_url" 
            target="_blank"
            rel="noopener noreferrer"
            class="flex-1 bg-orange-500 text-white py-2 rounded-lg text-sm font-medium hover:bg-orange-600 transition-colors flex items-center justify-center shadow-sm hover:shadow"
        >
            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
            View
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import api from '../utils/api'
import { ref, computed } from 'vue'

const props = defineProps({
  event: {
    type: Object,
    required: true
  },
  isSaved: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['toggleSave'])
const isLoading = ref(false)

const toggleSave = async () => {
    isLoading.value = true
    try {
        if (props.isSaved) {
            await api.unsaveEvent(props.event.id || props.event._id)
        } else {
            await api.saveEvent(props.event.id || props.event._id)
        }
        emit('toggleSave', props.event)
    } catch (e) {
        console.error("Failed to toggle save", e)
        alert("Failed to save/unsave event")
    } finally {
        isLoading.value = false
    }
}

const formatDate = (dateString) => {
  if (!dateString) return 'TBD'
  return new Date(dateString).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' })
}

const categoryImage = computed(() => {
    if (!props.event.category) return '/assets/categories/business.png' // Default
    
    const cat = props.event.category.toLowerCase()
    
    // Exact/Strong Matches First
    if (cat.includes('workshop') || cat.includes('training') || cat.includes('class')) return '/assets/categories/workshops.png'
    if (cat.includes('party') || cat.includes('nightlife') || cat.includes('dj')) return '/assets/categories/parties.png'
    if (cat.includes('entertainment') || cat.includes('show') || cat.includes('magic')) return '/assets/categories/entertainment.png'
    
    // Broad Matches
    if (cat.includes('business') || cat.includes('tech') || cat.includes('corporate')) return '/assets/categories/business.png'
    if (cat.includes('comedy') || cat.includes('standup')) return '/assets/categories/comedy.png'
    if (cat.includes('music') || cat.includes('concert') || cat.includes('live')) return '/assets/categories/music.png'
    if (cat.includes('sport') || cat.includes('fitness')) return '/assets/categories/sports.png'
    
    return '/assets/categories/entertainment.png' // Generic Fallback
})

const handleImageError = (e) => {
    // Fallback to business image if specific category fails
    if (e.target.src.includes('business.png')) return // Stop infinite loop
    e.target.src = '/assets/categories/business.png'
}
</script>
