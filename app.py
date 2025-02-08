from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

@app.route('/static/fonts/<path:filename>')
def serve_fonts(filename):
    return send_from_directory('static/fonts', filename)

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)