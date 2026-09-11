import sys
import os
from paddleocr import PaddleOCR
import cv2

os.environ['GLOG_minloglevel'] = '2'
os.environ['FLAGS_call_stack_level'] = '0'

OUTPUT_FILE = r"E:\OCR_Project\recognize_output.txt"


def recognize(image_path):
    ocr = PaddleOCR(
        use_textline_orientation=True,
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

    # Собираем фрагменты: (y_top, y_bottom, x_left, text)
    fragments = []
    for res in result:
        texts = res.get('rec_texts', [])
        boxes = res.get('rec_polys', []) or res.get('dt_polys', [])
        for i, t in enumerate(texts):
            if i >= len(boxes):
                continue
            box = boxes[i]
            try:
                xs = [float(p[0]) for p in box]
                ys = [float(p[1]) for p in box]
                fragments.append((
                    min(ys),      # y_top
                    max(ys),      # y_bottom
                    min(xs),      # x_left
                    t
                ))
            except Exception:
                fragments.append((0, 0, 0, t))

    if not fragments:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write("")
        return

    # Сортируем по Y (сверху вниз), затем по X (слева направо)
    fragments.sort(key=lambda x: (x[0], x[2]))

    # Группируем по строкам: если вертикальные диапазоны перекрываются — одна строка
    lines = []
    current_line = [fragments[0]]

    for frag in fragments[1:]:
        # Проверяем перекрытие с текущей строкой
        line_top = min(f[0] for f in current_line)
        line_bottom = max(f[1] for f in current_line)

        # Перекрытие: frag.y_top < line_bottom AND frag.y_bottom > line_top
        overlap = frag[0] < line_bottom and frag[1] > line_top

        # Дополнительно: если frag начинается выше конца строки на небольшую величину
        # (для слов с разным размером шрифта)
        near = abs(frag[0] - line_top) < (line_bottom - line_top) * 0.5

        if overlap or near:
            current_line.append(frag)
        else:
            current_line.sort(key=lambda x: x[2])
            lines.append(' '.join(f[3] for f in current_line))
            current_line = [frag]

    if current_line:
        current_line.sort(key=lambda x: x[2])
        lines.append(' '.join(f[3] for f in current_line))

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write("ERROR: no image path")
        sys.exit(1)
    recognize(sys.argv[1])