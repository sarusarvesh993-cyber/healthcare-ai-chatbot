python -c "
c = '''# MediCare AI - Healthcare AI Chatbot

An AI-powered healthcare chatbot built with OpenRouter LLM, LangChain, FAISS, and Streamlit that provides general health information, symptom guidance, nutrition advice, first-aid tips, and preventive healthcare information.

---

## Table of Contents
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [API Endpoints](#api-endpoints-fastapi-backend)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Prompt Engineering](#prompt-engineering)
- [Safety Measures](#safety-measures)
- [Evaluation Criteria](#evaluation-criteria)
- [Disclaimer](#disclaimer)

---

## Features

### Core Features
- **LLM-Powered Responses** - Uses OpenRouter (GPT-OSS-20B) for intelligent health conversations
- **RAG (Retrieval-Augmented Generation)** - Answers grounded in a curated medical knowledge base of 20 documents
- **Conversation Memory** - Context-aware conversations with sliding window memory (10 exchanges)
- **FAISS Vector Store** - Efficient CPU-based similarity search over medical documents
- **Source Citations** - Transparent sourcing from reputable health organizations

### Safety Features
- **Medical Disclaimers** - Displayed with every health-related response
- **Emergency Detection** - Detects emergency keywords and provides immediate guidance
- **Response Guardrails** - Prevents the bot from providing diagnoses or prescriptions
- **Scope Enforcement** - Keeps conversations focused on healthcare topics only

### UI/UX Features
- **Professional Medical Interface** - Clean, responsive Streamlit UI with custom CSS
- **Quick Questions** - Sidebar buttons for common health queries
- **Conversation Stats** - Track message count and conversation history
- **History Management** - Clear conversation and start fresh

---

## Architecture

User Query -> Query Classification -> RAG Retrieval + LLM Generation -> Safety Checks -> Response

### Query Classification
- Emergency: Keywords like chest pain, can't breathe -> Immediate emergency response
- Greeting: Short greeting messages -> Welcome message
- Out of Scope: Non-health topics -> Redirect to health topics
- Health Query: All health questions -> Full RAG + LLM pipeline

### RAG Pipeline
1. User query is embedded using all-MiniLM-L6-v2
2. FAISS performs similarity search against medical knowledge base
3. Top 3 relevant documents are retrieved
4. Context is injected into the LLM system prompt
5. LLM generates response grounded in retrieved context

---

## Tech Stack

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Frontend | Streamlit | Rapid prototyping, built-in chat, Python-native |
| Backend | FastAPI | RESTful API design, automatic documentation |
| LLM | OpenRouter (GPT-OSS-20B) | Free tier, fast, OpenAI-compatible API |
| Orchestration | LangChain | Mature framework for chains and RAG |
| Vector Store | FAISS | Efficient CPU-based similarity search |
| Embeddings | all-MiniLM-L6-v2 | Lightweight, fast, good semantics |
| Language | Python 3.9+ | Best AI/ML ecosystem |

---

## API Endpoints (FastAPI Backend)

The project includes a REST API backend built with FastAPI.

### Start the API Server
python api.py

### Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | API info and available endpoints |
| GET | /health | Health check and system status |
| POST | /chat | Send a health question and get AI response |
| GET | /summary | Get conversation summary |
| POST | /clear | Clear conversation history |

### API Documentation
- Swagger UI: http://localhost:8000/docs
- OpenAPI JSON: http://localhost:8000/openapi.json

### Example Request
curl -X POST http://localhost:8000/chat -H Content-Type: application/json -d {\"message\": \"What are the symptoms of the flu?\"}

### Example Response
{
  \"response\": \"Common symptoms include fever, body aches...\",
  \"sources\": [],
  \"query_type\": \"health_query\",
  \"has_disclaimer\": true
}

### Running Both Services

Terminal 1 (Streamlit Frontend):
streamlit run app.py

Terminal 2 (FastAPI Backend):
python api.py

- Streamlit UI: http://localhost:8501
- FastAPI Docs: http://localhost:8000/docs

---

## Project Structure

healthcare-chatbot/
+-- app.py                          # Streamlit UI (Frontend)
+-- api.py                          # FastAPI Backend (REST API)
+-- healthcare_chatbot.py           # Core chatbot logic
+-- prompt_engineering.py           # System prompts and templates
+-- conversation_memory.py          # Chat history management
+-- requirements.txt                # Python dependencies
+-- .env                            # API key (not shared)
+-- .env.example                    # Environment variable template
+-- .gitignore                      # Git ignore rules
+-- README.md                       # This file
+-- create_presentation.py          # PPTX generator
+-- create_pdf.py                   # PDF generator
+-- data/
|   +-- medical_knowledge_base.json # 20 curated medical documents
|   +-- create_vector_store.py      # Vector store creation script
|   +-- faiss_medical_store/        # Generated FAISS index
+-- docs/
    +-- architecture_presentation.pptx
    +-- logic_documentation.pdf

---

## Setup Instructions

### Prerequisites
- Python 3.9 or higher
- OpenRouter API key (free)

### Step 1: Clone
git clone https://github.com/sarusarvesh993-cyber/healthcare-ai-chatbot.git
cd healthcare-ai-chatbot

### Step 2: Create Virtual Environment
python -m venv venv
venv\\Scripts\\activate (Windows) or source venv/bin/activate (Mac/Linux)

### Step 3: Install Dependencies
pip install -r requirements.txt

### Step 4: Set Up API Key
1. Get a free key at: https://openrouter.ai/keys
2. Create a .env file with:
OPENROUTER_API_KEY=your_key_here
LLM_MODEL=openai/gpt-oss-20b:free

### Step 5: Create Vector Store
python data/create_vector_store.py

### Step 6: Run
streamlit run app.py (Frontend on port 8501)
python api.py (Backend on port 8000)

---

## Usage

| Category | Example |
|----------|---------|
| Symptoms | What are the symptoms of the flu? |
| Diseases | What is Type 2 Diabetes? |
| Nutrition | What should I eat for a healthy heart? |
| First Aid | How do I treat a minor burn? |
| Lifestyle | How much exercise do I need per week? |
| Prevention | What vaccines do adults need? |
| Mental Health | How can I manage stress effectively? |

---

## How It Works

### Query Processing
1. Classification: emergency, greeting, out-of-scope, or health query
2. Retrieval: FAISS retrieves top 3 relevant documents from knowledge base
3. Generation: System prompt + context + history sent to LLM
4. Post-Processing: Disclaimer added, sources appended, stored in memory

### Conversation Memory
- Sliding window of last 10 exchanges for LLM context
- 20 message history for UI display
- Context-aware follow-up question handling

### Knowledge Base
20 curated medical documents from: Mayo Clinic, CDC, American Heart Association, American Diabetes Association, National Sleep Foundation, American Red Cross, Harvard Health, National Institute of Mental Health, USDA, American Academy of Dermatology

---

## Prompt Engineering

### System Prompt (5 Layers)
1. Role Definition: Empathetic Healthcare AI Assistant
2. Scope Boundaries: CAN do vs MUST NOT do lists
3. Response Style: Empathetic tone, clear language
4. Safety Protocol: Emergency handling, disclaimers
5. RAG Integration: How to use context, cite sources

### Key Techniques
- Role Prompting: Healthcare AI persona
- Constraint Setting: No diagnoses or prescriptions
- Context Injection: RAG documents in system prompt
- Guardrail Prompting: Safety rules in every prompt
- Response Templates: Emergency, greeting, out-of-scope
- Chain-of-Thought: Classification before response
- Medical Disclaimers: Auto-appended to responses

---

## Safety Measures

- Emergency keyword detection with immediate safety response
- Medical disclaimer on every health response
- Diagnosis prevention through system prompt constraints
- Scope enforcement for non-health queries
- Source attribution for transparency
- Error handling with safe fallback responses

---

## Evaluation Criteria

| Criteria | Weight | Implementation |
|----------|--------|---------------|
| Code Quality | 25% | Modular design, clean Python, docstrings |
| Functionality | 25% | Full RAG, memory, classification, guardrails |
| Prompt Engineering | 20% | Multi-layered prompts, RAG context, templates |
| UI/UX | 10% | Professional medical UI, quick questions |
| Documentation | 10% | README, architecture slides, logic doc |
| Innovation | 10% | Emergency detection, FastAPI, source citations |

---

## Disclaimer

This chatbot provides general health information for educational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider. If you think you may have a medical emergency, call your doctor or emergency services immediately.
'''
open('README.md', 'w', encoding='utf-8').write(c)
print('README.md updated!')
"