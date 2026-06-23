
<script setup>
    import { ref } from "vue";

    import EmotionForm from "../components/EmotionForm.vue";
    import Dashboard from "../components/Dashboard.vue";


    function handleAnalyze(data) {
    console.log(data);

    // qui andrà la chiamata al backend
    }
</script>

<template>
  <div class="min-h-screen bg-slate-100 p-6">
    <div class="mx-auto max-w-7xl space-y-2">

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