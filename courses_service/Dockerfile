FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install flask pandas

EXPOSE 5004

CMD ["python", "app.py"]