import json
import requests

BASE_URL = "https://api.internal.temp-mail.io/api/v3"

def handler(request):
    path = request["path"]
    query = request.get("query", {})

    # /semy → generate mail
    if path == "/semy":
        r = requests.post(f"{BASE_URL}/email/new")
        data = r.json()
        data["developer"] = "DEVELOPER SEMY"

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(data)
        }

    # /inbox?email=
    if path == "/inbox":
        email = query.get("email")
        if not email:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "success": False,
                    "message": "❌ Please create an email first",
                    "developer": "DEVELOPER SEMY"
                })
            }

        r = requests.get(f"{BASE_URL}/email/{email}/messages")
        msgs = r.json()

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "email": email,
                "messages": msgs,
                "developer": "DEVELOPER SEMY"
            })
        }

    return {
        "statusCode": 404,
        "body": "Route not found"
    }