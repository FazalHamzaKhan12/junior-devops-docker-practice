import os

import mysql.connector
from flask import Flask, flash, redirect, render_template, request, url_for
from mysql.connector import Error


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "devops-105-practice-key")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024


def get_database_connection():
    """Connect using the Compose service name supplied through MYSQL_HOST."""
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "mysql"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "root"),
        database=os.getenv("MYSQL_DB", "devops"),
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


def load_recent_feedback(connection):
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
        connection = get_database_connection()
        initialize_table(connection)

        if request.method == "POST":
            employee_name = request.form.get("name", "").strip()
            message = request.form.get("feedback", "").strip()

            if not employee_name or not message:
                flash("Please enter your name and feedback.", "error")
            elif len(employee_name) > 100 or len(message) > 1000:
                flash("Your name or feedback is too long.", "error")
            else:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO feedback (employee_name, message) VALUES (%s, %s)",
                    (employee_name, message),
                )
                connection.commit()
                cursor.close()
                flash("Feedback saved. Thank you for helping us improve.", "success")
                return redirect(url_for("index"))

        return render_template(
            "index.html",
            database_connected=True,
            recent_feedback=load_recent_feedback(connection),
        )
    except Error as error:
        app.logger.error("MySQL connection failed: %s", error)
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

    try:
        connection = get_database_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        return {
            "application": "healthy",
            "database": "connected",
            "project": "DEVOPS-105",
        }, 200
    except Error:
        return {
            "application": "healthy",
            "database": "unavailable",
            "project": "DEVOPS-105",
        }, 503
    finally:
        if connection and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
