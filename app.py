from flask import Flask, render_template, request
import os
from logic import analyze_resume, rag_query

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

current_result = None

@app.route("/", methods=["GET", "POST"])
def index():
    global current_result
    answer = None
    if request.method == "POST":
        file = request.files.get("resume")
        if file:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)
            current_result = analyze_resume(filepath)
    return render_template("index.html", result=current_result, answer=answer)

@app.route("/ask", methods=["POST"])
def ask():
    global current_result
    question = request.form.get("question")
    answer = rag_query(question)
    return render_template("index.html", result=current_result, answer=answer)

if __name__ == "__main__":
    app.run(debug=True)
