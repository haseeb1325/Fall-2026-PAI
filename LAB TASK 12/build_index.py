import pandas as pd
import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# ---------------------------
# STEP 1: LOAD DATA
# ---------------------------
df = pd.read_csv("../data/travels_qna.csv")
questions = df["question"].tolist()
answers = df["answer"].tolist()

# ---------------------------
# STEP 2: PREPROCESS
# ---------------------------
def preprocess(text):
    return text.lower().strip()

processed_questions = [preprocess(q) for q in questions]

# ---------------------------
# STEP 3: EMBEDDINGS (MiniLM)
# ---------------------------
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
embeddings = model.encode(processed_questions)

np.save("embeddings.npy", embeddings)

# ---------------------------
# STEP 4: FAISS INDEX
# ---------------------------
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings.astype("float32"))

faiss.write_index(index, "faiss_index.bin")

# ---------------------------
# STEP 5: SAVE Q/A DATA
# ---------------------------
with open("qna_data.pkl", "wb") as f:
    pickle.dump({"questions": questions, "answers": answers}, f)

print("Index built successfully!")
