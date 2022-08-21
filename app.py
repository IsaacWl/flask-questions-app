from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def connect():
    conn = sqlite3.connect("questions.db")
    return conn

@app.route("/")
def home():
   conn = connect()
   cursor = conn.cursor()
   cursor.execute("""
   CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL
   )
   """)
   conn.close()
   return render_template("home.html")

@app.route("/questions", methods=["POST", "GET"])
def questions():
    conn = connect()
    cursor = conn.cursor()
    try:
        questions = cursor.execute("SELECT * FROM questions").fetchall()
    except:
        return redirect("/")    
    results = []
    cols = [col[0] for col in cursor.description]

    results = [dict(zip( cols, value )) for value in questions]
    if request.method == "GET":
        return render_template("questions.html", questions=results)
    
    question = request.form.get("question").strip()
    answer = request.form.get("answer").strip()

    if not question or not answer:
        return redirect("/")

    cursor.execute("INSERT INTO questions (question, answer) VALUES (?, ?)", (question, answer))
    conn.commit()
    conn.close()
    return redirect("/questions")


@app.route("/question/<string:id>")
def question(id):
    conn = connect()
    cursor = conn.cursor()
    question = cursor.execute("SELECT * FROM questions WHERE id=?", [int(id)]).fetchone()
    cols = [col[0] for col in cursor.description]
    question_dict = dict(zip(cols, question))
    conn.close()
    return render_template("question.html", question=question_dict)