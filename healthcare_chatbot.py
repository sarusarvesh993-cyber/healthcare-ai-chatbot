import os
import re
import json
from typing import Dict, List, Optional, Tuple

from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

from prompt_engineering import (
    MEDICAL_SYSTEM_PROMPT,
    MEDICAL_DISCLAIMER,
    SHORT_DISCLAIMER,
    EMERGENCY_RESPONSE,
    OUT_OF_SCOPE_RESPONSE,
    GREETING_RESPONSE,
    format_context,
)
from conversation_memory import ConversationMemoryManager

load_dotenv()

EMERGENCY_KEYWORDS = [
    'chest pain', 'heart attack', 'can\'t breathe', 'cannot breathe',
    'difficulty breathing', 'severe bleeding', 'unconscious', 'stroke',
    'suicide', 'kill myself', 'want to die', 'overdose', 'poisoning',
    'seizure', 'anaphylaxis', 'choking', 'drowning', 'severe burn',
    'broken bone', 'bone sticking out', 'unresponsive', 'not breathing',
]

GREETING_PATTERNS = [
    r'\b(hi|hello|hey|good morning|good afternoon|good evening|howdy)\b',
    r'\b(how are you|what\'s up|sup|yo)\b',
    r'\b(who are you|what are you|what can you do|help me)\b',
]

OUT_OF_SCOPE_INDICATORS = [
    'weather', 'stock price', 'recipe for cake', 'movie recommendation',
    'sports score', 'programming', 'javascript', 'python code',
    'translate', 'calculator', 'math problem', 'tell me a joke',
    'buy', 'purchase', 'order', 'shopping',
]


class HealthcareChatbot:
    def __init__(self, model_name=None):
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        self.model_name = model_name or os.getenv('LLM_MODEL', 'google/gemini-2.0-flash-exp:free')
        self.is_initialized = False
        self.initialization_error = None
        self.llm = None
        self.vector_store = None
        self.embeddings = None
        self.memory = ConversationMemoryManager()
        self.retriever = None
        self._initialize()

    def _initialize(self):
        try:
            if not self.api_key:
                raise ValueError('OPENROUTER_API_KEY not found. Get a key at: https://openrouter.ai/keys')

            self.llm = ChatOpenAI(
                model=self.model_name,
                openai_api_key=self.api_key,
                openai_api_base='https://openrouter.ai/api/v1',
                temperature=0.4,
                max_tokens=2048,
                default_headers={
                    'HTTP-Referer': 'http://localhost:8501',
                    'X-Title': 'Healthcare AI Chatbot',
                },
            )

            print('Loading embeddings model...')
            self.embeddings = HuggingFaceEmbeddings(
                model_name='all-MiniLM-L6-v2',
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True},
            )

            self._initialize_vector_store()
            self.is_initialized = True
            print('Chatbot initialized successfully!')

        except Exception as e:
            self.initialization_error = str(e)
            self.is_initialized = False
            print(f'Initialization error: {e}')

    def _initialize_vector_store(self):
        store_path = os.path.join(os.path.dirname(__file__), 'data', 'faiss_medical_store')
        if os.path.exists(store_path):
            self.vector_store = FAISS.load_local(store_path, self.embeddings, allow_dangerous_deserialization=True)
            self.retriever = self.vector_store.as_retriever(search_type='similarity', search_kwargs={'k': 3})
        else:
            self._create_vector_store()

    def _create_vector_store(self):
        kb_path = os.path.join(os.path.dirname(__file__), 'data', 'medical_knowledge_base.json')
        if not os.path.exists(kb_path):
            print('Warning: Knowledge base not found.')
            return

        with open(kb_path, 'r') as f:
            knowledge_base = json.load(f)

        documents = []
        for entry in knowledge_base:
            doc = Document(
                page_content=entry['content'],
                metadata={'id': entry['id'], 'topic': entry['topic'], 'source': entry['source'], 'category': entry['category']},
            )
            documents.append(doc)

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50, separators=['\n\n', '\n', '. ', ' ', ''])
        chunks = text_splitter.split_documents(documents)
        self.vector_store = FAISS.from_documents(chunks, self.embeddings)

        store_path = os.path.join(os.path.dirname(__file__), 'data', 'faiss_medical_store')
        self.vector_store.save_local(store_path)
        self.retriever = self.vector_store.as_retriever(search_type='similarity', search_kwargs={'k': 3})
        print(f'Vector store created with {len(chunks)} chunks!')

    def _is_emergency(self, query):
        return any(keyword in query.lower() for keyword in EMERGENCY_KEYWORDS)

    def _is_greeting(self, query):
        query_lower = query.lower().strip()
        for pattern in GREETING_PATTERNS:
            if re.search(pattern, query_lower) and len(query_lower.split()) <= 6:
                return True
        return False

    def _is_out_of_scope(self, query):
        return any(indicator in query.lower() for indicator in OUT_OF_SCOPE_INDICATORS)

    def _classify_query(self, query):
        if self._is_emergency(query): return 'emergency'
        if self._is_greeting(query): return 'greeting'
        if self._is_out_of_scope(query): return 'out_of_scope'
        return 'health_query'

    def _retrieve_context(self, query):
        if not self.retriever: return 'Knowledge base not available.', []
        try:
            docs = self.retriever.get_relevant_documents(query)
            context = format_context(docs)
            sources = [{'topic': d.metadata.get('topic', 'Unknown'), 'source': d.metadata.get('source', 'Unknown'), 'category': d.metadata.get('category', 'general')} for d in docs]
            return context, sources
        except Exception:
            return 'Error retrieving context.', []

    def _generate_health_response(self, query, context, sources):
        try:
            system_prompt = MEDICAL_SYSTEM_PROMPT.format(disclaimer=MEDICAL_DISCLAIMER)
            rag_instruction = f'\n## RETRIEVED KNOWLEDGE BASE CONTEXT:\n{context}\n\n## INSTRUCTIONS:\n- Use the above context to inform your answer when relevant\n- Cite sources from the context when applicable\n- Supplement with general health knowledge if context is insufficient\n- Always be empathetic and clear\n- Include the medical disclaimer at the end of your response\n'
            full_system = system_prompt + '\n' + rag_instruction

            messages = [('system', full_system)]
            chat_history = self.memory.get_langchain_history()
            for msg in chat_history[-6:]:
                if hasattr(msg, 'content'):
                    role = 'human' if msg.__class__.__name__ == 'HumanMessage' else 'ai'
                    messages.append((role, msg.content))
            messages.append(('human', query))

            prompt = ChatPromptTemplate.from_messages(messages)
            chain = prompt | self.llm
            response = chain.invoke({'input': query})
            response_text = response.content if hasattr(response, 'content') else str(response)

            if 'disclaimer' not in response_text.lower():
                response_text += SHORT_DISCLAIMER

            if sources:
                response_text += '\n\n---\n**Sources Referenced:**\n'
                seen = set()
                for src in sources:
                    key = f"{src['topic']} - {src['source']}"
                    if key not in seen:
                        seen.add(key)
                        response_text += f"- _{src['topic']}_ — {src['source']}\n"

            return response_text

        except Exception as e:
            return f'I apologize, but I encountered an issue. Please try rephrasing.\n\n_Technical details: {str(e)}_'

    def chat(self, user_message):
        if not self.is_initialized:
            return {'response': f'**Initialization Error:** {self.initialization_error}\n\nGet a key at: https://openrouter.ai/keys', 'sources': [], 'query_type': 'error', 'has_disclaimer': False}

        self.memory.add_user_message(user_message)
        query_type = self._classify_query(user_message)

        if query_type == 'emergency': response, sources = EMERGENCY_RESPONSE, []
        elif query_type == 'greeting': response, sources = GREETING_RESPONSE, []
        elif query_type == 'out_of_scope': response, sources = OUT_OF_SCOPE_RESPONSE, []
        else:
            context, sources = self._retrieve_context(user_message)
            response = self._generate_health_response(user_message, context, sources)

        self.memory.add_assistant_message(response, sources)
        self.memory.add_to_langchain_memory(user_message, response)

        return {'response': response, 'sources': sources, 'query_type': query_type, 'has_disclaimer': 'disclaimer' in response.lower()}

    def clear_conversation(self):
        self.memory.clear_history()

    def get_conversation_summary(self):
        return self.memory.get_summary()
