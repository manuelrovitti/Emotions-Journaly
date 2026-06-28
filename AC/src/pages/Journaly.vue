<script setup>
import { ref, computed } from "vue";
import { useSiteStore } from '../stores/HomeStore'

const store = useSiteStore()

const form = ref({
  name: "",
  surname: "",
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

    console.log(history.value);
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
        <div class="max-w-3xl mx-auto rounded-2xl bg-white p-8 shadow-md">

            <h2 class="mb-6 text-2xl font-semibold">
            View History
            </h2>

            <form @submit.prevent="submitForm" class="space-y-4">

            <div class="grid gap-4 md:grid-cols-2">

                <input
                v-model="form.name"
                type="text"
                placeholder="Name"
                class="rounded-lg border px-4 py-3"
                />

                <input
                v-model="form.surname"
                type="text"
                placeholder="Surname"
                class="rounded-lg border px-4 py-3"
                />

            </div>

            <button
                type="submit"
                :disabled="!isValid || loading"
                class="rounded-lg px-6 py-3 text-white"
                :class="isValid ? 'bg-indigo-600 hover:bg-indigo-700' : 'bg-gray-400'"
            >
                {{ loading ? "Loading..." : "Load History" }}
            </button>

            </form>

            <div v-if="history.length" class="mt-6 rounded-lg bg-slate-50 p-4">
            <h3 class="font-semibold mb-2">History</h3>

            <ul>
                <li
                v-for="(item, index) in history"
                :key="index"
                >
                {{ item }}
                </li>
            </ul>
            </div>

            <p
            v-if="error"
            class="mt-4 text-red-500"
            >
            {{ error }}
            </p>

        </div>
    </div>
</template>