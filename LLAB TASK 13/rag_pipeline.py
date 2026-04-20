from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Updated Groq Model (old model was decommissioned)
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.2)

def load_documents():
    documents = []
    if not os.path.exists("data"):
        print("Warning: 'data' folder does not exist!")
        return documents
    
    for filename in os.listdir("data"):
        if filename.endswith(".pdf"):
            loader = PyMuPDFLoader(os.path.join("data", filename))
            documents.extend(loader.load())
    
    print(f"Loaded {len(documents)} PDF documents from data folder.")
    return documents

def get_vectorstore():
    persist_dir = "vector_db"
    
    # Agar pehle se vector database hai to use karo
    if os.path.exists(persist_dir) and len(os.listdir(persist_dir)) > 0:
        print("Using existing vector database...")
        return Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    
    # Naya vectorstore banao
    docs = load_documents()
    if not docs:
        print("No documents found in 'data' folder! RAG will give limited answers.")
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    splits = text_splitter.split_documents(docs)
    
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=persist_dir
    )
    print(f"Created new vectorstore with {len(splits)} text chunks.")
    return vectorstore

def get_rag_chain():
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 6})
    
    # Strong English-only prompt
    template = """You are an expert friendly teacher for Class 9-12 students in Pakistan.
    Answer the question using ONLY the following context.

    Important Rules:
    - Always answer in **clear and simple English** only.
    - Do NOT use Urdu script or full Urdu sentences.
    - Use very easy English words so students can understand easily.
    - Explain step-by-step with real-life examples.
    - If you don't have enough information, say: "Sorry, I don't have enough study material about this topic right now."

    Context: {context}
    Question: {question}

    Answer in simple English:"""

    prompt = PromptTemplate.from_template(template)
    
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain