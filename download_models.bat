@echo off
chcp 65001 >nul
echo ==================================================
echo  OCR Project - Загрузка моделей
echo ==================================================
echo.

cd /d "%~dp0"

REM === 1. SwinIR (код) ===
if not exist "SwinIR" (
    echo [1/4] Клонирую SwinIR...
    git clone https://github.com/JingyunLiang/SwinIR.git
) else (
    echo [1/4] SwinIR уже есть, пропускаю.
)

REM === 2. Веса SwinIR ===
if not exist "SwinIR\model_zoo\swinir\001_classicalSR_DF2K_s64w8_SwinIR-M_x2.pth" (
    echo [2/4] Скачиваю веса SwinIR...
    mkdir "SwinIR\model_zoo\swinir" 2>nul
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/JingyunLiang/SwinIR/releases/download/v0.0/001_classicalSR_DF2K_s64w8_SwinIR-M_x2.pth' -OutFile 'SwinIR\model_zoo\swinir\001_classicalSR_DF2K_s64w8_SwinIR-M_x2.pth'"
) else (
    echo [2/4] Веса SwinIR уже есть, пропускаю.
)

REM === 3. Saiga Llama 3 8B ===
if not exist "models\model-q4_K.gguf" (
    echo [3/4] Скачиваю Saiga Llama 3 8B (~5 ГБ)...
    mkdir models 2>nul
    set HF_ENDPOINT=https://hf-mirror.com
    hf download IlyaGusev/saiga_llama3_8b_gguf model-q4_K.gguf --local-dir models
) else (
    echo [3/4] Saiga уже есть, пропускаю.
)

REM === 4. ocr_env (venv + PaddleOCR) ===
if not exist "ocr_env" (
    echo [4/4] Создаю ocr_env и ставлю PaddleOCR...
    python -m venv ocr_env
    call ocr_env\Scripts\activate.bat
    pip install --upgrade pip
    pip install -r requirements_ocr.txt
    call deactivate
) else (
    echo [4/4] ocr_env уже есть, пропускаю.
)

echo.
echo ==================================================
echo  Готово! Все модели и окружения установлены.
echo ==================================================
echo.
echo Следующие шаги:
echo   1. Установи llama.cpp: winget install llama.cpp
echo   2. Запусти: start_llama.bat
echo   3. Запусти: python hotkey_runner.py
echo.
pause