<script setup>
import { computed } from "vue";
import { Bar } from "vue-chartjs";

import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from "chart.js";


ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
);



const props = defineProps({
  history:{
    type:Array,
    required:true
  }
});



// ------------------------
// EMOTIONS
// ------------------------

const emotions = [
  "anger",
  "disgust",
  "fear",
  "joy",
  "neutral",
  "sadness",
  "surprise"
];




// ------------------------
// NORMALIZE
function normalize(x){
  return String(x ?? "")
    .toLowerCase()
    .replace(/["']/g,"")
    .trim();
}

// ------------------------
// PARSE ARRAY CSV
function parseArray(value){

  if(!value)
    return [];

  if(Array.isArray(value)){
    return value.map(normalize);
  }

  let text = String(value)
    .replace(/""/g,'"')
    .trim();

  try{
    const arr = JSON.parse(text);
    if(Array.isArray(arr)){
      return arr.map(normalize);
    }
  }
  catch(e){}

  return text
    .replace(/[\[\]]/g,"")
    .split(",")
    .map(normalize)
    .filter(Boolean);
}




// ------------------------
// F1 SCORE PER MODELLO
function calculateF1(modelField){
  const scores = {};
  emotions.forEach(emotion=>{
    let TP = 0;
    let FP = 0;
    let FN = 0;
    props.history.forEach(row=>{
      const gt = parseArray(
        row.emotion_gt
      );
      const prediction = parseArray(
        row[modelField]
      );
      const actual =
        gt.includes(emotion);
      const predicted =
        prediction.includes(emotion);
      if(actual && predicted)
        TP++;
      if(!actual && predicted)
        FP++;
      if(actual && !predicted)
        FN++;
    });
    const precision =
      TP + FP === 0 ?
      0 :
      TP / (TP + FP);

    const recall =
      TP + FN === 0 ?
      0 :
      TP / (TP + FN);

    const f1 =
      precision + recall === 0 ?
      0 :
      2 *
      (precision * recall) /
      (precision + recall);

    scores[emotion] =
      Number((f1 * 100).toFixed(2));

  });

  return scores;
}





// ------------------------
// F1 RESULTS
const f1Scores = computed(()=>{
  return {
    pipeline:
      calculateF1("Emotion_Pipeline"),

    roberta:
      calculateF1("Emotion_Roberta"),

    qwen:
      calculateF1("Emotion_Qwen")
  };
});





// ------------------------
// CHART DATA
const chartData = computed(()=>({ 
  labels: emotions,
  datasets:[
    {
      label:"Pipeline F1 %",
      data:emotions.map(e=>f1Scores.value.pipeline[e]),
      backgroundColor:"#4F46E5",
      borderRadius:8
    },
    {
      label:"Roberta F1 %",
      data:emotions.map(e=>f1Scores.value.roberta[e]),
      backgroundColor:"#10B981",
      borderRadius:8
    },
    {
      label:"Qwen F1 %",
      data:emotions.map(e=>f1Scores.value.qwen[e]),
      backgroundColor:"#F59E0B",
      borderRadius:8
    }
  ]
}));

const chartOptions={
  responsive:true,
  maintainAspectRatio:false,
  plugins:{
    title:{
      display:true,
      text:"F1-score per emozione"
    }
  },
  scales:{
    y:{
      beginAtZero:true,
      max:100
    }
  },
  datasets:{
    bar:{
      barThickness:25,
      maxBarThickness:40
    }
  }
};

</script>



<template>

  <div class="rounded-2xl bg-white shadow-lg p-6 h-[450px]">


    <Bar
    :data="chartData"
    :options="chartOptions"
    />


  </div>


</template>