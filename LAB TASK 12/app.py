from flask import Flask, render_template, request
import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

# -----------------------
# Load model + vectors
# -----------------------
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

index = faiss.read_index("../model/faiss_index.bin")
embeddings = np.load("../model/embeddings.npy")

with open("../model/qna_data.pkl", "rb") as f:
    data = pickle.load(f)

questions = data["questions"]
answers = data["answers"]

# -----------------------
# Flask App
# -----------------------
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    response = ""
    if request.method == "POST":
        query = request.form["query"]

        # Embedding of the input
        user_emb = model.encode([query])

        # Search
        D, I = index.search(user_emb.astype("float32"), 1)
        idx = I[0][0]

        response = answers[idx]

    return render_template("index.html", response=response)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
