# CHAOS Bot 🤖💥

A chaotic, funny AI chatbot powered by Ollama + Flask.

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Make sure Ollama is running with gemma3:4b
```bash
ollama serve
ollama pull gemma3:4b   # skip if you already have it
```

### 3. Run the bot
```bash
python app.py
```

### 4. Open your browser
Go to: http://localhost:5000

---

## Want to change the personality?
Edit the `CHAOS_SYSTEM_PROMPT` in `app.py` — that's where all the personality lives!

## Want to use a different model?
Change the `MODEL` variable at the top of `app.py`:
```python
MODEL = "gemma3:4b"   # change to any model you have in Ollama
```

## Project structure
```
chaos-bot/
├── app.py              # Flask backend + Ollama connection
├── requirements.txt    # Python dependencies
├── README.md
└── templates/
    └── index.html      # Chat UI
```
