# Use a imagem base Python
FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1

# Instalar o supervisord e outras dependências de construção
RUN apt-get update && \
    apt-get install -y supervisor && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos de dependência e instalá-los
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar toda a aplicação (incluindo as pastas 'app' e os arquivos de execução)
COPY . /app/

# Expor ambas as portas
EXPOSE 8000 8501

# Comando final: iniciar o supervisord
CMD ["/usr/bin/supervisord", "-c", "supervisord.conf"]