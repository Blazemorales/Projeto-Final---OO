FROM python:3.12-slim

# 2. Definir o diretório de trabalho 
WORKDIR /bmeta

# 3. Copiar o arquivo de dependências primeiro para otimizar o cache
COPY requirements.txt .

# 4. Instalar as dependências do arquivo
RUN pip install --no-cache-dir -r requirements.txt

# 5. 
COPY . .

# 6. Expor a porta que o aplicativo usa 
EXPOSE 8080

# 7. Comando para executar a aplicação 
CMD ["python3", "startserver.py"]