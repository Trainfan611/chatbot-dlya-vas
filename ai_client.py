"""
Универсальный AI клиент с поддержкой Gemini, GigaChat, Groq.
"""

import os
import logging
from typing import Optional, List
from dataclasses import dataclass, field

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logging.warning("google-generativeai не установлен")

import requests

logger = logging.getLogger("AIClient")


@dataclass
class ChatSession:
    """Сессия чата для пользователя."""
    user_id: int
    history: List[dict] = field(default_factory=list)
    
    def add_message(self, role: str, text: str):
        self.history.append({"role": role, "parts": [text]})
        if len(self.history) > 10:
            self.history = self.history[-10:]
    
    def clear_history(self):
        self.history = []


class AIClient:
    """Универсальный AI клиент."""
    
    def __init__(self, provider: str = "gemini", **kwargs):
        """
        Инициализация.
        
        Args:
            provider: "gemini", "gigachat", "groq"
            **kwargs: Ключи API
        """
        self.provider = provider
        self._sessions: dict[int, ChatSession] = {}
        
        if provider == "gemini":
            self.api_key = kwargs.get("api_key", "")
            if GEMINI_AVAILABLE:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                
                # Пробуем доступные модели по порядку
                self.model_name = None
                for model in ["gemini-1.5-flash", "gemini-1.5-flash-8b", "gemini-pro"]:
                    try:
                        self.model = genai.GenerativeModel(model)
                        self.model_name = model
                        logger.info(f"✅ Gemini модель {model} доступна")
                        break
                    except:
                        continue
                
                if not self.model_name:
                    raise ValueError("Ни одна модель Gemini не доступна")
            else:
                raise ImportError("google-generativeai не установлен")
                
        elif provider == "gigachat":
            self.auth_key = kwargs.get("auth_key", "")
            self.model = "GigaChat"
            self.base_url = "https://gigachat.devices.sberbank.ru/api/v2"
            logger.info(f"✅ GigaChat инициализирован")
            
        elif provider == "groq":
            self.api_key = kwargs.get("api_key", "")
            self.model = "llama-3.1-8b-instant"
            logger.info(f"✅ Groq (Llama 3.1) инициализирован")
            
        else:
            raise ValueError(f"Неизвестный провайдер: {provider}")
    
    def get_session(self, user_id: int) -> ChatSession:
        if user_id not in self._sessions:
            self._sessions[user_id] = ChatSession(user_id=user_id)
        return self._sessions[user_id]
    
    def clear_session(self, user_id: int):
        if user_id in self._sessions:
            self._sessions[user_id].clear_history()
    
    async def ask(self, user_id: int, message: str, system_prompt: str = "") -> str:
        """Запрос к AI."""
        session = self.get_session(user_id)
        session.add_message("user", message)
        
        try:
            if self.provider == "gemini":
                return await self._ask_gemini(session, message, system_prompt)
            elif self.provider == "gigachat":
                return self._ask_gigachat(session, message, system_prompt)
            elif self.provider == "groq":
                return self._ask_groq(session, message, system_prompt)
        except Exception as e:
            logger.error(f"Ошибка AI: {e}")
            session.clear_history()
            return "Произошла ошибка. Используйте /clear"
    
    async def _ask_gemini(self, session: ChatSession, message: str, system_prompt: str) -> str:
        """Запрос к Gemini."""
        import google.generativeai as genai
        
        try:
            # Создаём чат с историей
            chat = self.model.start_chat(
                history=session.history[:-1] if len(session.history) > 1 else None
            )
            
            # Отправляем сообщение
            response = await chat.send_message_async(message)
            answer = response.text
            
            return answer
            
        except Exception as e:
            logger.error(f"Gemini ошибка: {e}")
            # Пробуем без истории
            try:
                response = self.model.generate_content(message)
                return response.text
            except:
                return f"Ошибка Gemini: {e}"
    
    def _ask_gigachat(self, session: ChatSession, message: str, system_prompt: str) -> str:
        """Запрос к GigaChat."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.extend(session.history)
        
        headers = {
            "Authorization": f"Bearer {self.auth_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1024
        }
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            return data["choices"][0]["message"]["content"]
        else:
            logger.error(f"GigaChat ошибка: {response.status_code}")
            return f"Ошибка GigaChat ({response.status_code})"
    
    def _ask_groq(self, session: ChatSession, message: str, system_prompt: str) -> str:
        """Запрос к Groq."""
        messages = [{"role": "system", "content": system_prompt}] if system_prompt else []
        messages.extend(session.history)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": 1024,
            "temperature": 0.7
        }
        
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            return data["choices"][0]["message"]["content"]
        else:
            logger.error(f"Groq ошибка: {response.status_code}")
            return f"Ошибка Groq ({response.status_code})"
    
    def get_stats(self) -> dict:
        return {
            "active_sessions": len(self._sessions),
            "model": self.model_name if self.provider == "gemini" else self.model,
            "provider": self.provider
        }


# Глобальный клиент
ai_client: Optional[AIClient] = None


def init_ai(provider: str = "gemini", **kwargs) -> AIClient:
    """Инициализировать AI клиент."""
    global ai_client
    ai_client = AIClient(provider, **kwargs)
    return ai_client


def get_ai_client() -> AIClient:
    """Получить AI клиент."""
    if ai_client is None:
        raise RuntimeError("AI клиент не инициализирован")
    return ai_client
