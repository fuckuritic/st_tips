FROM python:3.10-slim

WORKDIR /app

# Устанавливаем нужные утилиты
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Клонируем твой репозиторий в /app
RUN git clone https://github.com/fuckuritic/st_tips.git .

# Устанавливаем зависимости Python
RUN pip3 install -r requirements.txt

# Открываем порт
EXPOSE 8501

# Опциональный чемпек состояния
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Запускаем Streamlit, заменив main.py на нужный файл
ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
