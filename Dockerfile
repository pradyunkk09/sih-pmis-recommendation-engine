FROM python:3.11-slim

WORKDIR /app

COPY Requirements.txt .
COPY backend/requirements.txt ./backend_reqs.txt
COPY ml_engine/requirements.txt ./ml_reqs.txt
RUN pip install --no-cache-dir -r Requirements.txt -r backend_reqs.txt -r ml_reqs.txt

COPY . .

ENV PYTHONPATH=/app/backend

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]