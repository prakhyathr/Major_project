<template>
  <div class="bg-white p-4 rounded-xl shadow-sm border border-gray-100 mb-6">
    <div class="grid grid-cols-1 md:grid-cols-12 gap-4 items-end">
        
        <!-- Search -->
        <div class="md:col-span-4">
            <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">Search</label>
            <div class="relative">
                <input 
                    type="text" 
                    v-model="filters.keyword"
                    placeholder="Search events..." 
                    class="w-full pl-9 pr-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-orange-200 focus:border-orange-500 outline-none transition-all"
                >
                <svg class="w-4 h-4 text-gray-400 absolute left-3 top-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
            </div>
        </div>

        <!-- Categories -->
        <div class="md:col-span-4">
             <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">Category</label>
             <select 
                v-model="filters.category" 
                class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-orange-200 focus:border-orange-500 outline-none bg-white"
             >
                 <option value="">All Categories</option>
                 <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
             </select>
        </div>

        <!-- Radius -->
        <div class="md:col-span-4">
            <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1 flex justify-between">
                <span>Distance</span>
                <span class="text-orange-600">{{ filters.radius }} km</span>
            </label>
            <input 
                type="range" 
                min="1" 
                max="20" 
                v-model.number="filters.radius"
                class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-orange-500"
            >
        </div>
        <!-- Search Button -->
        <div class="md:col-span-12 flex justify-end mt-4">
            <button 
                @click="emitChange"
                class="bg-orange-500 text-white px-6 py-2 rounded-lg font-bold hover:bg-orange-600 transition-colors shadow-md flex items-center"
            >
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                Search Events
            </button>
        </div>
    </div>
    
    <!-- Interests Tags (Optional) -->
    <div class="mt-4 pt-4 border-t border-gray-100" v-if="interests.length">
        <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Your Interests</label>
        <div class="flex flex-wrap gap-2">
            <button 
                v-for="interest in interests" 
                :key="interest"
                @click="toggleInterest(interest)"
                class="px-3 py-1 rounded-full text-xs font-medium transition-colors border"
                :class="[
                    filters.selectedInterests.includes(interest)
                    ? 'bg-orange-100 text-orange-700 border-orange-200'
                    : 'bg-gray-50 text-gray-600 border-gray-200 hover:bg-gray-100'
                ]"
            >
                {{ interest }}
            </button>
        </div>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'

const props = defineProps({
  categories: {
    type: Array,
    default: () => []
  },
  interests: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['change'])

const filters = reactive({
  keyword: '',
  category: '',
  radius: 10,
  selectedInterests: []
})

const toggleInterest = (interest) => {
    if (filters.selectedInterests.includes(interest)) {
        filters.selectedInterests = filters.selectedInterests.filter(i => i !== interest)
    } else {
        filters.selectedInterests.push(interest)
    }
    // Auto-update on interest toggle? User asked for Search button.
    // Let's keep it manual for consistency with the request.
}

const emitChange = () => {
  emit('change', { ...filters })
}
</script>
