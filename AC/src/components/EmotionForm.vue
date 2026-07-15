<template>
  <div class="relative w-full max-w-6xl mx-auto rounded-2xl bg-white p-8 shadow-md">

    <h2 class="mb-6 text-2xl font-semibold text-slate-800">
      New Thoughts
    </h2>

    <form @submit.prevent="submitForm" class="space-y-6">

      <!-- USER DATA -->
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


      <!-- TEXT -->
      <textarea
        v-model.trim="form.text"
        rows="6"
        placeholder="Write your thoughts..."
        class="w-full rounded-lg border px-4 py-3"
      ></textarea>

      <!-- INSTRUCTION TEXT -->
      <div class="text-center mt-8 mb-4">

        <h3 class="text-xl font-semibold text-slate-700">
          How do you feel about this thought?
        </h3>

        <p class="mt-2 text-sm text-slate-500">
          Select the emotion that best represents your feeling
          and adjust its intensity level.
        </p>

      </div>

      <!-- 3 HUMAN EVALUATIONS -->
      <div
        v-for="(selection,index) in selections"
        :key="index"
        class="rounded-xl bg-slate-50 p-5"
      >
        <h3 class="mb-4 text-lg font-semibold text-slate-700">
          Emotion {{ index + 1 }}
        </h3>


        <!-- INTENSITY -->
        <div>

          <p class="text-sm text-slate-500 mb-2">
            Intensity: {{ selection.intensity }}/10
          </p>


          <input
            type="range"
            min="1"
            max="10"
            v-model="selection.intensity"
            class="w-full"
          />

        </div>



        <!-- EMOTION PICKER -->
        <div class="mt-5 grid grid-cols-3 md:grid-cols-7 gap-3">

          <button
            v-for="emotion in emotions"
            :key="emotion.name"
            type="button"
            @click="selection.emotion = emotion.name"
            class="flex flex-col items-center rounded-xl p-3 transition"
            :class="
              selection.emotion === emotion.name
              ? 'bg-indigo-200 scale-110'
              : 'hover:bg-slate-200'
            "
          >

            <span class="text-4xl">
              {{ emotion.emoji }}
            </span>


            <span class="mt-1 text-xs text-slate-600">
              {{ emotion.name }}
            </span>


          </button>

        </div>

      </div>



      <!-- SUBMIT -->
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
        {{ loading ? "Analyzing..." : "Save evaluation" }}
      </button>


    </form>

  </div>
</template>



<script setup>

import { ref, computed } from "vue";


const emit = defineEmits(["analyze"]);


const loading = ref(false);



/*
 USER FORM
*/
const form = ref({

  name:"",
  surname:"",
  text:""

});



/*
 EMOTIONS
*/
const emotions = [

  {
    name:"joy",
    emoji:"😀"
  },

  {
    name:"sadness",
    emoji:"😢"
  },

  {
    name:"anger",
    emoji:"😡"
  },

  {
    name:"fear",
    emoji:"😨"
  },
  {
    name: "disgust",
    emoji: "🤮"

  },

  {
    name:"surprise",
    emoji:"😮"
  },

  {
    name:"neutral",
    emoji:"😐"
  }

];



/*
 THREE EVALUATIONS
*/
const selections = ref([

  {
    intensity:5,
    emotion:""
  },

  {
    intensity:5,
    emotion:""
  },

  {
    intensity:5,
    emotion:""
  }

]);



/*
 VALIDATION
*/
const isValid = computed(()=>{

  return (

    form.value.name.trim() !== "" &&

    form.value.surname.trim() !== "" &&

    form.value.text.trim() !== "" &&

    selections.value.every(
      item => item.emotion !== ""
    )

  );

});



/*
 SEND DATA
*/
async function submitForm(){


  loading.value = true;

  const rawIntensities = selections.value.map(
    item => Number(item.intensity)
  );


  const totalIntensity = rawIntensities.reduce(
    (sum,value)=> sum + value,
    0
  );


  const normalizedIntensities = rawIntensities.map(
    value => Number(
      (value / totalIntensity).toFixed(3)
    )
  );



  const data = {


    name: form.value.name,


    surname: form.value.surname,


    text: form.value.text,



    emotion: selections.value.map(
      item => item.emotion
    ),



    intensity: normalizedIntensities


  };



  console.log(
    "SEND TO ANALYZE:",
    data
  );



  try {


    const response = await fetch(

      "http://localhost:8000/analyze",

      {

        method:"POST",

        headers:{

          "Content-Type":"application/json"

        },

        body: JSON.stringify(data)

      }

    );



    if(!response.ok){

      throw new Error(
        "Backend error"
      );

    }



    const result = await response.json();



    console.log(
      "ANALYZE RESULT:",
      result
    );



    const finalData = {


      name: data.name,


      surname: data.surname,


      text: data.text,



      emotion: data.emotion,


      intensity: data.intensity,



      ...result


    };



    console.log(
      "FINAL DATA:",
      finalData
    );



    emit(
      "analyze",
      finalData
    );


  }


  catch(error){


    console.error(
      "Analyze error:",
      error
    );


  }


  finally{


    loading.value = false;


  }


}

</script>