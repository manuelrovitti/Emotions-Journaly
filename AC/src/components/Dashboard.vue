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
import { ref, computed, watch } from "vue";

const history = ref([]);

const props = defineProps({
  name: String,
  surname: String,
});

/* =========================
   FETCH HISTORY
========================= */
async function loadHistory() {
  console.log("▶ loadHistory chiamata");

  const url = `http://localhost:8000/history/${props.name}/${props.surname}`;
  console.log("URL:", url);

  const res = await fetch(url);

  console.log("STATUS:", res.status);

  const text = await res.text();
  console.log("RAW RESPONSE:", text);

  const data = JSON.parse(text);
  console.log("PARSED DATA:", data);

  history.value = data;
}

const total = computed(() => history.value.length);

const stats = computed(() => {
  const counts = {
    joy: 0,
    neutral: 0,
    sadness: 0,
  };

  for (const emotion of history.value || []) {
    if (counts[emotion] !== undefined) {
      counts[emotion]++;
    }
  }

  const total = history.value.length || 1;

  return {
    happy: Math.round((counts.joy / total) * 100),
    neutral: Math.round((counts.neutral / total) * 100),
    sad: Math.round((counts.sadness / total) * 100),
  };
});


  watch(
    () => props.name + props.surname,
    async () => {
      await loadHistory();
    },
    { immediate: true }
  );

</script>