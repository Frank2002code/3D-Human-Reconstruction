# save this as app.py
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
@app.route("/hello")
def hello():
    return "Hello, World!"

@app.route("/showtext")
def showtext():
    html_str = "<html><body><h1>這是測試網頁</h1></body></html>"
    return html_str

@app.route("/home")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run()