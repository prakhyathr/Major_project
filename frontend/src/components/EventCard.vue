<template>
  <div class="bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow duration-200 border border-gray-100 overflow-hidden flex flex-col h-full">
    <!-- Header / Image Placeholder -->
    <div class="h-32 bg-gray-100 relative">
        <!-- Category Badge -->
        <span class="absolute top-3 right-3 bg-orange-500 text-white text-xs font-bold px-2 py-1 rounded-full uppercase tracking-wide">
            {{ event.category || 'Event' }}
        </span>
        <!-- Placeholder Pattern -->
        <div class="w-full h-full flex items-center justify-center text-gray-300">
            <svg class="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
        </div>
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
            @click.stop="saveEvent"
            class="flex-1 border border-gray-300 text-gray-700 py-2 rounded-lg text-sm font-medium hover:bg-gray-50 transition-colors flex items-center justify-center"
        >
            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"></path></svg>
            Save
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
const props = defineProps({
  event: {
    type: Object,
    required: true
  }
})

const saveEvent = () => {
    // TODO: Implement save functionality
    alert('Event saved!')
}

const formatDate = (dateString) => {
  if (!dateString) return 'TBD'
  return new Date(dateString).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' })
}
</script>
