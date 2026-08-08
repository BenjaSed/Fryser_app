ARG BUILD_FROM=python:3.11-alpine
FROM $BUILD_FROM

WORKDIR /app

# Install dos2unix tool
RUN apk add --no-cache dos2unix

# Copy application files
COPY app /app/app
COPY server.py /app/server.py
COPY run.sh /app/run.sh

# Fix line endings & ensure executable permissions
RUN dos2unix /app/run.sh && chmod +x /app/run.sh

# Install Python packages (added python-multipart)
RUN pip install --no-cache-dir fastapi uvicorn aiofiles python-multipart

CMD ["/app/run.sh"]