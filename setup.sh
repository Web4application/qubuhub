#!/bin/bash
set -e

PROJECT_NAME="my-ai-project"
AI_WEBAPP_ZIP="https://github.com/QUBUHUB/web4/files/14301670/AI-webapp-main.zip"
GPT_PILOT_ZIP="https://github.com/QUBUHUB/web4/files/14301672/gpt-pilot-main.zip"

echo "🚀 Setting up $PROJECT_NAME..."
mkdir -p "$QUBUHUB"
cd "$QUBUHUB"

# --- Download & Extract AI-webapp ---
echo "📥 Downloading AI-webapp..."
curl -L -o AI-webapp-main.zip "$AI_WEBAPP_ZIP"
unzip -q AI-webapp-main.zip -d AI-webapp
rm AI-webapp-main.zip

# --- Download & Extract GPT-pilot ---
echo "📥 Downloading GPT-pilot..."
curl -L -o gpt-pilot-main.zip "$GPT_PILOT_ZIP"
unzip -q gpt-pilot-main.zip -d gpt-pilot
rm gpt-pilot-main.zip

# --- Install dependencies ---
if [ -f AI-webapp/package.json ]; then
    echo "📦 Installing AI-webapp dependencies..."
    cd AI-webapp
    npm install
    cd ..
fi

if [ -f gpt-pilot/package.json ]; then
    echo "📦 Installing GPT-pilot dependencies..."
    cd gpt-pilot
    npm install
    cd ..
fi

# --- Link GPT-pilot into AI-webapp ---
echo "🔗 Linking GPT-pilot into AI-webapp..."
mkdir -p AI-webapp/modules
cp -r gpt-pilot AI-webapp/modules/

# --- Create start script ---
echo "🛠 Creating start script..."
cat > start.sh <<EOL
#!/bin/bash
echo "🚀 Starting AI-webapp & GPT-pilot..."
(cd AI-webapp && npm start) &
(cd gpt-pilot && npm start) &
wait
EOL
chmod +x start.sh

echo "✅ Setup complete!"
echo "➡ To start both projects: ./start.sh"
