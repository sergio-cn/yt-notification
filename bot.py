import os
import json
import requests
import xml.etree.ElementTree as ET

YOUTUBE_CHANNEL_ID = "UCy01uEQKAjnfiXIZQ8ydJPg"
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
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

    return {"id": video_id, "title": title, "link": link}


def get_last_sent_id():
    if os.path.exists(LAST_VIDEO_FILE):
        with open(LAST_VIDEO_FILE, "r") as f:
            return json.load(f).get("last_id")
    return None


def save_last_sent_id(video_id):
    with open(LAST_VIDEO_FILE, "w") as f:
        json.dump({"last_id": video_id}, f)


def send_telegram_message(title, link):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": "-1003797390603",
        "text": f"🎬 {title}\n\n{link}",
    }
    r = requests.post(url, json=payload, timeout=10)
    print(r.json())
    r.raise_for_status()
    print(f"✅ Enviado: {title}")


def main():
    video = get_latest_video()
    if not video:
        print("No se encontró ningún video.")
        return

    if video["id"] == get_last_sent_id():
        print("No hay videos nuevos.")
        return

    print(f"🆕 Nuevo video: {video['title']}")
    send_telegram_message(video["title"], video["link"])
    save_last_sent_id(video["id"])


if __name__ == "__main__":
    main()
