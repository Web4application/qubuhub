#!/bin/bash
set -e

PROJECT_NAME="my-ai-docker-project"
AI_WEBAPP_ZIP="https://github.com/QUBUHUB/web4/files/14301670/AI-webapp-main.zip"
GPT_PILOT_ZIP="https://github.com/QUBUHUB/web4/files/14301672/gpt-pilot-main.zip"

echo "🚀 Setting up $PROJECT_NAME..."
mkdir -p "$PROJECT_NAME"
cd "$PROJECT_NAME"

# Download AI-webapp
curl -L -o AI-webapp-main.zip "$AI_WEBAPP_ZIP"
unzip -q AI-webapp-main.zip -d AI-webapp
rm AI-webapp-main.zip

# Download GPT-pilot
curl -L -o gpt-pilot-main.zip "$GPT_PILOT_ZIP"
unzip -q gpt-pilot-main.zip -d gpt-pilot
rm gpt-pilot-main.zip

# Create Dockerfiles
cat > AI-webapp/Dockerfile <<'EOL'
FROM node:20
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
EOL

cat > gpt-pilot/Dockerfile <<'EOL'
FROM node:20
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 4000
CMD ["npm", "start"]
EOL

# Create docker-compose with internal bridge
cat > docker-compose.yml <<'EOL'
version: "3.9"

services:
  ai-webapp:
    build: ./AI-webapp
    ports:
      - "3000:3000"
    volumes:
      - ./AI-webapp:/app
    command: npm start
    depends_on:
      - gpt-pilot
    environment:
      GPT_PILOT_URL: "http://gpt-pilot:4000"

  gpt-pilot:
    build: ./gpt-pilot
    expose:
      - "4000"
    volumes:
      - ./gpt-pilot:/app
    command: npm start
EOL

echo "✅ Setup complete!"
echo "➡ Run: docker compose up --build"
