# Emotion Journaly
It began as a university project on affective computing, with the goal of allowing users to create their own collection of lived experiences along with the emotions associated with them. 
The possible emotions are those identified by Ekman, namely: JOY, SADNESS, ANGER, FEAR, DISGUST, SURPRISE and NEUTRAL.
This project does not have a true database; instead, everything is managed using a CSV file. Despite this, the data displayed (if you enter your name) consists exclusively of the information for that specific user.
The process is divided into two parts: 
- the first involves entering your first and last name and a sentence describing what you're experiencing at that moment; then, using three different models, the system will tell you the most likely or selected emotion.
- The second step (after the fact) is to select up to 3 emotions for the phrases you entered earlier.

## Structure
The project consists of a front end and a back end, AC and AC_B, respectively.

### Frontend
Vue 3 and Vite were used to build the front end, along with Tailwind for building reusable components.

### Backend
The backend consists of two components: `server.py`, which will handle the calls, and `csv_manager.py`, which manages the CSV files.
The models used for emotion recognition are:
- Pipeline: "arpanghoshal/EkmanClassifier" (LOCAL MODEL)
- HuggingFace: "emotion-english-distilroberta-base" (API)
- HuggingFace: Qwen (API)

# TEST
To test it, a Docker environment was created.

Two terminals are opened: one is used to access the frontend, and the other is used to access the backend.

In AC:
(grafici) => npm install chart.js vue-chartjs
- npm run dev -- --host

In AC_B:
- uvicorn server:app --host 0.0.0.0 --port 8000

To make API calls to HF, you must first create your own TOKEN on their website.