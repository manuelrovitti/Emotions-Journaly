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

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

const props = defineProps({
  history: {
    type: Array,
    required: true
  }
});

// --------------------
// NORMALIZE
// --------------------
function normalize(x) {
  return String(x || "")
    .toLowerCase()
    .replace(/["'\[\]]/g, "")
    .trim();
}

// --------------------
// SAFE JSON PARSER
// --------------------
function safeParse(value) {
  if (!value) return [];

  try {
    const cleaned = String(value)
      .replace(/""/g, '"')
      .replace(/'/g, '"')
      .trim();

    return JSON.parse(cleaned);
  } catch {
    return null;
  }
}

// --------------------
// GT PARSER
// --------------------
function normalizeArray(value) {
  if (!value) return [];

  if (Array.isArray(value)) {
    return value.map(normalize);
  }

  try {
    return JSON.parse(value).map(normalize);
  } catch {
    return String(value)
      .replace(/[\[\]']/g, "")
      .split(",")
      .map(normalize)
      .filter(Boolean);
  }
}

// --------------------
// PIPELINE / QWEN
// --------------------
function parseSingle(value) {
  return normalize(value);
}

// --------------------
// ROBERTA PARSER (ARRAY + OBJECT SAFE)
// --------------------
function parseRoberta(value) {
  const parsed = safeParse(value);
  if (!parsed) return [];

  if (Array.isArray(parsed)) {
    return parsed.map(normalize);
  }

  if (typeof parsed === "object") {
    return Object.keys(parsed).map(normalize);
  }

  return [];
}

// --------------------
// ACCURACY
// --------------------
const accuracy = computed(() => {
  const total = props.history.length;

  let pipeline = 0;
  let roberta = 0;
  let qwen = 0;

  for (const item of props.history) {
    const gt = normalizeArray(item.G_T);

    const p = parseSingle(item.Emotion_Pipeline);
    const q = parseSingle(item.Emotion_Qwen);
    const r = parseRoberta(item.Emotion_Roberta);

    // DEBUG unico (facoltativo)
    console.log("GT:", gt, "PIPE:", p, "QWEN:", q, "ROBERTA:", r);

    if (gt.includes(p)) pipeline++;
    if (gt.includes(q)) qwen++;
    if (r.some(x => gt.includes(x))) roberta++;
  }

  return {
    pipeline: total ? (pipeline / total) * 100 : 0,
    roberta: total ? (roberta / total) * 100 : 0,
    qwen: total ? (qwen / total) * 100 : 0
  };
});

// --------------------
// CHART DATA
// --------------------
const chartData = computed(() => ({
  labels: ["Pipeline", "Roberta", "Qwen"],
  datasets: [
    {
      label: "Accuracy %",
      data: [
        accuracy.value.pipeline,
        accuracy.value.roberta,
        accuracy.value.qwen
      ],
      backgroundColor: [
        "#4F46E5", // Pipeline
        "#10B981", // Roberta
        "#F59E0B"  // Qwen 
      ],
      borderRadius: 8
    }
  ]
}));

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    title: {
      display: true,
      text: "Model Accuracy vs Ground Truth"
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      max: 100
    }
  },
  datasets: {
    bar: {
      barThickness: 40,  
      maxBarThickness: 60
    }
  }
};
</script>

<template>
  <div class="rounded-2xl bg-white shadow-lg p-6 h-[350px]">
    <Bar :data="chartData" :options="chartOptions" />
  </div>
</template>