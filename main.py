import json
import httpx

BASE = "https://api.internal.temp-mail.io/api/v3"

def handler(request):

    path = request.get("path", "")
    query = request.get("query", {})

    # -------------------------
    # /semy
    # -------------------------
    if path == "/semy":
        res = httpx.post(f"{BASE}/email/new")
        data = res.json()
        data["developer"] = "DEVELOPER SEMY"
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(data)
        }

    # -------------------------
    # /inbox
    # -------------------------
    if path == "/inbox":
        email = query.get("email")
        if not email:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "error": "❌ Please create an email first",
                    "developer": "DEVELOPER SEMY"
                })
            }
        res = httpx.get(f"{BASE}/email/{email}/messages")
        msgs = res.json()

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "email": email,
                "messages": msgs,
                "developer": "DEVELOPER SEMY"
            })
        }

    # -------------------------
    # DEFAULT
    # -------------------------
    return {
        "statusCode": 404,
        "headers": {"Content-Type": "text/plain"},
        "body": "Route Not Found"
    }
