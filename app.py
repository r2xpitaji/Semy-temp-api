from flask import Flask, request, jsonify
import httpx
import json

# BASE API FOR TEMP-MAIL
BASE = "https://api.internal.temp-mail.io/api/v3"

app = Flask(__name__)

# ----------------------------------------
# HOME
# ----------------------------------------
@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "api": "Temp-Mail Internal Clone",
        "developer": "SEMY"
    })


# ----------------------------------------
# GENERATE TEMP MAIL  (/semy)
# ----------------------------------------
@app.route("/semy")
def create_mail():
    try:
        r = httpx.post(f"{BASE}/email/new")
        data = r.json()
        data["developer"] = "DEVELOPER SEMY"
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ----------------------------------------
# INBOX  (/inbox?email=xxxx)
# ----------------------------------------
@app.route("/inbox")
def inbox():
    email = request.args.get("email")

    if not email:
        return jsonify({
            "error": "❌ Please create an email first",
            "developer": "DEVELOPER SEMY"
        }), 400

    try:
        r = httpx.get(f"{BASE}/email/{email}/messages")
        msgs = r.json()

        return jsonify({
            "email": email,
            "messages": msgs,
            "developer": "DEVELOPER SEMY"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ----------------------------------------
# READ SINGLE MESSAGE (OPTIONAL)
# ----------------------------------------
@app.route("/message")
def message():
    email = request.args.get("email")
    msg_id = request.args.get("id")

    if not email or not msg_id:
        return jsonify({"error": "Email & id required"}), 400

    try:
        r = httpx.get(f"{BASE}/email/{email}/messages/{msg_id}")
        data = r.json()
        data["developer"] = "DEVELOPER SEMY"
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ----------------------------------------
# VERCEL HANDLER (IMPORTANT)
# ----------------------------------------
from vercel_wsgi import handle_request

def handler(request, context):
    return handle_request(app, request, context)


# ----------------------------------------
# LOCAL TEST RUN (optional)
# ----------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)