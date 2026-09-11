import sys
import os
from paddleocr import PaddleOCR
import cv2

os.environ['GLOG_minloglevel'] = '2'
os.environ['FLAGS_call_stack_level'] = '0'

OUTPUT_FILE = r"E:\OCR_Project\recognize_output.txt"


def recognize(image_path):
    ocr = PaddleOCR(
        use_textline_orientation=False,
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        lang='ru'
    )
    img = cv2.imread(image_path)
    if img is None:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write("ERROR: image not found")
        return

    result = ocr.predict(img)

    # Собираем фрагменты с координатами
    fragments = []  # (y, x, text)
    for res in result:
        texts = res.get('rec_texts', [])
        boxes = res.get('rec_polys', []) or res.get('dt_polys', [])
        for i, t in enumerate(texts):
            if not t.strip():
                continue
            y = 0
            x = 0
            if i < len(boxes):
                try:
                    y = float(boxes[i][0][1])
                    x = float(boxes[i][0][0])
                except Exception:
                    pass
            fragments.append((y, x, t.strip()))

    if not fragments:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write("")
        return

    # Сортируем по Y, потом по X
    fragments.sort(key=lambda f: (f[0], f[1]))

    # Группируем фрагменты в строки: если разница по Y < порога, считаем одной строкой
    lines = []
    current_line = [fragments[0]]
    for frag in fragments[1:]:
        if abs(frag[0] - current_line[0][0]) < 15:
            current_line.append(frag)
        else:
            current_line.sort(key=lambda f: f[1])
            lines.append(' '.join(t for _, _, t in current_line))
            current_line = [frag]
    current_line.sort(key=lambda f: f[1])
    lines.append(' '.join(t for _, _, t in current_line))

    # Убираем пустые строки
    lines = [l for l in lines if l.strip()]

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write("ERROR: no image path")
        sys.exit(1)
    recognize(sys.argv[1])