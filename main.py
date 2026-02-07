import json
import requests

# BASE API
BASE_URL = "https://api.internal.temp-mail.io/api/v3"


def handler(request):
    path = request["path"]
    query = request.get("query", {})

    # -------------------------
    # GENERATE EMAIL: /semy
    # -------------------------
    if path == "/semy":
        try:
            r = requests.post(f"{BASE_URL}/email/new")
            data = r.json()

            data["developer"] = "DEVELOPER SEMY"
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps(data)
            }

        except Exception as e:
            return {"statusCode": 500, "body": str(e)}

    # -------------------------
    # GET INBOX: /inbox?email=
    # -------------------------
    if path == "/inbox":
        email = query.get("email")

        if not email:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "email parameter missing"})
            }

        try:
            r = requests.get(f"{BASE_URL}/email/{email}/messages")
            data = r.json()

            out = {
                "email": email,
                "messages": data,
                "developer": "DEVELOPER SEMY"
            }

            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps(out)
            }

        except Exception as e:
            return {"statusCode": 500, "body": str(e)}

    # Default Route
    return {"statusCode": 404, "body": "Invalid Route"}