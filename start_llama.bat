@echo off
chcp 65001 >nul
cd /d E:\OCR_Project\models
llama-server.exe -m model-q4_K.gguf --host 127.0.0.1 --port 8080 -c 4096 -ngl 99
pause