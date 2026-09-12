import sys
import keyboard

sys.path.append(r"E:\OCR_Project")
import pipeline

running = False


def launch_pipeline():
    global running
    if running:
        print("Пайплайн уже запущен, подождите...")
        return
    running = True
    print("\n>>> Запуск пайплайна...")
    try:
        pipeline.main()
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

    # Прогрев — SwinIR грузится ОДИН РАЗ здесь
    print(">>> Прогрев моделей...")
    pipeline.get_swinir()
    print(">>> Прогрев завершён.")

    keyboard.add_hotkey(41, launch_pipeline)

    print(">>> Готов. Нажмите 'ё' для захвата.")
    try:
        keyboard.wait()
    except KeyboardInterrupt:
        print("\nВыход.")


if __name__ == "__main__":
    main()