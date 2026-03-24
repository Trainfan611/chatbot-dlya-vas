@echo off
echo ========================================
echo  GitHub Deploy Script for AI ChatBot
echo ========================================
echo.

REM Проверка git
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Git не найден! Установите: https://git-scm.com
    pause
    exit /b 1
)

echo [1/5] Инициализация git...
cd /d "%~dp0"
git init 2>nul

echo [2/5] Добавление файлов...
git add .

echo [3/5] Commit...
git commit -m "AI ChatBot deployment"

echo.
echo [4/5] Введите URL вашего репозитория GitHub:
echo Пример: https://github.com/username/ai-telegram-bot.git
echo.
set /p REPO_URL="URL репозитория: "

if "%REPO_URL%"=="" (
    echo [ERROR] URL не введён!
    pause
    exit /b 1
)

echo [5/5] Push на GitHub...
git remote remove origin 2>nul
git remote add origin %REPO_URL%
git push -u origin main --force

echo.
echo ========================================
echo  Готово! Проект загружен на GitHub.
echo ========================================
echo.
echo Далее:
echo 1. Зайдите на https://railway.app
echo 2. Создайте новый проект из GitHub
echo 3. Выберите ваш репозиторий
echo 4. Добавьте переменные окружения:
echo    - TELEGRAM_TOKEN
echo    - GEMINI_API_KEY
echo.
pause
