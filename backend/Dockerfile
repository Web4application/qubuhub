FROM node:18-buster AS node
WORKDIR /app
COPY package*.json /app/
RUN npm install

FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
