# AI Personalised Exam Revision Planner

A small full-stack study planner for creating an exam revision timetable. The React interface collects the subject, course context, exam date range, daily study time, and confidence for each topic. A Python Flask backend asks a local Ollama model to suggest topics, then creates a confidence-based schedule.

## Features

- React frontend with a responsive form and timetable view
- Python Flask backend with topic-generation and timetable endpoints
- Local AI topic suggestions through Ollama, without OpenAI API credits
- Manual topic entry if Ollama is not running
- More study time for topics with lower confidence
- Downloadable, separate text timetable for each plan

## Requirements

- Python 3.10 or newer
- Node.js and npm
- Ollama for local AI topic generation

## Setup

### 1. Install and download the local model

Install Ollama for Windows from https://ollama.com/download/windows. Then open Command Prompt and run:

    ollama run qwen3:4b

Wait for the model download to finish. You can exit the model prompt after it responds.

### 2. Start the backend

Open a Command Prompt in the project folder and run:

    cd backend
    py -m venv .venv
    .venv\Scripts\activate
    py -m pip install -r requirements.txt
    py app.py

The backend runs at http://127.0.0.1:5000.

### 3. Start the frontend

Open a second Command Prompt in the project folder and run:

    cd frontend
    npm install
    npm run dev

Open the local URL shown by Vite, usually http://localhost:5173.

## How to use

1. Enter your name, subject, course context, exam days, and available daily hours.
2. Ask the local model to suggest topics. If Ollama is unavailable, enter topics manually.
3. Rate confidence for each topic from 1 to 5.
4. Create the timetable and download it as a text file.

## Notes

The suggested topics are general AI suggestions, not a guaranteed copy of your institution's syllabus. Check them against your official course materials. Local model speed depends on your computer hardware. No OpenAI API key is used by this web version.

## Project structure

    backend/
      app.py
      requirements.txt
    frontend/
      index.html
      package.json
      package-lock.json
      src/
        App.jsx
        main.jsx
        styles.css
      vite.config.js
    main.py
    README.md
    .gitignore
