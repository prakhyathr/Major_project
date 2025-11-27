<template>
  <div class="mb-8 animate-fade-in">
    <div class="flex items-center justify-between mb-4">
        <h2 class="text-xl font-bold text-gray-800 flex items-center">
            <span class="bg-gradient-to-r from-orange-500 to-red-500 text-transparent bg-clip-text">Top 5 Recommended Events</span>
            <span class="ml-3 px-2 py-0.5 bg-orange-100 text-orange-700 text-xs font-bold uppercase rounded-md tracking-wider border border-orange-200">AI Powered</span>
        </h2>
    </div>
    
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        <div v-for="event in events" :key="event.id" class="transform hover:-translate-y-1 transition-transform duration-200">
            <EventCard :event="event" class="h-full border-orange-200 shadow-orange-100/50" />
        </div>
    </div>
    
    <div class="mt-6 text-center border-b border-gray-200 pb-6">
        <button 
            @click="$emit('viewAll')"
            class="text-gray-500 hover:text-orange-600 font-medium text-sm flex items-center justify-center mx-auto transition-colors"
        >
            View All Events
            <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
        </button>
    </div>
  </div>
</template>

<script setup>
import EventCard from './EventCard.vue'

defineProps({
  events: {
    type: Array,
    required: true
  }
})

defineEmits(['viewAll'])
</script>

<style scoped>
.animate-fade-in {
    animation: fadeIn 0.5s ease-out;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>
