# Установка OCR Project

Пошаговая инструкция для восстановления проекта на новом ПК.

## Требования

- Windows 10/11
- Python 3.12+
- Git
- NVIDIA GPU (рекомендуется) с CUDA 12.6+
- ~15 ГБ свободного места

## Шаг 1. Клонировать репозиторий

git clone https://github.com/gp197213-arch/OCR_Project.git E:\OCR_Project
cd E:\OCR_Project

## Шаг 2. Установить llama.cpp

winget install llama.cpp

Перезапусти PowerShell.

## Шаг 3. Установить зависимости

pip install -r requirements.txt

## Шаг 4. Скачать модели

.\download_models.bat

## Шаг 5. Запуск

Окно 1:

.\start_llama.bat

Окно 2:

python hotkey_runner.py
