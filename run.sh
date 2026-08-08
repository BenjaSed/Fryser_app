#!/bin/sh

echo "Starting fryser app..."
cd /app
exec uvicorn server:app --host 0.0.0.0 --port 8000