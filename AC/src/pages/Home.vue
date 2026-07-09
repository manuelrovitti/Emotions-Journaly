<script setup>
    import { ref } from "vue";

    import EmotionForm from "../components/EmotionForm.vue";
    import Dashboard from "../components/Dashboard.vue";
    import HeroCarousel from "../components/HeroCarousel.vue";
    import { useSiteStore } from '../stores/HomeStore'

    const store = useSiteStore()

    const currentUser = ref({
      name: "Mario",
      surname: "Rossi",
    });

    /* =========================
      HANDLER
    ========================= */
    function handleAnalyze(data) {
      console.log("Analyze data:", data);

      currentUser.value.name = data.name;
      currentUser.value.surname = data.surname;
    }
</script>

<template>
  <div class="min-h-screen flex flex-col ">

    <HeroCarousel />

    <div class="flex-1 bg-cover bg-center p-6"
      :style="{ backgroundImage: `url(${store.bgImage})` }"
    >
      <div class="mx-auto w-full max-w-7xl px-6 py-6 space-y-6">

        <EmotionForm @analyze="handleAnalyze" />

        <Dashboard
          :name="currentUser.name"
          :surname="currentUser.surname"
        />

      </div>
    </div>
  </div>
</template>