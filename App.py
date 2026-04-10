import os
import requests
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    quality = request.form.get('format_type')

    if not url:
        return "URL কই দোস্ত? আগে লিঙ্ক দাও!"

    # Snaptube স্টাইল API (Cobalt Updated Instance)
    api_url = "https://api.cobalt.tools/api/json"
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
    }
    
    is_audio = "k" in quality
    
    payload = {
        "url": url,
        "videoQuality": quality.replace('k', '') if not is_audio else "720",
        "downloadMode": "audio" if is_audio else "video",
        "audioFormat": "mp3",
        "filenameStyle": "pretty",
        "youtubeVideoCodec": "h264",
        "isAudioMuted": False
    }

    try:
        # মেইন এপিআই কল
        response = requests.post(api_url, headers=headers, json=payload, timeout=12)
        
        if response.status_code == 200:
            result = response.json()
            if "url" in result:
                return redirect(result["url"])
        
        # ব্যাকআপ ১: Snaptube এর মতো প্রক্সি সার্ভিস
        fallback_url = f"https://downloader.nocopyright.workers.dev/?url={url}"
        return redirect(fallback_url)

    except:
        # ব্যাকআপ ২: কোনো কিছুই কাজ না করলে
        return redirect(f"https://www.y2mate.com/youtube-vi/{url.split('=')[-1]}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
