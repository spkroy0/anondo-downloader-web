import os
from flask import Flask, render_template, make_response
from flask_compress import Compress

app = Flask(__name__)

# সাইট লোডিং স্পিড বাড়ানোর জন্য Gzip কম্প্রেশন
Compress(app)

# ব্রাউজার ক্যাশিং কনফিগারেশন (১ বছর স্ট্যাটিক ফাইল সেভ থাকবে)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000

@app.route('/')
def index():
    """মেইন এডিটর পেজ এবং সিকিউরিটি হেডার সেটআপ"""
    response = make_response(render_template('index.html'))
    # সিকিউরিটি হেডারস
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Server'] = 'Anondo-Pro-RGB-v2.5'
    return response

@app.errorhandler(404)
def page_not_found(e):
    return """
    <body style="background:#0b1120; color:white; display:flex; justify-content:center; align-items:center; height:100vh; font-family:sans-serif; flex-direction:column; text-align:center;">
        <h1 style="color:#ef4444; font-size:60px; margin-bottom:10px;">404</h1>
        <p style="font-size:18px;">Oi bhai, vul rasta e aisa porson! Link check koro.</p>
        <a href="/" style="margin-top:25px; color:#38bdf8; text-decoration:none; border:1px solid #38bdf8; padding:12px 30px; border-radius:30px; transition:0.3s; font-weight:bold;">Home e Fire Jao</a>
    </body>
    """, 404

if __name__ == "__main__":
    # Render বা Heroku এর জন্য পোর্ট অটো-ডিটেকশন
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
