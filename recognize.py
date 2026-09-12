import sys
import json
import os
import tempfile

sys.stdout.reconfigure(encoding='utf-8')

from paddleocr import PaddleOCR


def recognize(image_path: str) -> str:
    ocr = PaddleOCR(
        lang="ru",
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False,
    )

    result = ocr.predict(image_path)

    if not result:
        return ""

    lines = []
    for res in result:
        json_path = tempfile.mktemp(suffix=".json")
        try:
            res.save_to_json(json_path)
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            texts = data.get("rec_texts", [])
            for t in texts:
                lines.append(t)
        finally:
            if os.path.exists(json_path):
                os.remove(json_path)

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python recognize.py <image_path>", file=sys.stderr)
        sys.exit(1)

    image_path = sys.argv[1]
    text = recognize(image_path)
    print(text)


if __name__ == "__main__":
    main()