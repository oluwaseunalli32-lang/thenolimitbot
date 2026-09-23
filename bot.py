import os
import time
import requests
from openai import OpenAI

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

SYSTEM_PROMPT = (
    "Rewrite the user's text so it sounds natural and human-written. "
    "Keep the meaning. Use contractions. Vary sentence length. "
    "Don't add explanations, just return the rewritten text."
)

def humanize(text):
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.8,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
    )
    return r.choices[0].message.content.strip()

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
