from flask import Flask, render_template, request, redirect, url_for
import os
import json
from datetime import datetime

app = Flask(__name__)

# Define the data directory
DATA_DIR = os.environ.get("DATA_DIR", "./data")

# Define the JSON files within the data directory
DATA_FILE = os.path.join(DATA_DIR, "todos.json")
COMPLETED_FILE = os.path.join(DATA_DIR, "completed.json")
NOTES_FILE = os.path.join(DATA_DIR, "notes.json")

@app.template_filter("datetimeformat")
def datetimeformat(value, format="%b %d, %Y %I:%M %p"):
    try:
        return datetime.fromisoformat(value).strftime(format)
    except ValueError:
        return value

def load_todos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_todos(todos):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(todos, f, indent=2, sort_keys=True)

def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r") as f:
            return json.load(f)
    return []

def save_notes(notes):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=2, sort_keys=True)

def save_completed(task):
    os.makedirs(DATA_DIR, exist_ok=True)
    if os.path.exists(COMPLETED_FILE):
        with open(COMPLETED_FILE, "r") as f:
            completed_tasks = json.load(f)
    else:
        completed_tasks = []

    task["completed"] = datetime.now().isoformat()
    completed_tasks.append(task)

    with open(COMPLETED_FILE, "w") as f:
        json.dump(completed_tasks, f, indent=2, sort_keys=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        task = request.form.get("task")
        if task:
            todos.append({
                "text": task,
                "created": datetime.now().isoformat()
            })
            save_todos(todos)
        return redirect(url_for("index"))
    return render_template("index.html", todos=todos)

@app.route("/delete/<int:task_id>", methods=["POST"])
def delete(task_id):
    global todos
    if 0 <= task_id < len(todos):
        todos.pop(task_id)
        save_todos(todos)
    return redirect(url_for("index"))

@app.route("/completed")
def completed():
    if os.path.exists(COMPLETED_FILE):
        with open(COMPLETED_FILE, "r") as f:
            completed_tasks = json.load(f)
    else:
        completed_tasks = []
    return render_template("completed.html", completed=completed_tasks)

@app.route("/complete/<int:task_id>", methods=["POST"])
def complete(task_id):
    if 0 <= task_id < len(todos):
        task = todos.pop(task_id)
        save_completed(task)
        save_todos(todos)
    return redirect(url_for("index"))

@app.route("/revert/<int:task_id>", methods=["POST"])
def revert(task_id):
    if os.path.exists(COMPLETED_FILE):
        with open(COMPLETED_FILE, "r") as f:
            completed_tasks = json.load(f)
    else:
        completed_tasks = []

    if 0 <= task_id < len(completed_tasks):
        task = completed_tasks.pop(task_id)
        task.pop("completed", None)

        todos.append(task)
        save_todos(todos)

        with open(COMPLETED_FILE, "w") as f:
            json.dump(completed_tasks, f, indent=2, sort_keys=True)

    return redirect(url_for("completed"))

@app.route("/notes", methods=["GET", "POST"])
def notes():
    notes = load_notes()
    if request.method == "POST":
        note_title = request.form.get("note_title")
        note_content = request.form.get("note_content")
        if note_title and note_content:
            notes.append({
                "title": note_title,
                "content": note_content,
                "created": datetime.now().isoformat()
            })
            save_notes(notes)
        return redirect(url_for("notes"))
    return render_template("notes.html", notes=notes)

@app.route("/add_note", methods=["POST"])
def add_note():
    note_title = request.form.get("title")
    note_content = request.form.get("content")
    if note_title and note_content:
        notes = load_notes()
        notes.append({
            "title": note_title,
            "content": note_content,
            "created": datetime.now().isoformat()
        })
        save_notes(notes)
    return redirect(url_for("notes"))

@app.route("/update_note/<int:note_id>", methods=["POST"])
def update_note(note_id):
    notes = load_notes()
    if 0 <= note_id < len(notes):
        notes[note_id]["title"] = request.form.get("title", notes[note_id]["title"])
        notes[note_id]["content"] = request.form.get("content", notes[note_id]["content"])
        notes[note_id]["created"] = notes[note_id].get("created", datetime.now().isoformat())
        save_notes(notes)
    return redirect(url_for("notes"))

@app.route("/delete_note/<int:note_id>", methods=["POST"])
def delete_note(note_id):
    notes = load_notes()
    if 0 <= note_id < len(notes):
        notes.pop(note_id)
        save_notes(notes)
    return redirect(url_for("notes"))

# Ensure data directory and files exist
os.makedirs(DATA_DIR, exist_ok=True)
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)
if not os.path.exists(COMPLETED_FILE):
    with open(COMPLETED_FILE, "w") as f:
        json.dump([], f)
if not os.path.exists(NOTES_FILE):
    with open(NOTES_FILE, "w") as f:
        json.dump([], f)

todos = load_todos()

if __name__ == "__main__":
    app.run(debug=True, port=5001)
