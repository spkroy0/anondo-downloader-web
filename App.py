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
    choice = request.form.get('format_type')
    
    if not url:
        return "Link কই ভাই? আগে লিঙ্ক দিন!"

    # নতুন আপডেট করা এপিআই এন্ডপয়েন্ট
    api_url = "https://api.cobalt.tools/api/json"
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    # অডিও নাকি ভিডিও চেক
    is_audio = True if 'k' in choice else False
    
    payload = {
        "url": url,
        "videoQuality": choice if not is_audio else "720",
        "downloadMode": "audio" if is_audio else "video",
        "audioFormat": "mp3",
        "filenameStyle": "pretty"
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        result = response.json()

        # নতুন রেসপন্স ফরম্যাট অনুযায়ী চেক
        if "url" in result:
            return redirect(result["url"])
        elif "text" in result:
            return f"Error: {result['text']}"
        else:
            return "দুঃখিত, ডাউনলোড লিঙ্ক পাওয়া যায়নি। আবার চেষ্টা করুন।"

    except Exception as e:
        return f"সার্ভার এরর: {str(e)}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
