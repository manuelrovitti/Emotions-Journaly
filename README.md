# Vue 3 + Vite

This template should help get you started developing with Vue 3 in Vite. The template uses Vue 3 `<script setup>` SFCs, check out the [script setup docs](https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup) to learn more.

Learn more about IDE Support for Vue in the [Vue Docs Scaling up Guide](https://vuejs.org/guide/scaling-up/tooling.html#ide-support).

# avvio 
su AC:
- npm run dev -- --host

su AC_B:
- python -m pip install fastapi pydantic transformers torch pandas uvicorn[standard]
python -m pip install requests
- uvicorn server:app --host 0.0.0.0 --port 8000

# Models
- pipeline : "arpanghoshal/EkmanClassifier":
    ## Learning

- HuggingFace: "emotion-english-distilroberta-base"
    ## Learning
    Addestrato su testo in inglese, tali testi sono stati presi da X (Twittter), Reddit, auto-rapporti degli studenti e dialoghi televisivi.
    ### Struttura Output
    Array con etichetta + puntteggio, il punteggio indica la probabilita' di corrrispondenza.

- HuggingFace: 
    ## Learning