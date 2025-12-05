<template>
  <div class="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <img src="/assets/logo.jpg" alt="BLR Hive Logo" class="mx-auto h-16 w-auto mb-4">
      <h2 class="mt-6 text-center text-3xl font-bold leading-9 tracking-tight text-gray-900">Vendor Registration</h2>
      <p class="mt-2 text-center text-sm text-gray-600">
        Tell us about your business to get personalized event recommendations.
      </p>
    </div>

    <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-md">
      <form class="space-y-6" @submit.prevent="handleRegister">
        
        <!-- Step 1: Account Info -->
        <div class="bg-white p-6 shadow rounded-lg space-y-6">
            <h3 class="text-lg font-medium text-gray-900">Account Details</h3>
            <div>
            <label for="email" class="block text-sm font-medium leading-6 text-gray-900">Email address</label>
            <div class="mt-2">
                <input id="email" v-model="email" name="email" type="email" autocomplete="email" required class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary sm:text-sm sm:leading-6" />
            </div>
            </div>

            <div>
            <label for="password" class="block text-sm font-medium leading-6 text-gray-900">Password</label>
            <div class="mt-2">
                <input id="password" v-model="password" name="password" type="password" autocomplete="new-password" required class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary sm:text-sm sm:leading-6" />
            </div>
            </div>
        </div>

        <!-- Step 2: Business Info -->
        <div class="bg-white p-6 shadow rounded-lg space-y-6">
            <h3 class="text-lg font-medium text-gray-900">Business Profile</h3>
            
            <div>
            <label for="business-name" class="block text-sm font-medium leading-6 text-gray-900">Business Name</label>
            <div class="mt-2">
                <input id="business-name" v-model="businessName" name="business-name" type="text" required class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary sm:text-sm sm:leading-6" />
            </div>
            </div>

            <div>
            <label for="category" class="block text-sm font-medium leading-6 text-gray-900">Business Category</label>
            <div class="mt-2">
                <select id="category" v-model="category" name="category" required class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-primary sm:text-sm sm:leading-6">
                    <option value="" disabled>Select a category</option>
                    <option value="Food & Beverage">Food & Beverage</option>
                    <option value="Handicrafts">Handicrafts</option>
                    <option value="Apparel">Apparel</option>
                    <option value="Tech & Gadgets">Tech & Gadgets</option>
                    <option value="Services">Services</option>
                </select>
            </div>
            </div>

            <div>
            <label class="block text-sm font-medium leading-6 text-gray-900">Interests (Select all that apply)</label>
            <div class="mt-2 space-y-2">
                <div v-for="interest in availableInterests" :key="interest" class="flex items-center">
                    <input :id="interest" :value="interest" v-model="selectedInterests" type="checkbox" class="h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary" />
                    <label :for="interest" class="ml-3 block text-sm leading-6 text-gray-900">{{ interest }}</label>
                </div>
            </div>
            </div>

            <div>
             <label for="radius" class="block text-sm font-medium leading-6 text-gray-900">Travel Radius (km)</label>
             <div class="mt-2">
                <input id="radius" v-model="travelRadius" type="number" min="1" max="100" class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary sm:text-sm sm:leading-6" />
             </div>
            </div>
        </div>

        <div>
          <button type="submit" class="flex w-full justify-center rounded-md bg-primary px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary">Complete Registration</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const businessName = ref('')
const category = ref('')
const selectedInterests = ref([])
const travelRadius = ref(10)
const router = useRouter()

const availableInterests = [
    "High Footfall",
    "Corporate Crowd",
    "Family Friendly",
    "Music Festivals",
    "Tech Conferences",
    "Outdoor Markets"
]

const handleRegister = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/v1/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: email.value,
        password: password.value,
        business_name: businessName.value,
        category: category.value,
        is_vendor: true
      }),
    })
    
    if (!response.ok) {
      const data = await response.json()
      throw new Error(data.detail || 'Registration failed')
    }

    alert('Registration successful! Please login.')
    router.push('/login')

  } catch (error) {
    console.error(error)
    alert(error.message)
  }
}
</script>
