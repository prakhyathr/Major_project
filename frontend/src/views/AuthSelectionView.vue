<template>
  <div class="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
        Welcome to BLR Event Discovery
      </h2>
      <p class="mt-2 text-center text-sm text-gray-600">
        Connect with the best events in Bengaluru
      </p>
    </div>

    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
      <div class="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10 space-y-6">
        
        <div>
          <h3 class="text-lg leading-6 font-medium text-gray-900 text-center mb-4">
            New to the platform?
          </h3>
          <router-link 
            to="/register" 
            class="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
          >
            Register as a Vendor
          </router-link>
        </div>

        <div class="relative">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-gray-300"></div>
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-2 bg-white text-gray-500">
              Or
            </span>
          </div>
        </div>

        <div>
          <h3 class="text-lg leading-6 font-medium text-gray-900 text-center mb-4">
            Already have an account?
          </h3>
          <router-link 
            to="/login" 
            class="w-full flex justify-center py-3 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
          >
            Login
          </router-link>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
</script>
