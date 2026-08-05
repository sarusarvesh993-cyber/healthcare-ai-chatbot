from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib import colors
import os

def create_pdf():
    os.makedirs('docs', exist_ok=True)
    doc = SimpleDocTemplate('docs/logic_documentation.pdf', pagesize=A4,
        rightMargin=0.75*inch, leftMargin=0.75*inch, topMargin=0.75*inch, bottomMargin=0.75*inch)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('T', parent=styles['Title'], fontSize=24, textColor=HexColor('#1a1a2e'), spaceAfter=20, alignment=1)
    sub_style = ParagraphStyle('S', parent=styles['Normal'], fontSize=14, textColor=HexColor('#667eea'), spaceAfter=30, alignment=1)
    h1 = ParagraphStyle('H1', parent=styles['Heading1'], fontSize=18, textColor=HexColor('#2d5f8a'), spaceBefore=20, spaceAfter=10)
    h2 = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=14, textColor=HexColor('#1b3a4b'), spaceBefore=15, spaceAfter=8)
    body = ParagraphStyle('B', parent=styles['Normal'], fontSize=10, textColor=HexColor('#333333'), spaceAfter=8, leading=14)
    bullet = ParagraphStyle('BL', parent=body, leftIndent=20, bulletIndent=10, spaceAfter=4)

    story = []

    # TITLE PAGE
    story.append(Spacer(1, 2*inch))
    story.append(Paragraph('MediCare AI - Healthcare Chatbot', title_style))
    story.append(Paragraph('Logic Documentation', sub_style))
    story.append(Spacer(1, 0.5*inch))
    story.append(HRFlowable(width='80%', thickness=2, color=HexColor('#667eea')))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph('AI Engineer Technical Assignment<br/>OpenRouter + LangChain + FAISS + Streamlit', ParagraphStyle('C', parent=body, alignment=1, fontSize=12)))
    story.append(PageBreak())

    # SECTION 1
    story.append(Paragraph('1. Overview', h1))
    story.append(Paragraph('This document explains the internal logic, prompt engineering strategy, safety measures, and design assumptions of the Healthcare AI Chatbot. The chatbot uses Retrieval-Augmented Generation (RAG), conversation memory, and prompt engineering to provide safe, accurate, and empathetic health information.', body))

    # SECTION 2
    story.append(Paragraph('2. Query Processing Pipeline', h1))
    story.append(Paragraph('2.1 Query Classification', h2))
    story.append(Paragraph('When a user sends a message, it first passes through a Query Classifier that categorizes it into one of four types:', body))

    table_data = [
        ['Category', 'Trigger', 'Handler'],
        ['emergency', 'Keywords: chest pain, can\'t breathe, suicide', 'Immediate emergency response'],
        ['greeting', 'Short messages matching greeting patterns', 'Welcome message with features'],
        ['out_of_scope', 'Non-health topics (weather, code, shopping)', 'Redirect to health topics'],
        ['health_query', 'All other health-related questions', 'Full RAG + LLM pipeline'],
    ]
    t = Table(table_data, colWidths=[1.2*inch, 2.5*inch, 2.5*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HexColor('#2d5f8a')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BACKGROUND', (0,1), (-1,-1), HexColor('#f8f9fa')),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor('#dee2e6')),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))

    story.append(Paragraph('Implementation Details:', body))
    story.append(Paragraph('Emergency detection uses a curated keyword list covering cardiac events, breathing emergencies, stroke symptoms, severe bleeding, and mental health crises', bullet))
    story.append(Paragraph('Greeting detection uses regex patterns with a word-count threshold (6 words or less) to avoid false positives', bullet))
    story.append(Paragraph('Out-of-scope detection checks for strong non-health indicators like weather, stock price, programming', bullet))

    story.append(Paragraph('2.2 RAG Retrieval', h2))
    story.append(Paragraph('For health queries, the system retrieves relevant context from the FAISS vector store:', body))
    story.append(Paragraph('1. Query Embedding: The user question is embedded using all-MiniLM-L6-v2 (384-dimensional)', bullet))
    story.append(Paragraph('2. Similarity Search: FAISS performs cosine similarity search against the knowledge base', bullet))
    story.append(Paragraph('3. Top-K Selection: The 3 most relevant documents are retrieved', bullet))
    story.append(Paragraph('4. Context Formatting: Retrieved documents are formatted with source metadata', bullet))

    story.append(Paragraph('2.3 Response Generation', h2))
    story.append(Paragraph('The LLM generates a response using the system prompt with role definition and safety guidelines, retrieved RAG context from the knowledge base, recent conversation history (last 3 exchanges), and the user current question.', body))

    story.append(Paragraph('2.4 Post-Processing', h2))
    story.append(Paragraph('After generation, the medical disclaimer is checked and added if missing, source citations are appended from retrieved documents, and the response is stored in conversation memory.', body))

    # SECTION 3
    story.append(PageBreak())
    story.append(Paragraph('3. Prompt Engineering Strategy', h1))
    story.append(Paragraph('3.1 System Prompt Architecture', h2))
    story.append(Paragraph('The system prompt follows a layered structure:', body))

    layers = [
        ['Layer', 'Content', 'Purpose'],
        ['1: Role Definition', 'Empathetic Healthcare AI Assistant', 'Sets persona and expertise'],
        ['2: Scope Boundaries', 'CAN do vs MUST NOT do lists', 'Prevents harmful outputs'],
        ['3: Response Style', 'Empathetic tone, clear language', 'Guides response quality'],
        ['4: Safety Protocol', 'Emergency handling, disclaimers', 'Ensures user safety'],
        ['5: RAG Integration', 'How to use context, cite sources', 'Grounds in facts'],
    ]
    lt = Table(layers, colWidths=[1.5*inch, 2.5*inch, 2*inch])
    lt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HexColor('#1b3a4b')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BACKGROUND', (0,1), (-1,-1), HexColor('#f0f7ff')),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor('#b8daff')),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(lt)
    story.append(Spacer(1, 10))

    story.append(Paragraph('3.2 Key Techniques', h2))
    techniques = [
        ['Technique', 'Application', 'Purpose'],
        ['Role Prompting', 'Healthcare AI persona', 'Sets expertise level'],
        ['Constraint Setting', 'No diagnoses/prescriptions', 'Prevents harm'],
        ['Context Injection', 'RAG docs in system prompt', 'Grounds in facts'],
        ['Guardrail Prompting', 'Safety rules in every prompt', 'Consistent safety'],
        ['Response Templates', 'Emergency/greeting/OOS', 'Consistent format'],
        ['Chain-of-Thought', 'Classification then Generation', 'Structured reasoning'],
    ]
    tt = Table(techniques, colWidths=[1.5*inch, 2*inch, 2.5*inch])
    tt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HexColor('#5c1f1f')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BACKGROUND', (0,1), (-1,-1), HexColor('#fff5f5')),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor('#f5c6cb')),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(tt)

    # SECTION 4
    story.append(Spacer(1, 10))
    story.append(Paragraph('4. Conversation Memory', h1))
    story.append(Paragraph('4.1 Dual Memory Architecture', h2))
    story.append(Paragraph('LangChain-style buffer memory for LLM context maintains last 10 exchanges formatted as Human/AI message pairs, injected into the LLM prompt.', body))
    story.append(Paragraph('Application-level Chat History for UI display stores up to 20 messages with timestamps and source metadata for rendering the chat interface.', body))
    story.append(Paragraph('4.2 Context-Aware Follow-ups', h2))
    story.append(Paragraph('When a user asks a follow-up question (e.g., What about treatment? after asking about diabetes), the conversation memory provides previous exchanges to the LLM, which understands the context and generates a coherent response.', body))

    # SECTION 5
    story.append(Paragraph('5. Safety Measures', h1))
    story.append(Paragraph('5.1 Emergency Detection', h2))
    story.append(Paragraph('Keyword-based detection covers cardiac events, breathing emergencies, stroke symptoms, severe bleeding, and mental health crises. When detected, the chatbot immediately displays emergency contact numbers and does NOT attempt medical treatment advice.', body))
    story.append(Paragraph('5.2 Diagnosis Prevention', h2))
    story.append(Paragraph('The system prompt explicitly states that the AI MUST NOT provide diagnoses or recommend medications. Responses are always phrased informatively.', body))
    story.append(Paragraph('5.3 Medical Disclaimers', h2))
    story.append(Paragraph('Every health response includes a disclaimer stating this is general health information, not medical advice.', body))
    story.append(Paragraph('5.4 Scope Enforcement', h2))
    story.append(Paragraph('Non-health queries receive a friendly redirect listing available healthcare topics.', body))

    # SECTION 6
    story.append(PageBreak())
    story.append(Paragraph('6. Assumptions Made', h1))
    assumptions = [
        'API Availability: Assumes OpenRouter API is accessible with a valid API key',
        'English Language: Designed for English-language queries',
        'General Health Info: Knowledge base provides general information, not personalized advice',
        'CPU Environment: Embeddings run on CPU (no GPU required)',
        'Single User: Designed for single-user sessions',
        'Internet Required: Requires internet for API calls',
        'Free Tier Usage: Designed to work within OpenRouter free API tier limits',
    ]
    for a in assumptions:
        story.append(Paragraph(f'{a}', bullet))

    # SECTION 7
    story.append(Paragraph('7. Error Handling', h1))
    errors = [
        ['Error Scenario', 'Handling'],
        ['Missing API Key', 'Clear error message with setup instructions'],
        ['API Rate Limit', 'Graceful error with retry suggestion'],
        ['Vector Store Missing', 'Auto-creates from knowledge base JSON'],
        ['LLM Generation Error', 'Safe fallback recommending professional consultation'],
        ['Empty/Invalid Input', 'Handled by Streamlit chat input validation'],
        ['Network Errors', 'Caught and displayed as user-friendly messages'],
    ]
    et = Table(errors, colWidths=[2.5*inch, 3.5*inch])
    et.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HexColor('#1f5c1f')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BACKGROUND', (0,1), (-1,-1), HexColor('#f5fff5')),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor('#c3e6cb')),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(et)

    # SECTION 8
    story.append(Spacer(1, 10))
    story.append(Paragraph('8. Performance Considerations', h1))
    perf = [
        'Embedding Cache: FAISS index loaded once at startup and reused',
        'Memory Window: Limited to 10 exchanges to control token usage',
        'Response Streaming: Simulated typing effect for better UX',
        'Lazy Initialization: Components initialized only when needed',
        'Chunk Size: 500 chars balances context quality with retrieval accuracy',
    ]
    for p in perf:
        story.append(Paragraph(p, bullet))

    doc.build(story)
    print('PDF saved: docs/logic_documentation.pdf')

if __name__ == '__main__':
    create_pdf()
