FROM python:3.11

WORKDIR /converter_api

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "crypto_converter.wsgi:application"]
