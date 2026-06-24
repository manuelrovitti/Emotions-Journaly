<template>
  <div class="w-full max-w-6xl mx-auto rounded-2xl bg-white p-8 shadow-md">
    <h2 class="mb-6 text-2xl font-semibold text-slate-800">
      New Thoughts
    </h2>

    <form @submit.prevent="submitForm" class="space-y-4">

      <!-- NAME + SURNAME -->
      <div class="grid gap-4 md:grid-cols-2">
        <div>
          <label class="mb-2 block text-sm font-medium">
            Name
          </label>

          <input
            v-model="form.name"
            type="text"
            placeholder="Mario"
            class="w-full rounded-lg border border-slate-300 px-4 py-3 focus:border-indigo-500 focus:outline-none"
          />
        </div>

        <div>
          <label class="mb-2 block text-sm font-medium">
            Surname
          </label>

          <input
            v-model="form.surname"
            type="text"
            placeholder="Rossi"
            class="w-full rounded-lg border border-slate-300 px-4 py-3 focus:border-indigo-500 focus:outline-none"
          />
        </div>
      </div>

      <!-- TEXT AREA -->
      <div>
        <label class="mb-2 block text-sm font-medium">
          How are you feeling today?
        </label>

        <textarea
          v-model="form.text"
          rows="6"
          placeholder="Scrivi qui i tuoi pensieri..."
          class="w-full resize-none rounded-lg border border-slate-300 px-4 py-3 focus:border-indigo-500 focus:outline-none"
        ></textarea>
      </div>

      <!-- BUTTON -->
      <button
        type="submit"
        :disabled="!isValid"
        class="rounded-lg px-6 py-3 font-semibold text-white transition"
        :class="isValid
          ? 'bg-indigo-600 hover:bg-indigo-700'
          : 'bg-gray-400 cursor-not-allowed'"
      >
        Analyze Emotion
      </button>
    </form>

    <!-- RESULT -->
    <div
      v-if="emotion"
      class="mt-6 rounded-xl bg-slate-50 p-4"
    >
      <p class="text-sm text-slate-500">
        Emotion detected
      </p>

      <p class="mt-2 text-xl font-bold">
        {{ emotion }}
      </p>

      <p class="text-lg font-semibold text-indigo-600">
        Confidence: {{ confidence }}%
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";

const emit = defineEmits(["analyze"]);

const emotion = ref("");
const confidence = ref(null);

const form = ref({
  name: "",
  surname: "",
  text: "",
});

/* ✅ VALIDAZIONE FORM */
const isValid = computed(() => {
  return (
    form.value.name.trim() !== "" &&
    form.value.surname.trim() !== "" &&
    form.value.text.trim() !== ""
  );
});

async function submitForm() {
  if (!isValid.value) return;


  try {
    const response = await fetch("http://localhost:8000/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(form.value),
    });

    const data = await response.json();

    emotion.value = data.emotion;
    confidence.value = data.confidence;

  emit("analyze", {
    name: form.value.name,
    surname: form.value.surname,
    text: form.value.text,
    emotion: data.emotion,
    confidence: data.confidence,

    });

  } catch (err) {
    emotion.value = "Errore API";
    console.error(err);
  }

  loading.value = false;
}
</script>