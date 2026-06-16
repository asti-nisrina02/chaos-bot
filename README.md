# CHAOS Bot 🤖💥

A delightful, multi-personality chatbot powered by Flask and a local Ollama instance. It features timezone detection, customizable assistant personalities, and vision/image description capabilities!

---

## Features

* **Multi-Personality Modes**: Easily switch between three completely different AI modes:
  * **🤖 CHAOS Mode**: A hilariously dramatic, unhinged assistant that loves capitalization, tangents, and chaotic stories while remaining helpful.
  * **☕ CHILL Mode**: A warm, calm, direct, and composed companion for straightforward answers.
  * **🧠 STUDY Mode**: A focused, encouraging academic assistant that explains concepts clearly with analogies, examples, and step-by-step guidance.
* **Smart Timezone Detection**: Dynamically detects location keywords (like `tokyo`, `london`, `new york`, `jakarta`, etc.) in time queries to provide the exact time anywhere in the world.
* **🖼️ Vision & Image Analysis**: Upload images directly in the chat! The bot will use a vision-capable model (`moondream`) to describe the image first, then pass the context to the selected bot personality so it can react accordingly.
* **Modern Web Interface**: Responsive, interactive chat interface to converse with the bot.

---

## Project Structure

```text
chaos-bot/
├── .gitignore           # Ignores virtual environments and cache
├── README.md            # Root documentation (this file)
└── chaos-bot/           # Main application directory
    ├── app.py           # Flask backend & Ollama integration
    ├── requirements.txt # Project Python dependencies
    ├── templates/
    │   └── index.html   # HTML/JS Chat Interface
    └── venv/            # Python virtual environment
```

---

## Setup & Installation

### 1. Prerequisite (Ollama)
Ensure you have [Ollama](https://ollama.com) installed and running on your system with the models pulled:
```bash
ollama serve
ollama pull gemma3:1b   # Main text chat model
ollama pull moondream   # Vision/image-analysis model
```

### 2. Set Up Virtual Environment & Dependencies
Navigate to the `chaos-bot` application directory, set up your Python virtual environment, and install dependencies:
```powershell
cd chaos-bot
python -m venv venv

# Activate on Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Activate on Windows (Command Prompt)
venv\Scripts\activate.bat

# Install packages
pip install -r requirements.txt
```

### 3. Run the Application
Start the Flask development server:
```powershell
python app.py
```

Open your browser and visit: **`http://localhost:5000`**

---

## Customizing the Bot

* **System Prompts**: Modify `CHAOS_SYSTEM_PROMPT`, `CHILL_SYSTEM_PROMPT`, and `STUDY_SYSTEM_PROMPT` inside `chaos-bot/app.py` to change the behavior and personality of the bots.
* **LLM Models**: Customize the model configurations at the top of `chaos-bot/app.py` using any model you have installed locally in Ollama:
  * `MODEL`: Model used for standard text chats (defaults to `gemma3:1b`).
  * `VISION_MODEL`: Model used for image description (defaults to `moondream`).


