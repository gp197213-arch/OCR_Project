from paddleocr import PaddleOCR
import cv2

print("Инициализация PaddleOCR...")
ocr = PaddleOCR(use_textline_orientation=True, lang='ru')
print("Модель загружена.")

img = cv2.imread(r"E:\test_input.png")
if img is None:
    print("Картинка не найдена.")
else:
    result = ocr.predict(img)
    print("Результат:")
    for res in result:
        # В PaddleOCR 3.x результат — словарь с ключами 'rec_texts'
        texts = res.get('rec_texts', [])
        for t in texts:
            print(t)