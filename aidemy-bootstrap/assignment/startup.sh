#!/bin/bash
apt-get update
apt-get install -y curl
curl -fsSL https://ollama.ai/install.sh | sh
sed -i 's/ExecStart=\/usr\/local\/bin\/ollama serve/Environment="OLLAMA_HOST=0.0.0.0:11434"\n&/' /etc/systemd/system/ollama.service
sudo systemctl daemon-reload
sudo systemctl enable ollama
sudo systemctl start ollama.service
ollama pull deepseek-r1:1.5b
