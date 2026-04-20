from langchain_groq import ChatGroq
from fpdf import FPDF
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Updated model - old one is decommissioned
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)

def generate_question_paper(topic, num_mcqs=10, num_short=5, num_long=3, difficulty="Medium"):
    prompt = f"""
    Create a professional question paper for class 9-12 on the topic: {topic}
    Difficulty: {difficulty}
    
    Include:
    - {num_mcqs} MCQs with 4 options each and correct answer marked
    - {num_short} Short questions (3-5 marks each)
    - {num_long} Long/Descriptive questions (8-10 marks each)
    
    Format it properly with clear numbering.
    Also provide Answer Key at the end.
    """

    response = llm.invoke(prompt)
    paper_text = response.content

    # PDF Generation
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 16)
            self.cell(0, 10, f'Question Paper: {topic}', ln=1, align='C')
            self.ln(10)

    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, paper_text.encode('latin-1', 'replace').decode('latin-1'))

    filename = f"Question_Paper_{topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    pdf.output(filename)
    
    return filename, paper_text