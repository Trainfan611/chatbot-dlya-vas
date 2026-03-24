"""
Модуль для работы с GigaChat API (Сбер, работает в РФ).
Бесплатная модель: GigaChat
"""

import os
import logging
import base64
from typing import Optional, List
from dataclasses import dataclass, field
import requests

logger = logging.getLogger("GigaChatClient")


@dataclass
class ChatSession:
    """Сессия чата для одного пользователя."""
    user_id: int
    history: List[dict] = field(default_factory=list)
    
    def add_message(self, role: str, text: str):
        """Добавить сообщение в историю."""
        self.history.append({"role": role, "content": text})
        # Ограничиваем историю последними 10 сообщениями
        if len(self.history) > 10:
            self.history = self.history[-10:]
    
    def clear_history(self):
        """Очистить историю."""
        self.history = []


class GigaChatClient:
    """Клиент для работы с GigaChat API."""
    
    def __init__(self, auth_key: str):
        """
        Инициализация клиента GigaChat.
        
        Args:
            auth_key: Bearer токен (получить в Sber ID)
        """
        self.auth_key = auth_key
        self.base_url = "https://gigachat.devices.sberbank.ru/api/v2"
        self.model = "GigaChat"
        self._sessions: dict[int, ChatSession] = {}
        self._access_token: Optional[str] = None
        
        logger.info(f"✅ GigaChat клиент инициализирован")
    
    def _get_access_token(self) -> str:
        """Получить access токен."""
        if self._access_token:
            return self._access_token
        
        try:
            # Для авторизации по API ключу
            headers = {
                "Authorization": f"Bearer {self.auth_key}",
                "Content-Type": "application/json"
            }
            
            # Пробуем получить токен
            # Примечание: в продакшене нужно использовать OAuth 2.0 flow
            self._access_token = self.auth_key
            return self._access_token
            
        except Exception as e:
            logger.error(f"Ошибка получения токена: {e}")
            return self.auth_key
    
    def get_session(self, user_id: int) -> ChatSession:
        """Получить или создать сессию."""
        if user_id not in self._sessions:
            self._sessions[user_id] = ChatSession(user_id=user_id)
        return self._sessions[user_id]
    
    def clear_session(self, user_id: int):
        """Очистить историю."""
        if user_id in self._sessions:
            self._sessions[user_id].clear_history()
    
    def ask(self, user_id: int, message: str, system_prompt: str = "") -> str:
        """
        Запрос к GigaChat.
        
        Args:
            user_id: ID пользователя
            message: Сообщение
            system_prompt: Системная инструкция
            
        Returns:
            Ответ GigaChat
        """
        session = self.get_session(user_id)
        session.add_message("user", message)
        
        try:
            # Формируем сообщения
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.extend(session.history)
            
            # Запрос к GigaChat API
            headers = {
                "Authorization": f"Bearer {self._get_access_token()}",
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
                answer = data["choices"][0]["message"]["content"]
                session.add_message("assistant", answer)
                
                logger.info(f"Пользователь {user_id}: {message[:50]}... -> Ответ: {answer[:50]}...")
                return answer
            else:
                logger.error(f"Ошибка API: {response.status_code} - {response.text}")
                return f"Ошибка API ({response.status_code}). Попробуйте позже."
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка запроса: {e}")
            session.clear_history()
            return "Произошла ошибка. Попробуйте позже или используйте /clear"
        except Exception as e:
            logger.error(f"Неизвестная ошибка: {e}")
            return "Произошла ошибка. Попробуйте позже."
    
    def get_stats(self) -> dict:
        """Статистика."""
        return {
            "active_sessions": len(self._sessions),
            "model": self.model,
            "provider": "GigaChat (Сбер)"
        }


# Глобальный клиент
gigachat_client: Optional[GigaChatClient] = None


def init_gigachat(auth_key: str) -> GigaChatClient:
    """Инициализировать глобальный клиент."""
    global gigachat_client
    gigachat_client = GigaChatClient(auth_key)
    return gigachat_client


def get_gigachat_client() -> GigaChatClient:
    """Получить глобальный клиент."""
    if gigachat_client is None:
        raise RuntimeError("GigaChat клиент не инициализирован")
    return gigachat_client
