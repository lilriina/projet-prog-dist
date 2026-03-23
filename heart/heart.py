from flask import Flask, request, send_file, render_template_string
from heart_utils import generate_heart_image, OUTPUT_PATH
import random
import os
import requests
from mysql import MysqlClient

app = Flask(__name__)

def mysql_client_from_env():
    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_USERNAME = os.getenv("MYSQL_USERNAME")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_DB = os.getenv("MYSQL_DB")
    MYSQL_TABLE = os.getenv("MYSQL_TABLE")

    client = MysqlClient(
        db=MYSQL_DB, username=MYSQL_USERNAME, password=MYSQL_PASSWORD, host=MYSQL_HOST, table=MYSQL_TABLE
    )
    client.connect_if_not_connected()
    return client

@app.route("/", methods=["GET"])
def index():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Great+Vibes&family=Playfair+Display&display=swap" rel="stylesheet">
    <style>
        body {
            background:#F6E6E8;
            font-family:'Playfair Display',serif;
            display:flex;
            justify-content:center;
            align-items:center;
            height:100vh;
            margin:0;
        }
        .card {
            background:white;
            padding:40px;
            border-radius:20px;
            box-shadow:0 10px 30px rgba(0,0,0,0.1);
            text-align:center;
            width:320px;
        }
        h1 {
            font-family:'Great Vibes',cursive;
            color:#5A3E46;
            font-size:40px;
            margin-bottom:25px;
        }
        label {
            display:block;
            margin-top:15px;
            margin-bottom:5px;
            color:#5A3E46;
            font-size:14px;
        }
        input,button {
            width:100%;
            padding:10px;
            border-radius:10px;
            border:1px solid #ddd;
        }
        input[type="color"]{
            padding:0;
            height:40px;
        }
        button {
            background:#F497B6;
            color:white;
            border:none;
            margin-top:20px;
            cursor:pointer;
        }
        button:hover {
            background:#ec7ea7;
        }
    </style>
    </head>
    <body>
        <div class="card">
            <h1>Create a heart</h1>
            <form action="/generate" method="post">
                <label>Name</label>
                <input type="text" name="name" placeholder="Enter a name" required>

                <label>Message</label>
                <input type="text" name="message" placeholder="Write a message" required>

                <label>Choose the heart color</label>
                <input type="color" name="color" value="#F497B6">

                <button type="submit">Generate</button>
            </form>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route("/generate", methods=["POST"])
def generate():
    name = request.form["name"]
    message = request.form["message"]
    color = request.form["color"]

    try:
        response = requests.get("http://titre:5001/titre")  # service name
        phrase = response.json().get("titre", "Have a good day!")
    except requests.exceptions.RequestException:
        phrase = "Have a good day!" 

    # Générer la nouvelle image de coeur
    generate_heart_image(name, message, color)

    # Sauvegarder dans la base de données
    client = mysql_client_from_env()
    # Récupérer le prochain id (max(id) + 1)
    db_connection = client.get_connection()
    try:
        with db_connection.cursor() as cursor:
            cursor.execute(f"SELECT MAX(id) FROM {client.db}.{client.table}")
            result = cursor.fetchone()
            next_id = (result[0] or 0) + 1
    except Exception as e:
        next_id = 1
    finally:
        if db_connection.is_connected():
            db_connection.close()

    # Réinsérer la connexion pour l'insertion (car close plus haut)
    client.connect_if_not_connected()
    client.insert_row(client.db, client.table, next_id, name, message)
    
    # HTML page with cache-busting query string for the image
    html = f"""
    <!DOCTYPE html>
    <html>
    <body style="background:#F6E6E8;text-align:center;padding-top:40px">
        <img src="/heart.png?{random.randint(1, 1_000_000)}" style="width:600px">
        <br><br>
        <p style="font-size:20px;color:#5A3E46;margin-top:20px">{phrase}</p>
        <br><br>
        <a href="/">Create another</a>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route("/heart.png")
def heart():
    return send_file(OUTPUT_PATH, mimetype="image/png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)