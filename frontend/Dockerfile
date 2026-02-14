FROM python:3.12-slim


WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Using 0.0.0.0 to bind to all interfaces in container
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
