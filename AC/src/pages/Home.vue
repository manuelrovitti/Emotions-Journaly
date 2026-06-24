<script setup>
    import { ref } from "vue";

    import EmotionForm from "../components/EmotionForm.vue";
    import Dashboard from "../components/Dashboard.vue";
    import HeroCarousel from "../components/HeroCarousel.vue";


    const currentUser = ref({
      name: "Manuel",
      surname: "Rovitti",
    });

    /* =========================
      HANDLER
    ========================= */
    function handleAnalyze(data) {
      console.log(data);

      currentUser.value.name = data.name;
      currentUser.value.surname = data.surname;
    }
</script>

<template>
  <div class="min-h-screen bg-slate-100">

    <HeroCarousel />

    <div class="mx-auto w-full max-w-7xl px-6 py-6 space-y-6">

      <EmotionForm @analyze="handleAnalyze" />

      <Dashboard
        :name="currentUser.name"
        :surname="currentUser.surname"
      />

    </div>

  </div>
</template>