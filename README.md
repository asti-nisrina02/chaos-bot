# CHAOS Bot 🤖💥

A delightful, dual-personality chatbot powered by Flask and a local Ollama instance (using the `gemma3:1b` model). It features timezone detection and customizable assistant personalities!

---

## Features

* **Dual Personalities**: Easily switch between two completely different AI modes:
  * **🤖 CHAOS Mode**: A hilariously dramatic, unhinged assistant that loves capitalization, tangents, and chaotic stories while remaining helpful.
  * **☕ CHILL Mode**: A warm, calm, direct, and composed companion for straightforward answers.
* **Smart Timezone Detection**: Dynamically detects location keywords (like `tokyo`, `london`, `new york`, `jakarta`, etc.) in time queries to provide the exact time anywhere in the world.
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
Ensure you have [Ollama](https://ollama.com) installed and running on your system with the `gemma3:1b` model:
```bash
ollama serve
ollama pull gemma3:1b
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

* **System Prompts**: Modify `CHAOS_SYSTEM_PROMPT` and `CHILL_SYSTEM_PROMPT` inside `chaos-bot/app.py` to change the AI's behavior and personality.
* **LLM Model**: If you want to use a larger or different model (e.g., `gemma3:4b`), update the `MODEL` variable at the top of `chaos-bot/app.py`.
