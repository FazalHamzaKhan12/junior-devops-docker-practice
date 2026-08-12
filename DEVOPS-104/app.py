import os

import mysql.connector
from flask import Flask, flash, redirect, render_template, request, url_for
from mysql.connector import Error
from werkzeug.middleware.proxy_fix import ProxyFix


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "devops-104-practice-key")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024

# The application is expected to sit behind one trusted Nginx reverse proxy.
app.wsgi_app = ProxyFix(
    app.wsgi_app,
    x_for=1,
    x_proto=1,
    x_host=1,
)


def get_db_connection():
    """Connect to the MySQL container using Docker-network configuration."""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "mysql-db"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "appuser"),
        password=os.getenv("DB_PASSWORD", "app123"),
        database=os.getenv("DB_NAME", "company"),
        connection_timeout=5,
    )


def initialize_table(connection):
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS feedback (
            id INT AUTO_INCREMENT PRIMARY KEY,
            employee_name VARCHAR(100) NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    connection.commit()
    cursor.close()


def get_recent_feedback(connection):
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT employee_name, message, created_at
        FROM feedback
        ORDER BY id DESC
        LIMIT 3
        """
    )
    items = cursor.fetchall()
    cursor.close()
    return items


@app.route("/", methods=["GET", "POST"])
def index():
    connection = None

    try:
        connection = get_db_connection()
        initialize_table(connection)

        if request.method == "POST":
            employee_name = request.form.get("name", "").strip()
            message = request.form.get("feedback", "").strip()

            if not employee_name or not message:
                flash("Please complete both fields before submitting.", "error")
            elif len(employee_name) > 100 or len(message) > 1000:
                flash("Your name or feedback exceeds the allowed length.", "error")
            else:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO feedback (employee_name, message) VALUES (%s, %s)",
                    (employee_name, message),
                )
                connection.commit()
                cursor.close()
                flash("Your feedback was delivered successfully.", "success")
                return redirect(url_for("index"))

        return render_template(
            "index.html",
            database_connected=True,
            recent_feedback=get_recent_feedback(connection),
        )
    except Error as error:
        app.logger.error("Database connection failed: %s", error)
        return render_template(
            "index.html",
            database_connected=False,
            recent_feedback=[],
        )
    finally:
        if connection and connection.is_connected():
            connection.close()


@app.route("/health")
def health():
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT 1")
        cursor.fetchone()

        return {
            "application": "healthy",
            "database": "connected",
            "service": "employee-feedback",
        }, 200

    except Error as error:
        app.logger.error("Health check failed: %s", error)

        return {
            "application": "healthy",
            "database": "unavailable",
            "service": "employee-feedback",
        }, 503

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
