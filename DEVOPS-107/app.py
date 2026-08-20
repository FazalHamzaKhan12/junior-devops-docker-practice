import os
import secrets
from urllib.parse import urlsplit

import redis
from flask import Flask, abort, flash, redirect, render_template, request, url_for
from redis.exceptions import RedisError
from werkzeug.middleware.proxy_fix import ProxyFix


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "devops-107-practice-key")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024

# One trusted Nginx proxy sits in front of this Flask application.
app.wsgi_app = ProxyFix(
    app.wsgi_app,
    x_for=1,
    x_proto=1,
    x_host=1,
)

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    decode_responses=True,
    socket_connect_timeout=3,
    socket_timeout=3,
)


def is_valid_url(value):
    try:
        parsed = urlsplit(value)
        return parsed.scheme in {"http", "https"} and bool(parsed.netloc)
    except ValueError:
        return False


def create_unique_code():
    for _ in range(10):
        code = secrets.token_urlsafe(4).rstrip("_-")
        if code and not redis_client.exists(f"url:{code}"):
            return code
    raise RuntimeError("Unable to generate a unique short code")


def load_recent_links():
    links = []
    codes = redis_client.lrange("recent_codes", 0, 2)

    for code in codes:
        destination = redis_client.get(f"url:{code}")
        if destination:
            links.append(
                {
                    "code": code,
                    "destination": destination,
                    "clicks": int(redis_client.get(f"clicks:{code}") or 0),
                }
            )

    return links


@app.route("/", methods=["GET", "POST"])
def index():
    generated_link = None
    redis_connected = False
    recent_links = []

    try:
        redis_connected = bool(redis_client.ping())

        if request.method == "POST":
            destination = request.form.get("url", "").strip()

            if not destination:
                flash("Enter a URL to shorten.", "error")
            elif len(destination) > 2048:
                flash("That URL is too long.", "error")
            elif not is_valid_url(destination):
                flash("Use a complete URL beginning with http:// or https://.", "error")
            else:
                code = create_unique_code()
                pipeline = redis_client.pipeline()
                pipeline.set(f"url:{code}", destination)
                pipeline.lpush("recent_codes", code)
                pipeline.ltrim("recent_codes", 0, 49)
                pipeline.execute()

                generated_link = {
                    "code": code,
                    "short_url": url_for(
                        "follow_short_link",
                        code=code,
                        _external=True,
                    ),
                    "destination": destination,
                }
                flash("Your short link is ready.", "success")

        recent_links = load_recent_links()
    except (RedisError, RuntimeError) as error:
        app.logger.error("Redis operation failed: %s", error)
        redis_connected = False

    return render_template(
        "index.html",
        generated_link=generated_link,
        recent_links=recent_links,
        redis_connected=redis_connected,
    )


@app.get("/health")
def health():
    try:
        if redis_client.ping():
            return {
                "application": "healthy",
                "redis": "connected",
                "project": "DEVOPS-107",
            }, 200
    except RedisError:
        pass

    return {
        "application": "healthy",
        "redis": "unavailable",
        "project": "DEVOPS-107",
    }, 503


@app.get("/<code>")
def follow_short_link(code):
    try:
        destination = redis_client.get(f"url:{code}")
        if not destination:
            abort(404)

        redis_client.incr(f"clicks:{code}")
        return redirect(destination)
    except RedisError:
        abort(503)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
