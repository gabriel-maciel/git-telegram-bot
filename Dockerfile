# Usa una imagen base de Python 3
FROM python:3.9-slim

# Crea un directorio para el bot
WORKDIR /bot

# Copia los requisitos e instala las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el script del bot
COPY bot.py .

# Expone el puerto en el que el bot está escuchando (5000 en tu caso)
EXPOSE 5000

# Ejecuta el bot
CMD ["python", "./bot.py"]
