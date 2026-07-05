<script setup>
import { ref } from 'vue'

const isMenuOpen = ref(false)

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

const navLinks = [
  { name: 'Home', href: '/' },
  { name: 'Journaly', href: '/journaly' },
  { name: 'About', href: '/about' },
  { name: 'Analysis', href: '/analysis' },
]
</script>

<template>
  <!-- NAVBAR FULL WIDTH -->
  <nav class="sticky top-0 z-50 w-screen bg-blue-200 backdrop-blur-xl border-b border-red-900/10">

    <!-- FULL WIDTH CONTENT-->
    <div class="w-full px-6 lg:px-10">

      <div class="flex items-center justify-between h-20">

        <!-- LOGO-->
        <router-link to="/" class="flex items-center gap-3">
          <img
            src="../assets/diario.png"
            alt="Logo"
            class="h-11 md:h-12 w-auto"
          />

          <span class="text-xl md:text-2xl font-semibold tracking-wide text-green-900 whitespace-nowrap">
            Emotional <span class="text-red-800"> Journal</span>
          </span>
        </router-link>

        <!-- DESKTOP NAV -->
        <div class="hidden md:flex items-center gap-10">
          <a
            v-for="link in navLinks"
            :key="link.name"
            :href="link.href"
            class="text-base font-medium text-black hover:text-red-900 transition-colors duration-200"
          >
            {{ link.name }}
          </a>
        </div>

        <!-- MOBILE BUTTON -->
        <button
          @click="toggleMenu"
          class="md:hidden p-2 rounded-lg text-gray-600 hover:bg-gray-100 transition"
        >
          <svg v-if="!isMenuOpen" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
              d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
          </svg>

          <svg v-else class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
              d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

      </div>
    </div>

    <!-- MOBILE MENU -->
    <div
      v-show="isMenuOpen"
      class="md:hidden border-t border-gray-200 bg-white/90 backdrop-blur-xl w-full"
    >
      <div class="px-6 py-4 space-y-2">
        <a
          v-for="link in navLinks"
          :key="link.name"
          :href="link.href"
          @click="isMenuOpen = false"
          class="block text-base font-medium text-black py-2 hover:text-red-900 transition"
        >
          {{ link.name }}
        </a>
      </div>
    </div>

  </nav>
</template>