from flask import Flask, render_template, request, redirect, session
import sqlite3
import requests
import os

app = Flask(__name__)
app.secret_key = "smartfarming123"

# ---------------- LOGIN ----------------
@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/do_login", methods=["POST"])
def do_login():
    username = request.form["username"]
    password = request.form["password"]

    if username == "admin" and password == "admin":
        session["user"] = username
        return redirect("/")
    else:
        return "Invalid Login ❌"


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


# ---------------- HOME ----------------
@app.route("/")
def home():
    if "user" in session:
        return render_template("index.html")
    else:
        return redirect("/login")


# ---------------- WEATHER ----------------
@app.route("/weather")
def weather():
    city = "Mumbai"
    api_key = cac8919b3bd2b0700e90c931c397d728

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        weather_data = {
            "city": city,
            "temp": data["main"]["temp"],
            "desc": data["weather"][0]["description"]
        }

    except:
        weather_data = {
            "city": city,
            "temp": "N/A",
            "desc": "API Error"
        }

    return render_template("weather.html", weather=weather_data)


# ---------------- FARMER FORM ----------------
@app.route("/farmer")
def farmer():
    return render_template("farmer.html")


# ---------------- ADD FARMER ----------------
@app.route("/add_farmer", methods=["POST"])
def add_farmer():
    name = request.form["name"]
    village = request.form["village"]
    crop = request.form["crop"]

    conn = sqlite3.connect("farmers.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO farmers (name, village, crop) VALUES (?, ?, ?)",
        (name, village, crop)
    )

    conn.commit()
    conn.close()

    return "Farmer Added Successfully <br><a href='/farmers'>Go Back</a>"


# ---------------- FARMERS LIST ----------------
@app.route("/farmers")
def farmers():
    conn = sqlite3.connect("farmers.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM farmers")
    data = cursor.fetchall()

    conn.close()

    return render_template("farmers_list.html", farmers=data)


# ---------------- STATISTICS ----------------
@app.route("/stats")
def stats():
    conn = sqlite3.connect("farmers.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM farmers")
    total_farmers = cursor.fetchone()[0]

    cursor.execute("SELECT crop, COUNT(*) FROM farmers GROUP BY crop")
    crop_data = cursor.fetchall()

    conn.close()

    return render_template("stats.html",
                           total=total_farmers,
                           crops=crop_data)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)