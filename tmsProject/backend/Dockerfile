# backend/Dockerfile
# FROM python:latest

# WORKDIR /app

# COPY requirements.txt requirements.txt
# RUN pip install -r requirements.txt

# COPY . .

# CMD ["flask", "run", "--host=0.0.0.0"]

# example

FROM python:latest
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY /app/app.py /app/
COPY /app/templates /app/templates/
EXPOSE 5000
CMD ["python", "/app/app.py"]
