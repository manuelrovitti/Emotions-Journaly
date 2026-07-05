<script setup>
import { ref, computed } from "vue";
import EmotionBarChart from "../components/EmotionBarChart.vue";
import { useSiteStore } from "../stores/HomeStore";

const store = useSiteStore();

const form = ref({
  name: "",
  surname: ""
});

const history = ref([]);
const loading = ref(false);
const error = ref("");

const isValid = computed(() =>
  form.value.name.trim() !== "" &&
  form.value.surname.trim() !== ""
);

async function submitForm() {
  loading.value = true;
  error.value = "";

  try {
    const response = await fetch(
      `http://localhost:8000/history/${encodeURIComponent(form.value.name)}/${encodeURIComponent(form.value.surname)}`
    );

    if (!response.ok) {
      throw new Error("Errore nel recupero della cronologia.");
    }

    history.value = await response.json();
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div
    class="min-h-screen flex items-center justify-center bg-cover bg-center p-6"
    :style="{ backgroundImage: `url(${store.bgImage})` }"
  >
    <div class="w-full max-w-6xl bg-white/90 backdrop-blur-md rounded-3xl shadow-2xl p-12 text-center">

      <h1 class="text-5xl font-bold mb-6 text-green-900">
        ANALYSIS
      </h1>

      <form @submit.prevent="submitForm" class="space-y-4">

        <div class="grid gap-4 md:grid-cols-2">
          <input v-model.trim="form.name" placeholder="Name" class="border p-3 rounded-lg" />
          <input v-model.trim="form.surname" placeholder="Surname" class="border p-3 rounded-lg" />
        </div>

        <button
          type="submit"
          :disabled="!isValid || loading"
          class="px-6 py-3 rounded-lg text-white"
          :class="isValid ? 'bg-indigo-600' : 'bg-gray-400'"
        >
          {{ loading ? "Loading..." : "Load Analysis" }}
        </button>
      </form>

      <div v-if="history.length" class="mt-10">
        <EmotionBarChart :history="history" />
      </div>

    </div>
  </div>
</template>