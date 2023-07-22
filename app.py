from flask import Flask, render_template, request, jsonify
from flask_cors import CORS   # Import the CORS module
import PyPDF2

app = Flask(__name__)
CORS(app)   # Enable CORS for the entire app

def extract_text_from_pdf(file):
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception:
        return None

def preprocess_text(text):
    tokens = text.lower().split()
    return tokens

def calculate_similarity(job_requirements, candidate_qualifications):
    job_requirements = preprocess_text(job_requirements)
    candidate_qualifications = preprocess_text(candidate_qualifications)

    common_tokens = set(job_requirements) & set(candidate_qualifications)
    similarity = len(common_tokens) / len(job_requirements)

    return similarity

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/upload-resume', methods=['POST'])

def upload_resume():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    job_requirements = request.form.get('job_requirements')

    candidate_resume_text = extract_text_from_pdf(file)
    if candidate_resume_text:
        similarity = calculate_similarity(job_requirements, candidate_resume_text)
        return jsonify({"similarity": similarity})
    else:
        return jsonify({"error": "Failed to extract text from the candidate's resume"}), 400

if __name__ == '__main__':
    app.run(debug=True)
