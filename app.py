import os
from datetime import datetime

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

# Directories for notes
NOTES_DIR = "./notes/named"
DAILY_NOTES_DIR = "./notes/daily"

# Ensure the directories exist
os.makedirs(NOTES_DIR, exist_ok=True)
os.makedirs(DAILY_NOTES_DIR, exist_ok=True)


@app.route("/")
def write_note():
    return render_template("index.html")  # Render the writing page


@app.route("/save", methods=["POST"])
def save_note():
    note_type = request.form["note_type"]
    filename = request.form["filename"]
    content = request.form["content"]

    # Determine the file path based on note type
    if note_type == "named":
        filepath = os.path.join(NOTES_DIR, f"{filename}.md")
    elif note_type == "daily":
        # Use current date for daily notes
        current_date = datetime.now().strftime("%Y-%m-%d")
        filepath = os.path.join(DAILY_NOTES_DIR, f"{current_date}.md")
    else:
        return "Invalid note type", 400

    # Save the note to a file
    with open(filepath, "w") as f:
        f.write(content)

    return redirect(url_for("view_notes"))


@app.route("/view")
def view_notes():
    # List all named and daily notes
    named_notes = os.listdir(NOTES_DIR)
    daily_notes = os.listdir(DAILY_NOTES_DIR)
    return render_template(
        "view_note.html", named_notes=named_notes, daily_notes=daily_notes
    )


@app.route("/view_note/<note_type>/<note_name>")
def view_single_note(note_type, note_name):
    # Read the content of a specific note
    if note_type == "named":
        filepath = os.path.join(NOTES_DIR, f"{note_name}")
    elif note_type == "daily":
        filepath = os.path.join(DAILY_NOTES_DIR, f"{note_name}")
    else:
        return "Invalid note type", 400

    print(filepath)
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            content = f.read()
        return render_template("view_note.html", content=content)
    else:
        return "Note not found", 404


if __name__ == "__main__":
    app.run(debug=True)
