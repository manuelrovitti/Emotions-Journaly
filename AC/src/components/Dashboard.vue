<template>
  <div class="w-full max-w-6xl mx-auto">

    <div class="rounded-2xl bg-white p-6 shadow-sm">
      <h2 class="mb-2 text-2xl font-semibold">
        Dashboard
      </h2>

      <div class="grid grid-cols-2 gap-4">

        <div class="rounded-xl bg-indigo-50 p-4">
          <p class="text-sm text-slate-600">
            Analisi Totali
          </p>

          <p class="mt-2 text-3xl font-bold">
            {{ totalAnalyses }}
          </p>
        </div>

        <div class="rounded-xl bg-green-50 p-4">
          <p class="text-sm text-slate-600">
            Emozione Dominante
          </p>

          <p class="mt-2 text-3xl font-bold">
            {{ dominantEmotion }}
          </p>
        </div>

        <div class="rounded-xl bg-yellow-50 p-4">
          <p class="text-sm text-slate-600">
            Stress
          </p>

          <p class="mt-2 text-3xl font-bold">
            {{ stressPercentage }}%
          </p>
        </div>

        <div class="rounded-xl bg-red-50 p-4">
          <p class="text-sm text-slate-600">
            Tristezza
          </p>

          <p class="mt-2 text-3xl font-bold">
            {{ sadnessPercentage }}%
          </p>
        </div>

      </div>
    </div>

  </div>
</template>

<script setup>
defineProps({
  history: {
    type: Array,
    default: () => [],
  },

  totalAnalyses: {
    type: Number,
    default: 0,
  },

  dominantEmotion: {
    type: String,
    default: "😊",
  },

  stressPercentage: {
    type: Number,
    default: 0,
  },

  sadnessPercentage: {
    type: Number,
    default: 0,
  },
});
</script>