"""
Универсальный AI клиент с поддержкой Gemini, GigaChat, Groq.
"""

import os
import logging
import time
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
        self.history.append({"role": role, "content": text})
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
            self._init_gemini(kwargs)
        elif provider == "gigachat":
            self._init_gigachat(kwargs)
        elif provider == "groq":
            self._init_groq(kwargs)
        else:
            raise ValueError(f"Неизвестный провайдер: {provider}")
    
    def _init_gemini(self, kwargs):
        """Инициализация Gemini."""
        self.api_key = kwargs.get("api_key", "")
        if GEMINI_AVAILABLE:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            
            self.model = None
            self.model_name = None
            
            for model_name in ["gemini-pro", "gemini-1.5-flash-latest", "gemini-1.5-flash-8b"]:
                try:
                    logger.info(f"  Проверяю модель {model_name}...")
                    self.model = genai.GenerativeModel(model_name)
                    test_response = self.model.generate_content("Hi", generation_config=genai.types.GenerationConfig(max_output_tokens=10))
                    self.model_name = model_name
                    logger.info(f"✅ Модель {model_name} доступна")
                    break
                except Exception as e:
                    logger.warning(f"  Модель {model_name} недоступна: {e}")
                    continue
            
            if not self.model_name:
                raise ValueError("Ни одна модель Gemini не доступна. Проверьте API ключ.")
        else:
            raise ImportError("google-generativeai не установлен")
    
    def _init_gigachat(self, kwargs):
        """Инициализация GigaChat."""
        self.auth_key = kwargs.get("auth_key", "")
        self.client_id = kwargs.get("client_id", "")
        self.scope = kwargs.get("scope", "GIGACHAT_API_PERS")
        self.model = "GigaChat"
        self.base_url = "https://gigachat.devices.sberbank.ru/api/v2"
        self._access_token = None
        self._token_expires = 0
        logger.info(f"✅ GigaChat инициализирован")
    
    def _init_groq(self, kwargs):
        """Инициализация Groq."""
        self.api_key = kwargs.get("api_key", "")
        self.model = "llama-3.1-8b-instant"
        logger.info(f"✅ Groq (Llama 3.1) инициализирован")
    
    def _get_gigachat_token(self) -> str:
        """Получить access token GigaChat через OAuth."""
        # Если токен ещё действителен, возвращаем его
        if self._access_token and time.time() < self._token_expires:
            return self._access_token
        
        try:
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Basic {self.auth_key}"
            }
            
            data = {"scope": self.scope}
            
            if self.client_id:
                data["client_id"] = self.client_id
            
            response = requests.post(
                "https://ngw.devices.sberbank.ru:9443/api/v2/oauth",
                headers=headers,
                data=data,
                timeout=30,
                verify=False
            )
            
            if response.status_code == 200:
                token_data = response.json()
                self._access_token = token_data["access_token"]
                self._token_expires = time.time() + 1800
                logger.info("✅ Получен новый токен GigaChat")
                return self._access_token
            else:
                logger.error(f"Ошибка получения токена: {response.status_code}")
                return self.auth_key
                
        except Exception as e:
            logger.error(f"Ошибка OAuth: {e}")
            return self.auth_key
    
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
            chat = self.model.start_chat(
                history=session.history[:-1] if len(session.history) > 1 else None
            )
            response = await chat.send_message_async(message)
            return response.text
        except Exception as e:
            logger.error(f"Gemini ошибка: {e}")
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
        
        token = self._get_gigachat_token()
        
        headers = {
            "Authorization": f"Bearer {token}",
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
