<script setup>
import { ref, computed, watch } from "vue";
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
    currentIndex.value = 0;

    console.log(history.value);
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
}

//=================
// NEXT ELEMENT HISTORY 
const currentIndex = ref(0);

const currentItem = computed(() => {
  return history.value[currentIndex.value] || null;
});

function previousItem() {
  if (currentIndex.value > 0) {
    currentIndex.value--;
  }
}

function nextItem() {
  if (currentIndex.value < history.value.length - 1) {
    currentIndex.value++;
  }
}

/*=========================
  SELECT EMOTION  
=========================*/
const selectedGT = ref([]);

const emotions = [
  "JOY",
  "SADNESS",
  "ANGER",
  "FEAR",
  "SURPRISE",
  "NEUTRAL"
];

const emotionsColors = {
  "JOY": "bg-yellow-100 text-yellow-800",
  "SADNESS": "bg-blue-100 text-blue-800",
  "ANGER": "bg-red-100 text-red-800",
  "FEAR": "bg-purple-100 text-purple-800",
  "SURPRISE": "bg-orange-100 text-orange-800",
  "NEUTRAL": "bg-gray-100 text-gray-800"
};

function toggleEmotion(emotion) {
  const index = selectedGT.value.indexOf(emotion);

  if (index !== -1) {
    selectedGT.value.splice(index, 1);
    return;
  }

  // max 3
  if (selectedGT.value.length >= 3) return;

  selectedGT.value.push(emotion);
}

const maxReached = computed(() => selectedGT.value.length >= 3);

watch(currentIndex, () => {
  selectedGT.value = [];
});

async function saveGT() {
  try {
    const response = await fetch("http://localhost:8000/save-gt", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: currentItem.value.Name,
        surname: currentItem.value.Surname,
        id: currentItem.value.id,
        gt: selectedGT.value,
      }),
    });

    if (!response.ok) {
      throw new Error("Errore nel salvataggio GT");
    }

    currentItem.value.G_T = [...selectedGT.value];
  } catch (err) {
    error.value = err.message;
  }
}

</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-cover bg-center p-6"
    :style="{ backgroundImage: `url(${store.bgImage})` }">
    <div class="max-w-3xl mx-auto rounded-2xl bg-white p-8 shadow-md">

      <h2 class="mb-6 text-2xl font-semibold">
        View History
      </h2>

      <form @submit.prevent="submitForm" class="space-y-4">

        <div class="grid gap-4 md:grid-cols-2">

          <input v-model.trim="form.name" type="text" placeholder="Name" class="rounded-lg border px-4 py-3" />

          <input v-model.trim="form.surname" type="text" placeholder="Surname" class="rounded-lg border px-4 py-3" />

        </div>

        <button type="submit" :disabled="!isValid || loading" class="rounded-lg px-6 py-3 text-white"
          :class="isValid ? 'bg-indigo-600 hover:bg-indigo-700' : 'bg-gray-400'">
          {{ loading ? "Loading..." : "Load History" }}
        </button>

      </form>

      <div v-if="history.length" class="mt-6 rounded-lg bg-slate-50 p-4">

        <h3 class="font-semibold mb-4">
          History {{ currentIndex + 1 }} / {{ history.length }}
        </h3>

        <div v-if="currentItem" class="rounded-2xl border border-gray-200 bg-white p-6 shadow-md">

          <div class="flex items-center justify-between border-b pb-4">
            <div>
              <h3 class="text-xl font-bold text-gray-800">
                {{ currentItem.Name }} {{ currentItem.Surname }}
              </h3>
              <p class="text-sm text-gray-500">
                Record {{ currentIndex + 1 }} / {{ history.length }}
              </p>
            </div>

            <span class="rounded-full bg-indigo-100 px-4 py-1 text-sm font-semibold text-indigo-700">
              {{ currentItem.agreement }}
            </span>
          </div>

          <!-- Text -->
          <div class="mt-6">
            <h4 class="mb-2 font-semibold text-gray-700">
              Text
            </h4>
            <div class="rounded-lg bg-slate-100 p-4 text-gray-800 italic">
              "{{ currentItem.Text }}"
            </div>
          </div>

          <hr>
          
          <div v-if="currentItem.G_T" class="space-y-4 mt-6">

            <!-- Ground Truth -->
            <div class="rounded-xl border border-amber-300 bg-amber-50 p-4 text-center">
              <h4 class="text-sm font-semibold text-amber-700">
                Ground Truth
              </h4>

              <p class="mt-1 text-lg font-bold text-amber-900">
                {{ currentItem.G_T }}
              </p>
            </div>

            <!-- Modelli -->
            <div class="grid gap-4 md:grid-cols-3">

              <div class="rounded-xl border bg-blue-50 p-4">
                <h5 class="font-semibold text-blue-700">PIPELINE</h5>

                <p class="mt-2 text-lg font-bold">
                  {{ currentItem.Emotion_Pipeline }}
                </p>

                <p class="text-sm text-gray-600">
                  Confidence:
                  {{ (Number(currentItem.Confidence_Pipeline) * 100).toFixed(1) }}%
                </p>
              </div>

              <div class="rounded-xl border bg-green-50 p-4">
                <h5 class="font-semibold text-green-700">ROBERTA</h5>

                <p class="mt-2 text-lg font-bold">
                  {{ currentItem.Emotion_Roberta }}
                </p>

                <p class="text-sm text-gray-600">
                  Confidence:
                  <span v-for="(c, i) in JSON.parse(currentItem.Confidence_Roberta || '[]')" :key="i">
                    {{ (c * 100).toFixed(1) }}%
                    <span v-if="i < JSON.parse(currentItem.Confidence_Roberta || '[]').length - 1">
                      ,
                    </span>
                  </span>
                </p>
              </div>

              <div class="rounded-xl border bg-purple-50 p-4">
                <h5 class="font-semibold text-purple-700">QWEN</h5>

                <p class="mt-2 text-lg font-bold">
                  {{ currentItem.Emotion_Qwen }}
                </p>
              </div>

            </div>

          </div>
          <div v-else class="mt-6">
            <h4 class="font-semibold mb-2">
              Select Ground Truth (max 3, in order)
            </h4>

            <div class="flex flex-wrap gap-2">
              <button
                v-for="emotion in emotions"
                :key="emotion"
                @click="toggleEmotion(emotion)"
                class="px-3 py-2 rounded border"
                :disabled="!selectedGT.includes(emotion) && maxReached"
                :class="[
                  selectedGT.includes(emotion)
                    ? emotionsColors[emotion]
                    : 'bg-white hover:bg-gray-100',
                  !selectedGT.includes(emotion) && maxReached
                    ? 'opacity-50 cursor-not-allowed'
                    : ''
                ]"
              >
                {{ emotion }}
              </button>
            </div>

            <div class="mt-3 text-sm text-gray-600">
              Selected Emotions (in order):
            </div>

            <div class="flex gap-2 mt-1">
              <span
                v-for="(e, i) in selectedGT"
                :key="i"
                class="px-2 py-1 bg-gray-200 rounded"
                :class="emotionsColors[e]"
              >
                {{ i + 1 }}. {{ e }}
              </span>
            </div>

            <button
              class="mt-4 bg-green-600 text-white px-4 py-2 rounded disabled:opacity-50"
              :disabled="selectedGT.length === 0"
              @click="saveGT"
            >
              Save Ground Truth
            </button>

            <p v-if="maxReached" class="text-sm text-red-500 mt-2">
              You have reached the maximum limit of 3 emotions.
            </p>
          </div>

        </div>


      </div>

      <div class="mt-4 flex justify-between">

        <button @click="previousItem" :disabled="currentIndex === 0"
          class="rounded bg-gray-500 px-4 py-2 text-white disabled:opacity-50">
          ← Previous
        </button>

        <button @click="nextItem" :disabled="currentIndex >= history.length - 1"
          class="rounded bg-indigo-600 px-4 py-2 text-white disabled:opacity-50">
          Next →
        </button>

      </div>

    </div>

    <p v-if="error" class="mt-4 text-red-500">
      {{ error }}
    </p>

  </div>

</template>