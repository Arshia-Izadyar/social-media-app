FROM python:3.11-slim

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

WORKDIR /app


COPY . /app

# CMD ["python3" ,"manage.py" ,"mgirate" ,"0.0.0.0:8000"]