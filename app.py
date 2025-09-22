from flask import Flask, render_template, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import os

app = Flask(__name__)
app.secret_key = "SUPER_SECRET_KEY"

# OAuth إعداد
oauth = OAuth(app)
google = oauth.register(
    name="google",
    client_id="295275899887-iol0mlh8uv0nm9gf2mrfmsq76t95eod2.apps.googleusercontent.com",
    client_secret="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",
    access_token_url="https://oauth2.googleapis.com/token",
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    api_base_url="https://www.googleapis.com/oauth2/v2/",
    client_kwargs={"scope": "openid email profile"},
)

# بيانات روايات تجريبية
novels = [
    {"title": "رواية الصحراء", "author": "أحمد خالد", "summary": "قصة عن رحلة في عمق الصحراء."},
    {"title": "حكاية القمر", "author": "ليلى محمد", "summary": "أسطورة رومانسية تدور تحت ضوء القمر."},
    {"title": "أسرار البحر", "author": "سامي علي", "summary": "مغامرة مثيرة بين الأمواج."}
]

@app.route("/")
def home():
    user = session.get("user")
    return render_template("home.html", novels=novels, user=user)

@app.route("/login")
def login():
    redirect_uri = url_for("callback", _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route("/callback")
def callback():
    token = google.authorize_access_token()
    user_info = google.get("userinfo").json()
    session["user"] = user_info
    return redirect(url_for("home"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
