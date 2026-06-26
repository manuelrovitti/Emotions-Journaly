<template>
  <div class="w-full max-w-6xl mx-auto rounded-2xl bg-white p-8 shadow-md">
    <h2 class="mb-6 text-2xl font-semibold text-slate-800">
      New Thoughts
    </h2>

    <form @submit.prevent="submitForm" class="space-y-4">

      <div class="grid gap-4 md:grid-cols-2">
        <input v-model="form.name" placeholder="Name"
          class="w-full rounded-lg border px-4 py-3" />

        <input v-model="form.surname" placeholder="Surname"
          class="w-full rounded-lg border px-4 py-3" />
      </div>

      <textarea v-model="form.text"
        rows="6"
        placeholder="Write your thoughts..."
        class="w-full rounded-lg border px-4 py-3">
      </textarea>

      <button
        type="submit"
        :disabled="!isValid"
        class="px-6 py-3 rounded-lg text-white"
        :class="isValid ? 'bg-indigo-600' : 'bg-gray-400'"
      >
        Analyze Emotion
      </button>
    </form>

    <!-- PIPELINE -->
    <div
      v-if="hasPipeline"
      class="mt-6 rounded-xl bg-slate-50 p-4"
    >
      <p class="text-sm text-slate-500">Emotion Pipeline</p>

      <p class="text-xl font-bold">
        {{ emotion_pipeline || "N/A" }}
      </p>

      <p class="text-indigo-600 font-semibold">
        Confidence: {{ confidence_pipeline }}%
      </p>
    </div>

    <!-- API -->
    <div
      v-if="hasApi"
      class="mt-6 rounded-xl bg-slate-50 p-4"
    >
      <p class="text-sm text-slate-500">Emotion API</p>

      <p class="text-xl font-bold">
        {{ emotion_api || "N/A" }}
      </p>

      <p class="text-indigo-600 font-semibold">
        Confidence: {{ confidence_api }}%
      </p>

      <!-- DEBUG ERROR (IMPORTANTISSIMO) -->
      <p v-if="api_error" class="text-red-500 text-sm mt-2">
        {{ api_error }}
      </p>
    </div>

  </div>
</template>

<script setup>
import { ref, computed } from "vue";

const form = ref({
  name: "",
  surname: "",
  text: "",
});

/* RESULTS */
const emotion_pipeline = ref("");
const confidence_pipeline = ref(0);

const emotion_api = ref("");
const confidence_api = ref(0);

const api_error = ref(null);

/* VALIDATION */
const isValid = computed(() =>
  form.value.name && form.value.surname && form.value.text
);

/* VISIBILITY (IMPORTANT FIX) */
const hasPipeline = computed(() => !!emotion_pipeline.value);
const hasApi = computed(() => emotion_api.value !== null && emotion_api.value !== "");

/* SUBMIT */
async function submitForm() {
  try {
    const res = await fetch("http://localhost:8000/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form.value),
    });

    const data = await res.json();

    console.log("API RESPONSE:", data); // DEBUG

    /* PIPELINE */
    emotion_pipeline.value = data.emotion_pipeline;
    confidence_pipeline.value = (data.confidence_pipeline * 100).toFixed(2);

    /* API */
    emotion_api.value = data.emotion_api;
    confidence_api.value = (data.confidence_api * 100).toFixed(2);

    /* ERROR HANDLING */
    api_error.value = data.error || null;

  } catch (err) {
    console.error(err);
    api_error.value = "Backend error";
  }
}
</script>