from rag_pipeline import get_rag_chain

def get_tutor_response(question):
    try:
        chain = get_rag_chain()
        
        full_question = f"Explain like a friendly tutor. Student asked: {question}. Give step-by-step explanation with examples."
        
        print(f"[Tutor] User asked: {question}")   # Debug ke liye
        
        answer = chain.invoke(full_question)
        
        # Agar RAG mein koi content nahi mila
        if not answer or len(answer.strip()) < 20 or "don't have enough" in answer.lower():
            answer = "Sorry, I don't have enough study material about this topic in my knowledge base right now. Please upload related PDF notes in the 'data' folder and try again."
        
        return answer
        
    except Exception as e:
        print(f"[Tutor Error]: {e}")
        return f"Sorry, something went wrong while processing your question. Error: {str(e)}"