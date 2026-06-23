
<script setup>
    import { ref } from "vue";

    import EmotionForm from "../components/EmotionForm.vue";
    import Dashboard from "../components/Dashboard.vue";
    import HeroCarousel from "../components/HeroCarousel.vue";


    function handleAnalyze(data) {
    console.log(data);

    // qui andrà la chiamata al backend
    }
</script>

<template>
  <div class="min-h-screen bg-slate-100">
    
    <HeroCarousel />

    <div class="mx-auto w-full max-w-7xl px-6 py-6 space-y-6">

      <EmotionForm
        @analyze="handleAnalyze"
      />

      <Dashboard
        :history="history"
        :total-analyses="24"
        dominant-emotion="😰"
        :stress-percentage="40"
        :sadness-percentage="20"
      />

    </div>

  </div>
</template>