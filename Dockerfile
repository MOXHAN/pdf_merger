FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache -r requirements.txt

COPY . .

EXPOSE 5100

CMD ["python", "app.py"]