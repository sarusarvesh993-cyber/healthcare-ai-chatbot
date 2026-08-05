from typing import List, Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ChatMessage:
    role: str
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    sources: Optional[List[Dict]] = None


@dataclass
class LangChainStyleMessage:
    content: str
    type: str


class ConversationMemoryManager:
    def __init__(self, max_history: int = 20, window_size: int = 10):
        self.max_history = max_history
        self.window_size = window_size
        self.chat_history: List[ChatMessage] = []
        self.langchain_pairs: List[tuple] = []

    def add_user_message(self, content: str) -> None:
        message = ChatMessage(role='user', content=content)
        self.chat_history.append(message)
        if len(self.chat_history) > self.max_history:
            self.chat_history = self.chat_history[-self.max_history:]

    def add_assistant_message(self, content: str, sources: Optional[List[Dict]] = None) -> None:
        message = ChatMessage(role='assistant', content=content, sources=sources)
        self.chat_history.append(message)
        if len(self.chat_history) > self.max_history:
            self.chat_history = self.chat_history[-self.max_history:]

    def add_to_langchain_memory(self, user_input: str, ai_response: str) -> None:
        self.langchain_pairs.append((user_input, ai_response))
        if len(self.langchain_pairs) > self.window_size:
            self.langchain_pairs = self.langchain_pairs[-self.window_size:]

    def get_langchain_history(self) -> List:
        result = []
        for user_msg, ai_msg in self.langchain_pairs:
            result.append(LangChainStyleMessage(content=user_msg, type='human'))
            result.append(LangChainStyleMessage(content=ai_msg, type='ai'))
        return result

    def get_display_history(self) -> List[Dict]:
        return [
            {
                'role': msg.role,
                'content': msg.content,
                'timestamp': msg.timestamp.strftime('%I:%M %p'),
                'sources': msg.sources,
            }
            for msg in self.chat_history
        ]

    def get_recent_context(self, n: int = 3) -> str:
        recent = self.chat_history[-(n * 2):] if self.chat_history else []
        if not recent:
            return 'No previous conversation context.'
        context_parts = []
        for msg in recent:
            role = 'User' if msg.role == 'user' else 'Assistant'
            content = msg.content[:300] + '...' if len(msg.content) > 300 else msg.content
            context_parts.append(f'{role}: {content}')
        return '\n'.join(context_parts)

    def clear_history(self) -> None:
        self.chat_history.clear()
        self.langchain_pairs.clear()

    def get_summary(self) -> Dict:
        total_messages = len(self.chat_history)
        user_messages = sum(1 for m in self.chat_history if m.role == 'user')
        assistant_messages = total_messages - user_messages
        return {
            'total_messages': total_messages,
            'user_messages': user_messages,
            'assistant_messages': assistant_messages,
            'has_history': total_messages > 0,
        }
