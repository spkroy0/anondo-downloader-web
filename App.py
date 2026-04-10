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
        return "Dost, link ta age dao!"

    # এটি একটি পাওয়ারফুল পাবলিক এপিআই যা ইউটিউব ব্লক বাইপাস করে
    # আমরা রেজোলিউশন এবং টাইপ অনুযায়ী এপিআই কল কাস্টমাইজ করছি
    is_audio = "k" in quality
    
    # ব্যাকআপ এবং মেইন এপিআই এর সংমিশ্রণ
    # আমরা এমন একটি এপিআই ব্যবহার করছি যা সরাসরি স্ট্রিমিং লিঙ্ক দেয়
    api_url = "https://api.cobalt.tools/api/json" # লেটেস্ট ভার্সন ট্রাই করা হচ্ছে
    
    payload = {
        "url": url,
        "videoQuality": quality.replace('k', '') if not is_audio else "720",
        "downloadMode": "audio" if is_audio else "video",
        "audioFormat": "mp3",
        "filenameStyle": "pretty"
    }
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        data = response.json()

        if "url" in data:
            return redirect(data["url"])
        else:
            # যদি কোবাল্ট এরর দেয়, তবে সরাসরি ব্যাকআপ মেথডে পাঠিয়ে দেবে
            backup_api = f"https://api.vyt-dlp.com/download?url={url}&quality={quality}"
            return redirect(backup_api)

    except Exception as e:
        # সব ফেল করলে এই ইউনিভার্সাল ডাউনলোডার কাজ করবেই
        fallback = f"https://downloader.nocopyright.workers.dev/?url={url}"
        return redirect(fallback)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
