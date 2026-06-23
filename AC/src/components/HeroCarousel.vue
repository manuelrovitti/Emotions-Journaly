<script setup>
    import { ref, onMounted, onUnmounted } from 'vue'
    import { useSiteStore } from '../stores/HomeStore'

    const store = useSiteStore()

    const current = ref(0)

    let interval

    onMounted(() => {
    interval = setInterval(() => {
        current.value =
        (current.value + 1) % store.heroImages.length
    }, 4000)
    })

    onUnmounted(() => {
    clearInterval(interval)
    })
</script>

<template>
    <p class="text-white absolute top-0">
        {{ store.heroImages }}
    </p>
  <section class="relative h-screen">

    <img
      :src="store.heroImages[current]"
      class="absolute inset-0 w-full h-full object-cover"
    >

    <div class="absolute inset-0 bg-black/40"></div>

    <div
      class="relative z-10 flex h-full items-center justify-center"
    >
      <div class="text-center text-white">

        <h1 class="text-6xl font-bold mb-6 text-green-900">
          Emotional <span class="text-red-800">Journal</span>
        </h1>

        <p class="text-xl mb-8">
          Keep your emotions journal up to date.
        </p>
      </div>
    </div>

  </section>
</template>