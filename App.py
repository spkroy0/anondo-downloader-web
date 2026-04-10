import os
from flask import Flask, render_template, request, send_file
import yt_dlp

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    choice = request.form.get('format_type')
    
    if not url:
        return "URL missing!"

    ydl_opts = {
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'referer': 'https://www.google.com/',
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'nocheckcertificate': True,
        'quiet': True,
    }

    # অডিও অপশন চেক (যদি মান এর শেষে 'k' থাকে)
    if choice.endswith('k'):
        bitrate = choice.replace('k', '')
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': bitrate,
            }],
        })
    # ভিডিও অপশন (3gp বা mp4)
    else:
        quality = choice.replace('3gp', '')
        if '3gp' in choice:
            # 3GP ফরম্যাট সাধারণত কম রেজোলিউশনে থাকে
            ydl_opts['format'] = f'bestvideo[ext=3gp][height<={quality}]+bestaudio/best[height<={quality}]/best[ext=3gp]'
        else:
            ydl_opts['format'] = f'bestvideo[height<={quality}][ext=mp4]+bestaudio[ext=m4a]/best[height<={quality}]'
            ydl_opts['merge_output_format'] = 'mp4'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            if choice.endswith('k'):
                filename = os.path.splitext(filename)[0] + ".mp3"
            elif '3gp' in choice and not filename.endswith('.3gp'):
                filename = os.path.splitext(filename)[0] + ".3gp"

            return send_file(filename, as_attachment=True)
            
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run()
