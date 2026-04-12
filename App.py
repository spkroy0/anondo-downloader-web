import os
from flask import Flask, render_template, make_response
from flask_compress import Compress

app = Flask(__name__)

# সাইট দ্রুত লোড হওয়ার জন্য কম্প্রেশন
Compress(app)

@app.route('/')
def index():
    # মেইন পেজ রেন্ডার এবং সিকিউরিটি হেডার সেটআপ
    response = make_response(render_template('index.html'))
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    return response

# এরর হ্যান্ডলিং
@app.errorhandler(404)
def not_found(e):
    return "<h1>Page Not Found!</h1><a href='/'>Go Home</a>", 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
