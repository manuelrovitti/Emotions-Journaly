<template>
  <div class="relative w-full max-w-6xl mx-auto rounded-2xl bg-white p-8 shadow-md">

    <!-- Loading Overlay -->
    <div
      v-if="loading"
      class="absolute inset-0 z-50 flex flex-col items-center justify-center rounded-2xl bg-white/80 backdrop-blur-sm"
    >
      <div
        class="h-14 w-14 rounded-full border-4 border-indigo-600 border-t-transparent animate-spin"
      ></div>

      <p class="mt-4 text-lg font-medium text-slate-700">
        Analyzing your thoughts...
      </p>

      <p class="text-sm text-slate-500">
        This may take a few seconds.
      </p>
    </div>

    <h2 class="mb-6 text-2xl font-semibold text-slate-800">
      New Thoughts
    </h2>

    <form @submit.prevent="submitForm" class="space-y-4">

      <div class="grid gap-4 md:grid-cols-2">
        <input
          v-model.trim="form.name"
          placeholder="Name"
          class="w-full rounded-lg border px-4 py-3"
        />

        <input
          v-model.trim="form.surname"
          placeholder="Surname"
          class="w-full rounded-lg border px-4 py-3"
        />
      </div>

      <textarea
        v-model.trim="form.text"
        rows="6"
        placeholder="Write your thoughts..."
        class="w-full rounded-lg border px-4 py-3"
      ></textarea>

      <button
        type="submit"
        :disabled="!isValid || loading"
        class="rounded-lg px-6 py-3 text-white transition"
        :class="
          isValid && !loading
            ? 'bg-indigo-600 hover:bg-indigo-700'
            : 'bg-gray-400 cursor-not-allowed'
        "
      >
        {{ loading ? "Analyzing..." : "Analyze Emotion" }}
      </button>
    </form>

    <!-- PIPELINE -->
    <div v-if="hasPipeline" class="mt-6 rounded-xl bg-slate-50 p-4">
      <p class="text-sm text-slate-500">Emotion Pipeline</p>

      <p class="text-xl font-bold">
        {{ emotion_pipeline || "N/A" }}
      </p>

      <p class="font-semibold text-indigo-600">
        Confidence: {{ confidence_pipeline }}%
      </p>
    </div>

    <!-- ROBERTTA -->
    <div v-if="hasRoberta" class="mt-6 rounded-xl bg-slate-50 p-4">
      <p class="text-sm text-slate-500">Emotion Roberta</p>

      <p class="text-xl font-bold">
        {{ emotion_roberta || "N/A" }}
      </p>

      <p class="font-semibold text-indigo-600">
        Confidence: {{ confidence_roberta }}%
      </p>

      <p v-if="api_error" class="mt-2 text-sm text-red-500">
        {{ api_error }}
      </p>
    </div>

    <div v-if="hasQwen" class="mt-6 rounded-xl bg-slate-50 p-4">
      <p class="text-sm text-slate-500">Emotion Qwen</p>

      <p class="text-xl font-bold">
        {{ emotion_qwen || "N/A" }}
      </p>

      <p v-if="api_error" class="mt-2 text-sm text-red-500">
        {{ api_error }}
      </p>
    </div>

  </div>
</template>

<script setup>
import { ref, computed } from "vue";

/* ✅ EMIT */
const emit = defineEmits(["analyze"]);

const form = ref({
  name: "",
  surname: "",
  text: "",
});

/* RESULTS */
const emotion_pipeline = ref("");
const confidence_pipeline = ref(0);

const emotion_roberta = ref("");
const confidence_roberta = ref(0);

const emotion_qwen = ref("");
const confidence_qwen = ref(0);

/* LOADING */
const loading = ref(false);

/* VALIDATION */
const isValid = computed(() =>
  form.value.name &&
  form.value.surname &&
  form.value.text
);

/* VISIBILITY */
const hasPipeline = computed(() => !!emotion_pipeline.value);
const hasRoberta = computed(
  () => emotion_roberta.value !== null && emotion_roberta.value !== ""
);
const hasQwen = computed ( 
  () => emotion_qwen.value != null && emotion_qwen.value != ""
);

/* SUBMIT */
async function submitForm() {
  loading.value = true;

  try {
    const res = await fetch("http://localhost:8000/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(form.value),
    });

    const data = await res.json();

    console.log("API RESPONSE:", data);

    emotion_pipeline.value = data.emotion_pipeline;
    confidence_pipeline.value = (
      data.confidence_pipeline * 100
    ).toFixed(2);

    emotion_roberta.value = data.emotion_roberta;
    confidence_roberta.value = (
      data.confidence_roberta * 100
    ).toFixed(2);

    emotion_qwen.value = data.emotion_qwen;



    /* ✅ EMIT AL PARENT */
    emit("analyze", {
      name: form.value.name,
      surname: form.value.surname,
    });

  } catch (err) {
    console.error(err);
    api_error.value = "Backend error";
  } finally {
    loading.value = false;
  }
}
</script>