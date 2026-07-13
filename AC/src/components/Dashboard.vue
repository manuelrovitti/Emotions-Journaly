<template>
  <div class="w-full max-w-6xl mx-auto">

    <div class="rounded-2xl bg-white p-6 shadow-sm">
      <h2 class="mb-2 text-2xl font-semibold">
        Dashboard {{ props.name }} {{ props.surname }}
      </h2>

      <div class="grid grid-cols-2 gap-4">

        <!-- TOTALI -->
        <div class="rounded-xl bg-indigo-50 p-4">
          <p class="text-sm text-slate-600">
            Analytical Total
          </p>

          <p class="mt-2 text-3xl font-bold">
            {{ total }}
          </p>
        </div>

        <!-- JOY -->
        <div class="rounded-xl bg-yellow-50 p-4">
          <p class="text-sm text-slate-600">
            JOY 😂
          </p>

          <p class="mt-2 text-3xl font-bold">
            {{ stats.joy }}%
          </p>
        </div>

        <!-- SADNESS -->
        <div class="rounded-xl bg-blue-50 p-4">
          <p class="text-sm text-slate-600">
            SADNESS 😞
          </p>

          <p class="mt-2 text-3xl font-bold">
            {{ stats.sadness }}%
          </p>
        </div>

        <!-- ANGER -->
        <div class="rounded-xl bg-red-50 p-4">
          <p class="text-sm text-slate-600">
            ANGER 😡
          </p>

          <p class="mt-2 text-3xl font-bold">
            {{ stats.anger }}%
          </p>
        </div>

        <!-- FEAR -->
        <div class="rounded-xl bg-purple-50 p-4">
          <p class="text-sm text-slate-600">
            FEAR 😱
          </p>

          <p class="mt-2 text-3xl font-bold">
            {{ stats.fear }}%
          </p>
        </div>

        <!-- DISGUST -->
        <div class="rounded-xl bg-green-50 p-4">
          <p class="text-sm text-slate-600">
            DISGUST 🤮
          </p>

          <p class="mt-2 text-3xl font-bold">
            {{ stats.disgust }}%
          </p>
        </div>

        <!-- SURPRISE -->
        <div class="rounded-xl bg-orange-50 p-4">
          <p class="text-sm text-slate-600">
            SURPRISE 😯
          </p>

          <p class="mt-2 text-3xl font-bold">
            {{ stats.surprise }}%
          </p>
        </div>

        <!-- NEUTRAL -->
        <div class="rounded-xl bg-gray-50 p-4">
          <p class="text-sm text-slate-600">
            NEUTRAL 😐
          </p>

          <p class="mt-2 text-3xl font-bold">
            {{ stats.neutral }}%
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

  const url = `http://localhost:8000/dashboard/${props.name}/${props.surname}`;
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

/* =========================
   COMPUTED PROPERTIES
========================= */

const stats = computed(() => {
  const counts = {
    joy: 0,
    sadness: 0,
    anger: 0,
    fear: 0,
    surprise: 0,
    disgust: 0,
    neutral: 0
  };

  for (const row of history.value || []) {

    if (counts[row] !== undefined) {
      counts[row]++;
    }
  }

  const total = history.value.length || 1;

  return {
    joy: Math.round((counts.joy / total) * 100),
    sadness: Math.round((counts.sadness / total) * 100),
    anger: Math.round((counts.anger / total) * 100),
    fear: Math.round((counts.fear / total) * 100),
    surprise: Math.round((counts.surprise / total) * 100),
    disgust: Math.round((counts.disgust / total) * 100),
    neutral: Math.round((counts.neutral / total) * 100),
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