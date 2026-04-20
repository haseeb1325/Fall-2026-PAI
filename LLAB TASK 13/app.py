from flask import Flask, render_template, request, jsonify, send_file
from question_generator import generate_question_paper
from tutor import get_tutor_response
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create folders if not exist
os.makedirs("data", exist_ok=True)
os.makedirs("uploads", exist_ok=True)
os.makedirs("vector_db", exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_paper', methods=['GET', 'POST'])
def generate_paper():
    if request.method == 'POST':
        topic = request.form.get('topic')
        mcqs = int(request.form.get('mcqs', 10))
        short = int(request.form.get('short', 5))
        long = int(request.form.get('long', 3))
        difficulty = request.form.get('difficulty', 'Medium')
        
        filename, paper_text = generate_question_paper(topic, mcqs, short, long, difficulty)
        
        return render_template('generate_paper.html', 
                             paper_text=paper_text, 
                             filename=filename)
    
    return render_template('generate_paper.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)

@app.route('/tutor', methods=['GET', 'POST'])
def tutor():
    if request.method == 'POST':
        question = request.form.get('question')
        if question:
            answer = get_tutor_response(question)
            return jsonify({"answer": answer})
    return render_template('tutor.html')

if __name__ == '__main__':
    print(" EduTech RAG App running...")
    app.run(debug=True)