<<<<<<< HEAD
import os
from flask import Flask, render_template, request
from logic import analyze_resume
import os
from logic import analyze_resume, rag_query

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure uploads folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
current_result = None

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        job_desc = request.form.get('job_description', '')
        print("Job Description:", job_desc) 
        file = request.files['resume']
@app.route("/", methods=["GET", "POST"])
def index():
    global current_result
    answer = None
    if request.method == "POST":
        file = request.files.get("resume")
        if file:
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            results = analyze_resume(file_path)
            return render_template('index.html', results=results)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)
            current_result = analyze_resume(filepath)
    return render_template("index.html", result=current_result, answer=answer)

    return render_template('index.html')
@app.route("/ask", methods=["POST"])
def ask():
    global current_result
    question = request.form.get("question")
    answer = rag_query(question)
    return render_template("index.html", result=current_result, answer=answer)

if __name__ == '__main__':
    app.run(debug=True)
if __name__ == "__main__":
    app.run(debug=True)
=======
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
>>>>>>> fa8778c19502a950c2bd04c6a7532e8c9725fb79
