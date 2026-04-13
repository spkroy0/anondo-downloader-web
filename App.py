import os
from flask import Flask, render_template, make_response
from flask_compress import Compress

app = Flask(__name__)
Compress(app)

@app.route('/')
def index():
    response = make_response(render_template('index.html'))
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    return response

# --- C Editor এর জন্য নতুন রুট ---
@app.route('/c-editor')
def c_editor():
    # এটি templates ফোল্ডার থেকে c_editor.html ফাইলটি লোড করবে
    response = make_response(render_template('c_editor.html'))
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    return response

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # প্রোডাকশন এনভায়রনমেন্টে debug=False রাখা ভালো
    app.run(host='0.0.0.0', port=port, debug=False)
