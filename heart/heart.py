import os
import turtle
from flask import Flask, send_file, render_template_string
from PIL import Image

app = Flask(__name__)

# Dossier où l'image sera enregistrée
OUTPUT_PATH = "heart.png"


def draw_heart_to_image(path=OUTPUT_PATH):
    # On utilise un écran hors‑écran (tkinter) classique
    screen = turtle.Screen()
    screen.bgcolor("black")
    turtle.title("for bestie")

    t = turtle.Turtle()
    t.hideturtle()
    t.color("red")
    t.fillcolor("red")
    t.begin_fill()

    t.left(140)
    t.forward(180)
    t.circle(-90, 200)
    t.setheading(60)
    t.circle(-90, 200)
    t.forward(100)

    t.end_fill()

    t.up()
    t.setpos(-80, 150)
    t.down()
    t.color("white")
    t.write("I LOVE YOU", font=("Rockwell Nova", 20, "bold"))

    # Récupération du canvas tkinter
    cv = screen.getcanvas()
    ps_path = "heart.ps"
    cv.postscript(file=ps_path)  # export PostScript [web:11]

    # Conversion PS -> PNG avec Pillow [web:11]
    img = Image.open(ps_path)
    img.save(path, "PNG")

    # Nettoyage
    turtle.bye()
    os.remove(ps_path)


@app.route("/")
def index():
    # Page HTML qui affiche l'image
    html = """
    <!doctype html>
    <html lang="fr">
      <head>
        <meta charset="utf-8">
        <title>Pour bestie</title>
      </head>
      <body style="background-color:black; display:flex; justify-content:center; align-items:center; height:100vh;">
        <img src="/heart" alt="heart">
      </body>
    </html>
    """
    return render_template_string(html)


@app.route("/heart")
def heart():
    # Redessine à chaque requête pour regénérer l'image si besoin
    if os.path.exists(OUTPUT_PATH):
        os.remove(OUTPUT_PATH)
    draw_heart_to_image(OUTPUT_PATH)
    return send_file(OUTPUT_PATH, mimetype="image/png")


if __name__ == "__main__":
    # Important : désactiver le reloader sinon turtle va être lancé deux fois
    app.run(host="0.0.0.0", port=5000, debug=False)
