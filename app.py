import streamlit as st
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from healthcare_chatbot import HealthcareChatbot

st.set_page_config(
    page_title="MediCare AI - Healthcare Assistant",
    page_icon="hospital",
    layout="centered",
    initial_sidebar_state="expanded")

def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
    .main .block-container { max-width: 880px; padding-top: 1.5rem; padding-bottom: 2rem; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .pro-header {
        background: linear-gradient(135deg, #0077B6 0%, #00B4D8 50%, #48CAE4 100%);
        padding: 1.8rem 2rem 1.5rem;
        border-radius: 20px;
        margin-bottom: 1rem;
        color: white;
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0, 119, 182, 0.25);
    }
    .pro-header h1 { color: white; font-size: 1.7rem; font-weight: 700; margin: 0; }
    .pro-header .tagline { color: rgba(255,255,255,0.9); font-size: 0.92rem; margin: 4px 0 0 64px; }
    .pro-header .badges { display: flex; gap: 8px; margin-top: 12px; padding-left: 64px; }
    .pro-header .badge {
        background: rgba(255,255,255,0.2);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 500;
        color: white;
        border: 1px solid rgba(255,255,255,0.15);
    }

    .pro-disclaimer {
        background: #FFF8E1;
        border: 1px solid #FFE082;
        border-left: 5px solid #FFA000;
        border-radius: 12px;
        padding: 0.9rem 1.2rem;
        margin-bottom: 1.2rem;
        font-size: 0.85rem;
        color: #5D4037;
    }
    .pro-disclaimer strong { color: #4E342E; }

    .features-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
        margin-bottom: 1.5rem;
    }
    .feature-card {
        background: white;
        border: 1px solid #E3F2FD;
        border-radius: 16px;
        padding: 1.2rem 1rem;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 2px 12px rgba(0, 119, 182, 0.06);
    }
    .feature-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 119, 182, 0.12);
        border-color: #90CAF9;
    }
    .feature-card .card-icon { font-size: 2rem; margin-bottom: 8px; display: block; }
    .feature-card h3 { margin: 0 0 4px; font-size: 0.88rem; color: #1565C0; font-weight: 600; }
    .feature-card p { font-size: 0.78rem; color: #78909C; margin: 0; line-height: 1.4; }

    .quick-section {
        background: #F5F9FF;
        border: 1px solid #E3F2FD;
        border-radius: 16px;
        padding: 1.2rem;
        margin-bottom: 1.5rem;
    }
    .quick-section h3 { color: #1565C0; font-size: 0.95rem; font-weight: 600; margin: 0 0 12px 0; }
    .quick-chip {
        background: white;
        border: 1px solid #BBDEFB;
        border-radius: 24px;
        padding: 6px 16px;
        font-size: 0.82rem;
        color: #1565C0;
        font-weight: 500;
        display: inline-block;
        margin: 4px;
    }

    .pro-footer {
        text-align: center;
        padding: 1.5rem 1rem;
        margin-top: 2rem;
        border-top: 2px solid #E3F2FD;
    }
    .pro-footer .footer-logo { font-size: 1.5rem; margin-bottom: 6px; }
    .pro-footer .footer-name { color: #1565C0; font-size: 0.95rem; font-weight: 600; margin-bottom: 4px; }
    .pro-footer .footer-sub { color: #90A4AE; font-size: 0.78rem; }
    .pro-footer .footer-disclaimer { color: #B0BEC5; font-size: 0.72rem; margin-top: 8px; }

    [data-testid="stSidebar"] { background: linear-gradient(180deg, #F8FBFF 0%, #EDF4FF 100%); }
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #1565C0; font-size: 1rem; font-weight: 600;
        padding-bottom: 6px; border-bottom: 2px solid #E3F2FD; margin-bottom: 10px;
    }
    .sidebar-status {
        background: #E8F5E9; border: 1px solid #A5D6A7;
        border-radius: 10px; padding: 8px 12px;
        font-size: 0.82rem; color: #2E7D32; margin-bottom: 10px;
    }
    .sidebar-stat {
        background: white; border: 1px solid #E3F2FD;
        border-radius: 10px; padding: 8px 12px;
        margin-bottom: 6px; font-size: 0.82rem; color: #37474F;
    }
    .sidebar-stat strong { color: #1565C0; }

    .stButton > button {
        border-radius: 24px !important;
        border: 1px solid #BBDEFB !important;
        background: white !important;
        color: #1565C0 !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        padding: 6px 16px !important;
    }
    .stButton > button:hover {
        background: #1565C0 !important;
        color: white !important;
    }
    [data-testid="stSidebar"] .stButton > button {
        background: #FFEBEE !important;
        color: #C62828 !important;
        border-color: #FFCDD2 !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background: #C62828 !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)


def render_sidebar():
    with st.sidebar:
        st.markdown("### About MediCare AI")
        st.markdown("MediCare AI provides evidence-based health information powered by Google Gemini and a curated medical knowledge base.")
        st.markdown('<div class="sidebar-status">System Status: Online</div>', unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("### Health Topics")
        topics = {
            "Common Symptoms": "cold, flu, headaches, fatigue",
            "General Diseases": "diabetes, hypertension, allergies",
            "Healthy Lifestyle": "exercise, sleep, stress management",
            "Nutrition & Diet": "balanced diet, hydration, gut health",
            "Preventive Care": "vaccines, screenings, sun protection",
            "First Aid": "burns, choking, wound care, CPR",
            "Mental Health": "anxiety, depression, mindfulness",
        }
        for topic, desc in topics.items():
            st.markdown(f"**{topic}**  \n_{desc}_")
        st.markdown("---")
        st.markdown("### Conversation Stats")
        if "chatbot" in st.session_state and st.session_state.chatbot:
            summary = st.session_state.chatbot.get_conversation_summary()
            st.markdown(f'<div class="sidebar-stat"><strong>{summary["total_messages"]}</strong> total messages</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="sidebar-stat"><strong>{summary["user_messages"]}</strong> questions asked</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="sidebar-stat"><strong>{summary["assistant_messages"]}</strong> responses given</div>', unsafe_allow_html=True)
        if st.button("Clear Conversation", use_container_width=True):
            if "chatbot" in st.session_state and st.session_state.chatbot:
                st.session_state.chatbot.clear_conversation()
            st.session_state.messages = []
            st.rerun()
        st.markdown("---")
        st.markdown("### Ask a Question")
        quick_questions = [
            "What are the symptoms of the flu?",
            "How can I lower blood pressure naturally?",
            "What should I eat for a healthy heart?",
            "How do I treat a minor burn at home?",
            "What are effective ways to manage stress?",
            "How much sleep do adults need?",
        ]
        for q in quick_questions:
            if st.button(q, key=f"quick_{q}", use_container_width=True):
                st.session_state.user_input = q
                st.rerun()
        st.markdown("---")
        st.markdown('<div class="pro-footer"><div class="footer-logo">MediCare AI</div><div class="footer-name">Healthcare AI Assistant</div><div class="footer-sub">Powered by OpenRouter + LangChain + FAISS</div><div class="footer-disclaimer">Not a substitute for professional medical advice</div></div>', unsafe_allow_html=True)


def initialize_chatbot():
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = HealthcareChatbot()
    return st.session_state.chatbot


def main():
    load_css()

    st.markdown("""
    <div class="pro-header">
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:6px;">
            <div style="font-size:2.2rem;background:rgba(255,255,255,0.2);width:52px;height:52px;display:flex;align-items:center;justify-content:center;border-radius:14px;">+</div>
            <h1 style="color:white;font-size:1.7rem;font-weight:700;margin:0;">MediCare AI</h1>
        </div>
        <p style="color:rgba(255,255,255,0.9);font-size:0.92rem;margin:4px 0 0 64px;">Your AI-powered healthcare information companion</p>
        <div style="display:flex;gap:8px;margin-top:12px;padding-left:64px;">
            <span style="background:rgba(255,255,255,0.2);padding:4px 12px;border-radius:20px;font-size:0.75rem;color:white;border:1px solid rgba(255,255,255,0.15);">RAG Powered</span>
            <span style="background:rgba(255,255,255,0.2);padding:4px 12px;border-radius:20px;font-size:0.75rem;color:white;border:1px solid rgba(255,255,255,0.15);">Evidence-Based</span>
            <span style="background:rgba(255,255,255,0.2);padding:4px 12px;border-radius:20px;font-size:0.75rem;color:white;border:1px solid rgba(255,255,255,0.15);">24/7 Available</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="pro-disclaimer">
        <strong>Medical Disclaimer:</strong> This AI assistant provides general health
        information for educational purposes only. It is <strong>not</strong> a substitute for
        professional medical advice, diagnosis, or treatment. Always consult a qualified
        healthcare provider. <strong>In case of emergency, call 108 / 911.</strong>
    </div>
    """, unsafe_allow_html=True)

    chatbot = initialize_chatbot()

    if not chatbot.is_initialized:
        st.error(f"**Initialization Error:** {chatbot.initialization_error}\n\n**Setup Steps:**\n1. Create a .env file in the project root\n2. Add: OPENROUTER_API_KEY=your_key_here\n3. Get a free key at: https://openrouter.ai/keys\n4. Restart the application")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if not st.session_state.messages:
        st.markdown("""
        <div class="features-grid">
            <div class="feature-card"><span class="card-icon">+</span><h3>Health Information</h3><p>Evidence-based info about symptoms and diseases</p></div>
            <div class="feature-card"><span class="card-icon">+</span><h3>Nutrition & Diet</h3><p>Dietary guidance and healthy eating tips</p></div>
            <div class="feature-card"><span class="card-icon">+</span><h3>First Aid Guide</h3><p>Guidance for common injuries and emergencies</p></div>
            <div class="feature-card"><span class="card-icon">+</span><h3>Preventive Care</h3><p>Vaccinations, screenings and health measures</p></div>
            <div class="feature-card"><span class="card-icon">+</span><h3>Mental Wellness</h3><p>Stress management and mental health support</p></div>
            <div class="feature-card"><span class="card-icon">+</span><h3>Lifestyle Tips</h3><p>Exercise, fitness and healthy living advice</p></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="quick-section">
            <h3>Quick Questions to Get Started</h3>
            <div>
                <span class="quick-chip">What are flu symptoms?</span>
                <span class="quick-chip">How to lower blood pressure?</span>
                <span class="quick-chip">Healthy diet tips</span>
                <span class="quick-chip">How to treat a burn?</span>
                <span class="quick-chip">Stress management</span>
                <span class="quick-chip">How much water to drink?</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("Type your health question here...", key="main_chat_input")

    if "user_input" in st.session_state and st.session_state.user_input:
        user_input = st.session_state.user_input
        st.session_state.user_input = None

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Searching medical knowledge base..."):
                result = chatbot.chat(user_input)
                response = result["response"]
                message_placeholder = st.empty()
                full_response = ""
                for chunk in response.split(" "):
                    full_response += chunk + " "
                    time.sleep(0.012)
                    message_placeholder.markdown(full_response + "")
                message_placeholder.markdown(full_response)

                if result.get("sources"):
                    with st.expander("View Sources & References", expanded=False):
                        for src in result["sources"]:
                            st.markdown(f"**{src['topic']}**  \nSource: {src['source']}  \nCategory: {src['category']}")

        st.session_state.messages.append({"role": "assistant", "content": response})

    st.markdown('<div class="pro-footer"><div class="footer-logo">MediCare AI</div><div class="footer-name">Healthcare AI Assistant</div><div class="footer-sub">Powered by OpenRouter + LangChain + FAISS | Built with Streamlit</div><div class="footer-disclaimer">Always consult a qualified healthcare professional for medical advice.</div></div>', unsafe_allow_html=True)


if __name__ == "__main__":
    render_sidebar()
    main()
