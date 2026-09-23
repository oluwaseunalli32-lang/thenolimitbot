import os
import time
import requests
import google.generativeai as genai

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
GEMINI_KEY = os.environ["GEMINI_API_KEY"]

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

PROMPT = (
    "Rewrite the following text so it sounds natural and human-written. "
    "Keep the meaning. Use contractions. Vary sentence length. "
    "Return only the rewritten text, nothing else:\n\n{text}"
)

def humanize(text):
    r = model.generate_content(PROMPT.format(text=text))
    return r.text.strip()

def send(chat_id, text):
    requests.post(f"{API}/sendMessage", json={"chat_id": chat_id, "text": text})

def main():
    offset = 0
    print("Bot running...")
    while True:
        try:
            r = requests.get(
                f"{API}/getUpdates",
                params={"offset": offset, "timeout": 30},
                timeout=40,
            )
            for update in r.json().get("result", []):
                offset = update["update_id"] + 1
                msg = update.get("message")
                if not msg or "text" not in msg:
                    continue
                chat_id = msg["chat"]["id"]
                try:
                    send(chat_id, humanize(msg["text"]))
                except Exception as e:
                    send(chat_id, f"Error: {e}")
        except Exception as e:
            print("Loop error:", e)
            time.sleep(5)

if __name__ == "__main__":
    main()
