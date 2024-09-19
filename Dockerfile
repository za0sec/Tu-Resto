FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

RUN pip install gunicorn

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]