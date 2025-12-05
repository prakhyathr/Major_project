<template>
  <div class="flex min-h-screen bg-white">
    <!-- Left Side: Hero Image -->
    <div class="hidden lg:flex lg:w-1/2 relative bg-gray-900">
      <img src="https://images.unsplash.com/photo-1545127398-14699f82751e?q=80&w=2548&auto=format&fit=crop" 
           alt="Bengaluru Event" 
           class="absolute inset-0 w-full h-full object-cover opacity-60">
      <div class="relative z-10 flex flex-col justify-center px-12 text-white">
        <h1 class="text-5xl font-bold mb-6 leading-tight">Your Gateway to <br>Bengaluru's Lifestyle</h1>
        <p class="text-xl text-gray-200 max-w-lg">
            From underground music gigs to tech conferences and flea markets — find opportunities that match your business vibe.
        </p>
      </div>
    </div>

    <!-- Right Side: Action Buttons -->
    <div class="flex-1 flex flex-col justify-center px-4 sm:px-6 lg:px-20 xl:px-24 relative">
      <!-- Logo (Top Left) -->
      <div class="absolute top-8 left-8 sm:left-12">
          <img src="/assets/logo.jpg" alt="BLR Hive Logo" class="h-24 w-auto">
      </div>

      <div class="mx-auto w-full max-w-sm lg:w-96 text-center lg:text-left">
        
        <div class="mb-10 text-center lg:text-left">
            <h2 class="text-4xl font-extrabold text-gray-900 mb-2">Get Started</h2>
            <p class="text-gray-500">Choose how you want to continue</p>
        </div>

        <div class="space-y-4">
            <!-- Register Button -->
            <router-link 
                to="/register" 
                class="group relative w-full flex justify-center py-4 px-4 border border-transparent rounded-xl text-sm font-bold text-white bg-orange-600 hover:bg-orange-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500 shadow-lg hover:shadow-xl transition-all transform hover:-translate-y-1"
            >
                <div class="flex items-center">
                    <span>Create New Account</span>
                    <svg class="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path></svg>
                </div>
            </router-link>

            <!-- Divider -->
            <div class="relative py-4">
                <div class="absolute inset-0 flex items-center">
                    <div class="w-full border-t border-gray-200"></div>
                </div>
                <div class="relative flex justify-center text-sm">
                    <span class="px-4 bg-white text-gray-500 font-medium">Already a member?</span>
                </div>
            </div>

            <!-- Login Button -->
            <router-link 
                to="/login" 
                class="w-full flex justify-center py-4 px-4 border-2 border-gray-200 rounded-xl text-sm font-bold text-gray-700 bg-white hover:bg-gray-50 hover:border-gray-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transition-all"
            >
                Log In
            </router-link>
        </div>

        <p class="mt-8 text-center text-xs text-gray-400">
            By continuing, you agree to our Terms of Service and Privacy Policy.
        </p>

      </div>
    </div>
  </div>
</template>

<script setup>
</script>
