# API para conversão de moedas e criptomoedas

## 📖  Descrição

Esta API proporciona a conversão de criptomoedas e moedas fiduciárias em tempo real, oferecendo taxas de câmbio atualizadas. 
Desenvolvida com Django e Django REST Framework, a API disponibiliza endpoints seguros para consulta de preços e histórico de conversões.
Além disso, utiliza cache com Redis para otimização de desempenho e oferece suporte a Docker para uma implantação simples.

<br/>

## 🛠️ Funcionalidades

- Conversão de Moedas e Criptomoedas
- Histórico de Conversões
- Cache com Redis
- Autenticação e Segurança
- Integração com Banco de Dados
- Docker para Implantação
<br/>

## 📡 Tecnologias utilizadas 
<div align="center"> 
<img align="left" alt="Python" height="30" width="30" src="https://s3.dualstack.us-east-2.amazonaws.com/pythondotorg-assets/media/files/python-logo-only.svg">
<img align="left" alt="Django" height="30" width="45" src="https://static.djangoproject.com/img/logos/django-logo-negative.svg">
<img align="left" alt="Postgresql" height="30" width="30" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/postgresql/postgresql-original.svg">
<img align="left" alt="docker" height="32" width="35" src="https://github.com/user-attachments/assets/6198150a-b145-449c-ad48-cc12f138bd95">
<img align="left" alt="docker" height="38" width="47" src="https://github.com/user-attachments/assets/0f604e51-e697-4358-b3b5-7f002b52ec58">
</div>
<br/><br/>

## ⏳ Inicialização

Esse projeto foi desenvolvido em ambiente Linux, utilizando as tecnologias citadas anteriormente. Sugiro que você prepare o seu ambiente seguindo os passos abaixo:

A preparação do ambiente consiste em instalar as tecnologias citadas anteriormente de acordo com seu sistema operacional.

Para instalar o Python, acesse: https://www.python.org/downloads/

Para instalar o Postgresql, acesse: https://www.postgresql.org/download/

Para instalar o Docker, acesse: https://www.docker.com/

Execute esses comandos no terminal para usar o docker:
```
# 1. Construir a imagem do Docker
docker-compose build

# 2. Subir os containers
docker-compose up -d
```

<br/>

## 🔮 Implementações futuras
1. Implementar suporte a mais moedas e criptomoedas

2. Implementar a melhoria na performance do cache

3. Implementar sistema de notificações quando uma taxa de câmbio atingir um valor específico

<br/>

## 🔎 Status do Projeto

![Badge em Desenvolvimento](https://img.shields.io/badge/Status-Em%20Desenvolvimento-green)
