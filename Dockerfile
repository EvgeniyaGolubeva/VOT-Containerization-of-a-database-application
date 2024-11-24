FROM python:3.9
WORKDIR /app
COPY backend/ /app/backend
COPY static/ /app/static
RUN pip install --no-cache-dir -r /app/backend/requirements.txt
EXPOSE 8000
CMD ["python", "/app/backend/app.py"]
