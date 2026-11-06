FROM python:3.12-slim
WORKDIR /app
COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt
COPY backend backend
COPY frontend frontend
RUN useradd -m app && chown -R app /app
USER app
WORKDIR /app/backend
ENV PORT=8000
EXPOSE 8000
# GEMINI_API_KEY entra em runtime: docker run -e GEMINI_API_KEY=... (nunca no build)
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT"]
