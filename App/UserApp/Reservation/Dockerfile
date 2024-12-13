FROM python:3.11 

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:app"]