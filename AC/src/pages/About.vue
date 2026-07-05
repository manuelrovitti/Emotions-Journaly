<script setup>
    import { useSiteStore } from '../stores/HomeStore'

    const store = useSiteStore()
</script>

<template>
  <div
    class="min-h-screen flex items-center justify-center bg-cover bg-center p-6"
    :style="{ backgroundImage: `url(${store.bgImage})` }"
  >
    <!-- CARD TEXT-->
    <div class="w-full max-w-6xl bg-blue-200/90 backdrop-blur-md rounded-3xl shadow-2xl p-12 text-center">
      
      <h1 class="text-5xl font-bold mb-6 text-green-900">
        ABOUT
      </h1>

      <p class="text-lg leading-relaxed text-black">
        Questo progetto è dedicato all’analisi delle emozioni e all’elaborazione dei dati testuali.
        L’obiettivo è comprendere meglio il comportamento emotivo attraverso modelli di machine learning
        e tecniche di natural language processing.
        <br /><br />
        Il sistema permette di visualizzare statistiche, trend e insight in modo semplice e intuitivo,
        rendendo l’analisi accessibile anche a utenti non tecnici.
      </p>

    </div>
  </div>
</template>