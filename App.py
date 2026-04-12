import os
from flask import Flask, render_template, make_response
from flask_compress import Compress

app = Flask(__name__)
Compress(app)

@app.route('/')
def index():
    # মেইন এডিটর পেজ এবং সিকিউরিটি হেডার
    response = make_response(render_template('index.html'))
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['Server'] = 'Anondo-Pro-v3.0'
    return response

@app.errorhandler(404)
def error_404(e):
    return "<h1>404 - Not Found</h1>", 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
