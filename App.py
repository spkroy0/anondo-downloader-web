import os
from flask import Flask, render_template, make_response
from flask_compress import Compress

app = Flask(__name__)

# সাইট ফাস্ট করার জন্য কমপ্রেশন এনাবল করা
Compress(app)

# ক্যাশ মেমোরি অপ্টিমাইজেশন (১ বছর)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000

@app.route('/')
def index():
    """মেইন এডিটর পেজ লোড এবং সিকিউরিটি হেডার সেটআপ"""
    response = make_response(render_template('index.html'))
    
    # সিকিউরিটি এবং কাস্টম হেডারস
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Server'] = 'Anondo Pro Server 1.0'
    
    return response

@app.errorhandler(404)
def page_not_found(e):
    # ইনলাইন স্টাইল ঠিক আছে, তবে বডি ক্লোজিং ট্যাগ এবং স্ট্রাকচার আরও ক্লিন করা হয়েছে
    html_404 = """
    <!DOCTYPE html>
    <html>
    <head><title>404 - Not Found</title></head>
    <body style="background:#0b1120; color:white; display:flex; justify-content:center; align-items:center; height:100vh; font-family:sans-serif; flex-direction:column; margin:0;">
        <h1 style="color:#38bdf8; font-size: 3rem; margin-bottom:10px;">404</h1>
        <h2 style="margin-bottom:20px;">Lost in Code?</h2>
        <p style="margin-bottom:30px; opacity:0.8;">Oi bhai, vul rasta e aisa porson! Link check koro.</p>
        <a href="/" style="color:#38bdf8; text-decoration:none; border:2px solid #38bdf8; padding:12px 24px; border-radius:8px; font-weight:bold; transition: 0.3s;">Home e Fire Jao</a>
    </body>
    </html>
    """
    return html_404, 404

if __name__ == "__main__":
    # পোর্ট ডিটেকশন এবং সার্ভার রান
    port = int(os.environ.get("PORT", 5000))
    # ডিবাগ মোড ফলস রাখা হয়েছে প্রোডাকশনের জন্য
    app.run(host='0.0.0.0', port=port, debug=False)
