import os
from flask import Flask, render_template, request, send_file
import yt_dlp

app = Flask(__name__)

# ডাউনলোড ফোল্ডার তৈরি
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    choice = request.form.get('format_type')
    
    # ভিডিও না অডিও তা চেক করা
    is_audio = choice.endswith('a')
    quality = choice.replace('a', '')

    ydl_opts = {
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'quiet': True,
        'noplaylist': True,
    }

    if is_audio:
        # অডিও ডাউনলোডের লজিক
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': quality,
            }],
        })
    else:
        # ভিডিও ডাউনলোডের লজিক
        if quality == "144":
            # ১৪৪পি-র জন্য ৩জিপি বা ছোট এমপি৪ ট্রাই করবে
            ydl_opts['format'] = 'best[height<=144][ext=3gp]/best[height<=144]'
        else:
            # অন্যান্য রেজোলিউশনের জন্য
            ydl_opts['format'] = f'bestvideo[height<={quality}][ext=mp4]+bestaudio[ext=m4a]/best[height<={quality}]'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # অডিও হলে এক্সটেনশন এমপি৩ হবে
            if is_audio:
                filename = os.path.splitext(filename)[0] + ".mp3"

            return send_file(filename, as_attachment=True)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
