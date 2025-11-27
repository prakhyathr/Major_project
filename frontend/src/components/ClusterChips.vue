<template>
  <div class="flex space-x-2 overflow-x-auto pb-2 scrollbar-hide">
    <button 
      v-for="cluster in clusters" 
      :key="cluster.name"
      @click="$emit('select', cluster)"
      class="whitespace-nowrap px-4 py-1.5 rounded-full text-sm font-medium transition-colors border"
      :class="[
        selectedCluster === cluster.name 
          ? 'bg-teal-600 text-white border-teal-600' 
          : 'bg-teal-100 text-teal-800 border-teal-200 hover:bg-teal-200'
      ]"
    >
      {{ cluster.name }} ({{ cluster.count }})
    </button>
  </div>
</template>

<script setup>
defineProps({
  clusters: {
    type: Array,
    default: () => []
  },
  selectedCluster: {
    type: String,
    default: null
  }
})

defineEmits(['select'])
</script>

<style scoped>
.scrollbar-hide::-webkit-scrollbar {
    display: none;
}
.scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
}
</style>
