import os
import json
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# === CONFIGURACIÓN ===
YOUTUBE_CHANNEL_ID = "UCy01uEQKAjnfiXIZQ8ydJPg"  # Tu canal, hardcodeado
TELEGRAM_CHANNEL = "@en_solitario"
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]  # Secreto en GitHub
LAST_VIDEO_FILE = "last_video.json"

FEED_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={YOUTUBE_CHANNEL_ID}"


def get_latest_video():
    response = requests.get(FEED_URL, timeout=10)
    response.raise_for_status()

    ns = {
        "atom": "http://www.w3.org/2005/Atom",
        "yt": "http://www.youtube.com/xml/schemas/2015",
    }

    root = ET.fromstring(response.content)
    entry = root.find("atom:entry", ns)

    if entry is None:
        return None

    video_id = entry.find("yt:videoId", ns).text
    title = entry.find("atom:title", ns).text
    link = entry.find("atom:link", ns).attrib["href"]
    published = entry.find("atom:published", ns).text

    return {"id": video_id, "title": title, "link": link, "published": published}


def get_last_sent_id():
    if os.path.exists(LAST_VIDEO_FILE):
        with open(LAST_VIDEO_FILE, "r") as f:
            data = json.load(f)
            return data.get("last_id")
    return None


def save_last_sent_id(video_id):
    with open(LAST_VIDEO_FILE, "w") as f:
        json.dump({"last_id": video_id}, f)


def send_telegram_message(title, link):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    text = f"🎬 *{title}*\n\n{link}"
    payload = {
        "chat_id": TELEGRAM_CHANNEL,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False,
    }
    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()
    print(f"✅ Mensaje enviado: {title}")


def main():
    print(f"🔍 Revisando canal: {YOUTUBE_CHANNEL_ID}")
    video = get_latest_video()

    if not video:
        print("No se encontró ningún video.")
        return

    last_id = get_last_sent_id()

    if video["id"] == last_id:
        print("No hay videos nuevos.")
        return

    print(f"🆕 Nuevo video detectado: {video['title']}")
    send_telegram_message(video["title"], video["link"])
    save_last_sent_id(video["id"])


if __name__ == "__main__":
    main()
