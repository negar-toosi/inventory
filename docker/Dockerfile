FROM python:3.12-slim
WORKDIR /app
ENV PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
    
COPY requirements/ /app/requirements/
RUN pip install --no-cache-dir -r requirements/dev.txt

COPY . /app
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
