# 1. Usar a imagem oficial do Python
FROM python:3.11

# 2. Defini o diretório de trabalho dentro do container
WORKDIR /converter_api

# 3. Copia os arquivos do projeto para dentro do container
COPY requirements.txt .

# 4. Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copia todos os arquivos do projeto
COPY . .

# 6. Define a porta que o Django usará
EXPOSE 8000

# 7. Roda os comandos para iniciar o servidor Django
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "crypto_converter.wsgi:application"]
