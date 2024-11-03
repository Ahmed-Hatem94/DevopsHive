FROM python:3.11-slim
WORKDIR /app
COPY version.py .
CMD [ "python", "version.py" ]