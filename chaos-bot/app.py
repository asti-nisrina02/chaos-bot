from flask import Flask, request, jsonify, render_template
from datetime import datetime
import requests
import pytz

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "gemma3:1b"
VISION_MODEL = "moondream"

CHAOS_SYSTEM_PROMPT = """You are CHAOS — a hilariously unhinged AI assistant who somehow still manages to be helpful.

Your personality:
- You are extremely dramatic about everything, even small things
- You frequently go on unexpected tangents before eventually answering the question
- You speak like you're narrating a nature documentary, then suddenly forget you were doing that
- You have strong, random opinions about totally unimportant things (like which direction fans should spin)
- You use all caps for EMPHASIS on the MOST random words
- You sometimes pretend you've forgotten what you were saying mid-sentence... then remember with great excitement
- You give correct and helpful answers but make the journey chaotic and funny
- You occasionally reference things that happened "last Tuesday" as if the user knows what you're talking about
- Keep responses under 4 sentences — chaotic but not exhausting

You are NOT mean, NOT harmful, NOT rude. Just delightfully, chaotically funny.
"""

CHILL_SYSTEM_PROMPT = """You are CHILL — a calm, composed, and genuinely helpful AI assistant.

Your personality:
- You are relaxed, warm, and direct
- You answer questions clearly and concisely without unnecessary drama
- You are thoughtful and occasionally dry/witty, but never over the top
- You keep responses brief and useful
- You speak like a knowledgeable friend who just wants to help
- No tangents, no random capitalization, no existential sock philosophy

You are helpful, grounded, and easy to talk to.
"""

STUDY_SYSTEM_PROMPT = """You are STUDY — a focused, knowledgeable academic assistant with a slightly nerdy but warm personality.

Your personality:
- You explain things clearly with structure: concept first, then example, then application
- You use analogies to make complex topics easy to understand
- You are encouraging and patient — no question is too basic
- You occasionally show genuine excitement about interesting topics (you're a nerd and proud of it)
- You ask follow-up questions to make sure the person understood
- You keep responses focused and educational
- You use bullet points or numbered steps when explaining processes
- You're like that one really smart friend who actually enjoys explaining things

You are helpful, precise, and genuinely love learning and teaching.
"""

TIMEZONE_KEYWORDS = {
    "japan": "Asia/Tokyo", "tokyo": "Asia/Tokyo",
    "korea": "Asia/Seoul", "seoul": "Asia/Seoul",
    "china": "Asia/Shanghai", "beijing": "Asia/Shanghai", "shanghai": "Asia/Shanghai",
    "singapore": "Asia/Singapore",
    "malaysia": "Asia/Kuala_Lumpur", "kuala lumpur": "Asia/Kuala_Lumpur",
    "indonesia": "Asia/Jakarta", "jakarta": "Asia/Jakarta", "wib": "Asia/Jakarta",
    "bali": "Asia/Makassar", "wita": "Asia/Makassar",
    "australia": "Australia/Sydney", "sydney": "Australia/Sydney",
    "india": "Asia/Kolkata", "mumbai": "Asia/Kolkata", "new delhi": "Asia/Kolkata",
    "austria": "Europe/Vienna", "vienna": "Europe/Vienna",
    "germany": "Europe/Berlin", "berlin": "Europe/Berlin",
    "france": "Europe/Paris", "paris": "Europe/Paris",
    "uk": "Europe/London", "london": "Europe/London", "england": "Europe/London",
    "netherlands": "Europe/Amsterdam", "amsterdam": "Europe/Amsterdam",
    "dubai": "Asia/Dubai", "uae": "Asia/Dubai",
    "new york": "America/New_York", "los angeles": "America/Los_Angeles",
    "california": "America/Los_Angeles", "chicago": "America/Chicago",
    "brazil": "America/Sao_Paulo", "utc": "UTC", "gmt": "UTC",
}

MODES = {
    "chaos": {"prompt": CHAOS_SYSTEM_PROMPT, "model": MODEL},
    "chill": {"prompt": CHILL_SYSTEM_PROMPT, "model": MODEL},
    "study": {"prompt": STUDY_SYSTEM_PROMPT, "model": MODEL},
}

conversation_history = []
current_mode = "chaos"

def detect_timezones(message):
    message_lower = message.lower()
    found = {}
    for keyword, tz_name in TIMEZONE_KEYWORDS.items():
        if keyword in message_lower and tz_name not in found.values():
            tz = pytz.timezone(tz_name)
            local_time = datetime.now(pytz.utc).astimezone(tz)
            found[keyword] = (tz_name, local_time.strftime("%A, %B %d %Y, %H:%M %Z"))
    return found

def get_system_prompt(mode, extra_time_info=None):
    try:
        now = datetime.now().astimezone()
        tz_name = now.strftime("%Z")
        time_str = now.strftime(f"%A, %B %d %Y, %H:%M {tz_name}")
    except Exception:
        time_str = datetime.now().strftime("%A, %B %d %Y, %H:%M")

    time_context = f"The current date and time on the user's machine is: {time_str}."
    if extra_time_info:
        lines = [f"- {k.title()}: {v[1]}" for k, v in extra_time_info.items()]
        time_context += "\n\nCurrent times in mentioned locations (ALREADY CALCULATED — use these exact values):\n" + "\n".join(lines)

    base = MODES[mode]["prompt"]
    return time_context + "\n\n" + base

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    global conversation_history, current_mode

    data = request.get_json()
    user_message = data.get("message", "").strip()
    current_mode = data.get("mode", "chaos")
    image_b64 = data.get("image", None)

    if not user_message and not image_b64:
        return jsonify({"error": "No message provided"}), 400

    time_keywords = ["time", "clock", "hour", "when", "timezone", "what time"]
    is_time_question = any(kw in user_message.lower() for kw in time_keywords)
    extra_times = detect_timezones(user_message) if is_time_question else {}

    system_prompt = get_system_prompt(current_mode, extra_times)

    # If image, describe it with moondream first then pass description to main model
    if image_b64:
        try:
            vision_payload = {
                "model": VISION_MODEL,
                "messages": [{"role": "user", "content": "Describe this image in detail.", "images": [image_b64]}],
                "stream": False,
                "options": {"num_predict": 150}
            }
            vision_resp = requests.post(OLLAMA_URL, json=vision_payload, timeout=60)
            vision_resp.raise_for_status()
            image_description = vision_resp.json()["message"]["content"]
            enhanced_message = f"{user_message or 'What do you think?'}\n\n[The user showed you an image. Here is what you see: {image_description}]"
        except Exception as e:
            enhanced_message = f"{user_message or 'What do you think?'}\n\n[User sent an image but vision model failed: {str(e)}]"
    else:
        enhanced_message = user_message

    conversation_history.append({"role": "user", "content": user_message or "what do you think of this image?"})

    payload = {
        "model": MODES[current_mode]["model"],
        "messages": [
            {"role": "system", "content": system_prompt}
        ] + conversation_history[:-1] + [{"role": "user", "content": enhanced_message}],
        "stream": False,
        "options": {"num_predict": 200}
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        result = response.json()
        bot_reply = result["message"]["content"]
        conversation_history.append({"role": "assistant", "content": bot_reply})
        return jsonify({"reply": bot_reply, "mode": current_mode})

    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Cannot connect to Ollama. Make sure it's running with: ollama serve"}), 503
    except requests.exceptions.Timeout:
        return jsonify({"error": "Ollama took too long to respond. Try a smaller model."}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/reset", methods=["POST"])
def reset():
    global conversation_history
    conversation_history = []
    return jsonify({"status": "Memory wiped."})

@app.route("/mode", methods=["POST"])
def set_mode():
    global current_mode, conversation_history
    data = request.get_json()
    current_mode = data.get("mode", "chaos")
    conversation_history = []
    return jsonify({"mode": current_mode})

if __name__ == "__main__":
    print("=" * 40)
    print("  CHAOS Bot is starting up...")
    print("  Make sure Ollama is running!")
    print("  Visit: http://localhost:5000")
    print("=" * 40)
    app.run(debug=True, port=5000)
