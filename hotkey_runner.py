import sys
import os
import subprocess
import keyboard

PIPELINE = r"E:\OCR_Project\pipeline.py"
PYTHON = sys.executable

running = False


def launch_pipeline():
    global running
    if running:
        print("Пайплайн уже запущен, подождите...")
        return
    running = True
    print("\n>>> Запуск пайплайна...")
    try:
        subprocess.run([PYTHON, PIPELINE], check=False)
    except Exception as e:
        print(f"Ошибка запуска: {e}")
    finally:
        running = False
        print(">>> Готов. Нажмите 'ё' для нового захвата.")


def main():
    print("=" * 50)
    print("Горячая клавиша: 'ё' (скан-код 41, любая раскладка)")
    print("Выход: Ctrl+C в этом окне")
    print("=" * 50)

    # Скан-код 41 — физическая клавиша 'ё' / '`' / '~'
    keyboard.add_hotkey(41, launch_pipeline)

    print(">>> Готов. Нажмите 'ё' для захвата.")
    try:
        keyboard.wait()
    except KeyboardInterrupt:
        print("\nВыход.")


if __name__ == "__main__":
    main()