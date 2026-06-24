<template>
  <div class="w-full max-w-6xl mx-auto">

    <div class="rounded-2xl bg-white p-6 shadow-sm">
      <h2 class="mb-2 text-2xl font-semibold">
        Dashboard di {{ props.name }} {{ props.surname }}
      </h2>

      <div class="grid grid-cols-2 gap-4">

        <!-- TOTALI -->
        <div class="rounded-xl bg-indigo-50 p-4">
          <p class="text-sm text-slate-600">
            Analisi Totali
          </p>

          <p class="mt-2 text-3xl font-bold">
            {{ total }}
          </p>
        </div>

        <!-- DOMINANTE -->
        <div class="rounded-xl bg-green-50 p-4">
          <p class="text-sm text-slate-600">
            Felicità 
          </p>

          <p class="mt-2 text-3xl font-bold">
            {{ stats.happy }}%
          </p>
        </div>

        <!-- HAPPINESS -->
        <div class="rounded-xl bg-yellow-50 p-4">
          <p class="text-sm text-slate-600">
            Neutralità 
          </p>

          <p class="mt-2 text-3xl font-bold">
            {{ stats.neutral }}%
          </p>
        </div>

        <!-- SADNESS -->
        <div class="rounded-xl bg-red-50 p-4">
          <p class="text-sm text-slate-600">
            Tristezza
          </p>

          <p class="mt-2 text-3xl font-bold">
            {{ stats.sad }}%
          </p>
        </div>

      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";

const history = ref([]);

const props = defineProps({
  name: String,
  surname: String,
});

/* =========================
   FETCH HISTORY
========================= */
async function loadHistory() {
  try {
    const res = await fetch("http://localhost:8000/history/" + props.name + "/" + props.surname);
    const data = await res.json();

    history.value = data;
  } catch (err) {
    console.error("Errore fetch history:", err);
  }
}

const total = computed(() => history.value.length);

const stats = computed(() => {
  if (!history.value || history.value.length === 0) {
    return { happy: 0, neutral: 0, sad: 0 };
  }

  let happy = 0;
  let neutral = 0;
  let sad = 0;
  for (const entry of history.value) {
    switch (entry.emotion) {
      case "joy":
        happy++;
        break;
      case "neutral":
        neutral++;
        break;
      case "sadness":
        sad++;
        break;
    }
  }

  const total = history.value.length;

  return {
    happy: Math.round((happy / total) * 100),
    neutral: Math.round((neutral / total) * 100),
    sad: Math.round((sad / total) * 100),
  };
});


onMounted(() => {
  loadHistory();
});

</script>