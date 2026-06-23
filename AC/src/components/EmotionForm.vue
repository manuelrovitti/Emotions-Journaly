<template>
  <div class="rounded-2xl bg-white p-6 shadow-sm">
    <h2 class="mb-6 text-2xl font-semibold text-slate-800">
      Nuova Analisi
    </h2>

    <form
      @submit.prevent="submitForm"
      class="space-y-4"
    >
      <div class="grid gap-4 md:grid-cols-2">
        <div>
          <label class="mb-2 block text-sm font-medium">
            Nome
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
            Cognome
          </label>

          <input
            v-model="form.surname"
            type="text"
            placeholder="Rossi"
            class="w-full rounded-lg border border-slate-300 px-4 py-3 focus:border-indigo-500 focus:outline-none"
          />
        </div>
      </div>

      <div>
        <label class="mb-2 block text-sm font-medium">
          Come ti senti oggi?
        </label>

        <textarea
          v-model="form.text"
          rows="6"
          placeholder="Scrivi qui i tuoi pensieri..."
          class="w-full rounded-lg border border-slate-300 px-4 py-3 focus:border-indigo-500 focus:outline-none"
        />
      </div>

      <button
        type="submit"
        class="rounded-lg bg-indigo-600 px-6 py-3 font-semibold text-white transition hover:bg-indigo-700"
      >
        Analizza Emozione
      </button>
    </form>

    <div
      v-if="emotion"
      class="mt-6 rounded-xl bg-slate-50 p-4"
    >
      <p class="text-sm text-slate-500">
        Emozione rilevata
      </p>

      <p class="mt-2 text-xl font-bold">
        {{ emotion }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const emit = defineEmits(["analyze"]);

const emotion = ref("");

const form = ref({
  name: "",
  surname: "",
  text: "",
});

function submitForm() {
  emit("analyze", form.value);

  emotion.value = "😰 Stress";
}
</script>