<script setup>
import { ref, computed } from "vue";
import { useSiteStore } from "../stores/HomeStore";

const store = useSiteStore();


const form = ref({
  name: "",
  surname: "",
});


const history = ref([]);
const selectedItem = ref(null);

const loading = ref(false);
const error = ref("");



const isValid = computed(() =>
  form.value.name.trim() !== "" &&
  form.value.surname.trim() !== ""
);



// ==========================
// LOAD HISTORY
// ==========================

async function submitForm() {

  loading.value = true;
  error.value = "";

  try {

    const response = await fetch(
      `http://localhost:8000/history/${encodeURIComponent(form.value.name)}/${encodeURIComponent(form.value.surname)}`
    );


    if (!response.ok)
      throw new Error("Errore recupero history");


    history.value = await response.json();

    console.log(history.value[0]);
    console.log(Object.keys(history.value[0]));


    selectedItem.value = null;


  } catch (err) {

    error.value = err.message;

  } finally {

    loading.value = false;

  }

}




// ==========================
// SELECT
function selectItem(item) {
  selectedItem.value = item;
}




// ==========================
// GET FIELD ROBUSTO
function getField(item, name) {
  const keys = [
    name,
    name.toLowerCase(),
    name.replaceAll("_", ""),
    name.toLowerCase().replaceAll("_", ""),
    name.replace("_", " ")
  ];

  for (const key of keys) {
    if (item[key] !== undefined)
      return item[key];
  }
  return "";
}

// ==========================
// PARSE ARRAY
function parseArray(value) {
  if (!value)
    return [];

  if (Array.isArray(value))
    return value;

  try {
    return JSON.parse(value);
  }
  catch {
    try {
      return JSON.parse(value.replaceAll("'", "\""));
    }
    catch {
      return [];
    }
  }
}

// ==========================
// PARSE DICT
function parseDict(value) {
  if (!value)
    return {};

  if (typeof value === "object")
    return value;

  try {
    return JSON.parse(value);
  }
  catch {
    try {
      return JSON.parse(value.replaceAll("'", "\""));
    }
    catch {
      return {};
    }
  }
}

// ==========================
// AGREEMENT TOP 3
function getAgreement(value) {
  const dict = parseDict(value);
  return Object.entries(dict)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 3)
    .map(
      ([emotion, value]) => {
        return {
          emotion,
          value
        }
      }
    );
}
</script>





<template>


  <div
  class="min-h-screen flex items-center justify-center bg-cover bg-center p-6"
  :style="{backgroundImage:`url(${store.bgImage})`}"
  >


    <div
    class="max-w-7xl w-full bg-white rounded-2xl shadow p-8"
    >


      <h2 class="text-2xl font-semibold mb-6">
      View History
      </h2>





      <form
      @submit.prevent="submitForm"
      class="space-y-4"
      >


      <div class="grid md:grid-cols-2 gap-4">


        <input
        v-model.trim="form.name"
        placeholder="Name"
        class="rounded-lg border px-4 py-3"
        />


        <input
        v-model.trim="form.surname"
        placeholder="Surname"
        class="rounded-lg border px-4 py-3"
        />


      </div>



        <button
        :disabled="!isValid || loading"
        class="px-6 py-3 rounded-lg text-white"
        :class="isValid?'bg-indigo-600':'bg-gray-400'"
        >
        {{loading ? "Loading..." : "Load History"}}
        </button>
      </form>


      <div
  v-if="history.length"
  class="mt-8 space-y-8"
>

  <!-- HISTORY -->

  <div>

    <h3 class="font-bold mb-4">
      History {{ history.length }}
    </h3>

    <div class="max-h-[500px] overflow-y-auto border rounded-xl p-4">

      <div
        v-for="(item,index) in history"
        :key="item.id"
        @click="selectItem(item)"
        class="border rounded-xl p-4 mb-3 cursor-pointer transition-all duration-200"
        :class="
          selectedItem?.id===item.id
            ? 'bg-indigo-100 border-indigo-500 shadow'
            : 'hover:bg-gray-50'
        "
      >

        <div class="flex justify-between items-start gap-6">

          <div class="flex-1">

            <p class="font-bold">
              #{{ index + 1 }}
            </p>

            <p class="text-gray-700 mt-2 line-clamp-2">
              {{ item.Text }}
            </p>

          </div>

          <div class="text-right shrink-0">

            <p class="text-xs text-gray-500">
              Ground Truth
            </p>

            <p class="font-semibold">
              {{ parseArray(getField(item,'emotion_gt')).join(", ") }}
            </p>

          </div>

        </div>

      </div>

    </div>

  </div>



  <!-- DETAILS -->

  <div
    v-if="selectedItem"
    class="border-t pt-8"
  >

    <h2 class="text-2xl font-bold mb-5">
      Emotion Analysis
    </h2>

    <div class="bg-gray-100 rounded-xl p-5 mb-6">
      {{ selectedItem.Text }}
    </div>



    <!-- AGREEMENT -->

    <div class="mb-8">

      <h3 class="font-bold mb-3">
        Agreement Top 3
      </h3>

      <div
        v-for="(a,index) in getAgreement(getField(selectedItem,'agreement'))"
        :key="index"
        class="flex justify-between border-b py-2"
      >

        <span>
          {{ index + 1 }}. {{ a.emotion }}
        </span>

        <span class="font-semibold">
          {{ (a.value*100).toFixed(2) }}%
        </span>

      </div>

    </div>



    <div class="grid md:grid-cols-3 gap-5">

      <!-- PIPELINE -->

      <div class="bg-blue-50 border rounded-xl p-4">

        <h3 class="font-bold text-blue-700 mb-3">
          PIPELINE
        </h3>

        <div
          v-for="(e,i) in parseArray(getField(selectedItem,'Emotion_Pipeline'))"
          :key="i"
          class="flex justify-between py-1"
        >

          <span>{{ e }}</span>

          <span>

            {{
              (
                parseArray(getField(selectedItem,'Confidence_Pipeline'))[i] * 100
              ).toFixed(2)
            }}%

          </span>

        </div>

      </div>



      <!-- ROBERTA -->

      <div class="bg-green-50 border rounded-xl p-4">

        <h3 class="font-bold text-green-700 mb-3">
          ROBERTA
        </h3>

        <div
          v-for="(e,i) in parseArray(getField(selectedItem,'Emotion_Roberta'))"
          :key="i"
          class="flex justify-between py-1"
        >

          <span>{{ e }}</span>

          <span>

            {{
              (
                parseArray(getField(selectedItem,'Confidence_Roberta'))[i] * 100
              ).toFixed(2)
            }}%

          </span>

        </div>

      </div>



      <!-- QWEN -->

      <div class="bg-purple-50 border rounded-xl p-4">

        <h3 class="font-bold text-purple-700 mb-3">
          QWEN
        </h3>

        <div
          v-for="(e,i) in parseArray(getField(selectedItem,'Emotion_Qwen'))"
          :key="i"
          class="flex justify-between py-1"
        >

          <span>{{ e }}</span>

          <span>

            {{
              (
                parseArray(getField(selectedItem,'Confidence_Qwen'))[i] * 100
              ).toFixed(2)
            }}%

          </span>

        </div>

      </div>

    </div>



    <!-- GROUND TRUTH -->

    <div class="mt-8 bg-yellow-50 border rounded-xl p-5">

      <h3 class="font-bold text-yellow-700 mb-4">
        Ground Truth
      </h3>

      <div
        v-for="(e,i) in parseArray(getField(selectedItem,'emotion_gt'))"
        :key="i"
        class="flex justify-between py-2 border-b last:border-0"
      >

        <span>{{ e }}</span>

        <span>

          {{
            (
              parseArray(getField(selectedItem,'intensity_gt'))[i] * 100
            ).toFixed(1)
          }}%

        </span>

      </div>

    </div>

  </div>

</div>
</div>


  <p
  v-if="error"
  class="text-red-500 mt-4"
  >

    {{error}}

  </p>


</div>

</template>
