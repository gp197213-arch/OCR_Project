# OCR Project — захват экрана + SwinIR + PaddleOCR + Saiga

Автоматическое распознавание текста с выделенной области экрана с коррекцией через нейросеть.

## Как работает

ё → рамка → SwinIR x2 → PaddleOCR → Saiga Llama 3 8B → буфер

## Возможности

- Горячая клавиша ё
- SwinIR x2 — апскейл
- PaddleOCR 3.x — русский + английский
- Saiga Llama 3 8B — коррекция
- Кэш моделей

## Требования

- Windows 10/11
- Python 3.12+
- NVIDIA GPU
- ~15 ГБ места

## Установка

См. INSTALL.md.

## Запуск

Окно 1:

.\start_llama.bat

Окно 2:

python hotkey_runner.py

## Не в репозитории

- models/
- ocr_env/
- SwinIR/
- *.gguf, *.pth
- capture_*.png
