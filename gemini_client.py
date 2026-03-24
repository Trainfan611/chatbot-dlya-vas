"""
Модуль для работы с Google Gemini API.
Бесплатная модель: gemini-2.0-flash-exp (или gemini-1.5-flash)
"""

import google.generativeai as genai
from typing import Optional, List
from dataclasses import dataclass, field
import logging

logger = logging.getLogger("GeminiAI")


@dataclass
class Message:
    """Сообщение для истории чата."""
    role: str  # 'user' или 'model'
    text: str


@dataclass
class ChatSession:
    """Сессия чата для одного пользователя."""
    user_id: int
    history: List[Message] = field(default_factory=list)
    
    def add_message(self, role: str, text: str):
        """Добавить сообщение в историю."""
        self.history.append(Message(role=role, text=text))
        # Ограничиваем историю последними 20 сообщениями
        if len(self.history) > 20:
            self.history = self.history[-20:]
    
    def clear_history(self):
        """Очистить историю."""
        self.history = []


class GeminiAIClient:
    """Клиент для работы с Google Gemini API."""
    
    def __init__(self, api_key: str):
        """
        Инициализация клиента.
        
        Args:
            api_key: API ключ Google Gemini
        """
        self.api_key = api_key
        self.model = None
        self._sessions: dict[int, ChatSession] = {}
        
        # Настраиваем API
        genai.configure(api_key=api_key)
        
        # Используем бесплатную модель gemini-2.0-flash-exp или gemini-1.5-flash
        self.model_name = "gemini-2.0-flash-exp"
        try:
            self.model = genai.GenerativeModel(self.model_name)
            logger.info(f"✅ Gemini модель {self.model_name} инициализирована")
        except Exception as e:
            logger.warning(f"Не удалось инициализировать {self.model_name}, пробуем gemini-1.5-flash")
            self.model_name = "gemini-1.5-flash"
            self.model = genai.GenerativeModel(self.model_name)
            logger.info(f"✅ Gemini модель {self.model_name} инициализирована")
    
    def get_session(self, user_id: int) -> ChatSession:
        """Получить или создать сессию для пользователя."""
        if user_id not in self._sessions:
            self._sessions[user_id] = ChatSession(user_id=user_id)
            logger.info(f"Создана новая сессия для пользователя {user_id}")
        return self._sessions[user_id]
    
    def clear_session(self, user_id: int):
        """Очистить историю чата пользователя."""
        if user_id in self._sessions:
            self._sessions[user_id].clear_history()
            logger.info(f"История чата пользователя {user_id} очищена")
    
    async def ask(self, user_id: int, message: str, system_prompt: str = "") -> str:
        """
        Отправить запрос к Gemini API.
        
        Args:
            user_id: ID пользователя
            message: Сообщение пользователя
            system_prompt: Системная инструкция (опционально)
            
        Returns:
            Ответ от нейросети
        """
        session = self.get_session(user_id)
        
        # Добавляем сообщение пользователя в историю
        session.add_message("user", message)
        
        try:
            # Формируем контекст из истории
            chat_history = []
            if system_prompt:
                chat_history.append({
                    "role": "user",
                    "parts": [f"Системная инструкция: {system_prompt}"]
                })
                chat_history.append({
                    "role": "model", 
                    "parts": ["Понял, буду следовать инструкции."]
                })
            
            # Добавляем историю сообщений
            for msg in session.history[:-1]:  # Все кроме последнего (оно уже в message)
                chat_history.append({
                    "role": "user" if msg.role == "user" else "model",
                    "parts": [msg.text]
                })
            
            # Создаём чат с историей
            chat = self.model.start_chat(history=chat_history if chat_history else None)
            
            # Отправляем сообщение
            response = await chat.send_message_async(message)
            
            # Получаем ответ
            answer = response.text
            
            # Добавляем ответ модели в историю
            session.add_message("model", answer)
            
            logger.info(f"Пользователь {user_id}: {message[:50]}... -> Ответ: {answer[:50]}...")
            
            return answer
            
        except Exception as e:
            logger.error(f"Ошибка при запросе к Gemini: {e}")
            # Очищаем сессию при ошибке и пробуем снова с чистого листа
            session.clear_history()
            try:
                response = self.model.generate_content(message)
                return response.text
            except Exception as e2:
                logger.error(f"Повторная ошибка: {e2}")
                return "Произошла ошибка при обработке запроса. Попробуйте позже."
    
    def get_stats(self) -> dict:
        """Получить статистику по сессиям."""
        return {
            "active_sessions": len(self._sessions),
            "model": self.model_name
        }


# Глобальный экземпляр (будет инициализирован позже)
gemini_client: Optional[GeminiAIClient] = None


def init_gemini(api_key: str) -> GeminiAIClient:
    """Инициализировать глобальный клиент Gemini."""
    global gemini_client
    gemini_client = GeminiAIClient(api_key)
    return gemini_client


def get_gemini_client() -> GeminiAIClient:
    """Получить глобальный клиент Gemini."""
    if gemini_client is None:
        raise RuntimeError("Gemini клиент не инициализирован. Вызовите init_gemini()")
    return gemini_client
