import sys
import os
import subprocess
import tkinter as tk
from tkinter import font as tkfont
from PIL import ImageGrab
import cv2
import numpy as np
import torch
import pyperclip

sys.path.append(r"E:\OCR_Project\SwinIR")
from models.network_swinir import SwinIR as net

# Пути
RAW_PATH = r"E:\OCR_Project\capture_raw.png"
UPSCALED_PATH = r"E:\OCR_Project\capture_upscaled.png"
OCR_PYTHON = r"E:\OCR_Project\ocr_env\Scripts\python.exe"
RECOGNIZE_SCRIPT = r"E:\OCR_Project\recognize.py"
OUTPUT_FILE = r"E:\OCR_Project\recognize_output.txt"
SWINIR_MODEL = r"E:\OCR_Project\SwinIR\model_zoo\swinir\001_classicalSR_DF2K_s64w8_SwinIR-M_x2.pth"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


# ============ 1. Выделение области ============
class AreaSelector:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-alpha', 0.3)
        self.root.attributes('-topmost', True)
        self.root.configure(bg='black')
        self.canvas = tk.Canvas(self.root, cursor='crosshair', bg='black', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.create_text(
            self.root.winfo_screenwidth() // 2, 30,
            text="Зажмите ЛКМ и растяните рамку. Esc — отмена.",
            fill='white', font=('Arial', 16)
        )
        self.start_x = self.start_y = self.rect = self.result = None
        self.canvas.bind('<ButtonPress-1>', self.on_press)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)
        self.root.bind('<Escape>', lambda e: self.root.destroy())
        self.root.mainloop()

    def on_press(self, event):
        self.start_x, self.start_y = event.x, event.y
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline='red', width=2
        )

    def on_drag(self, event):
        if self.rect:
            self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_release(self, event):
        x1, y1 = min(self.start_x, event.x), min(self.start_y, event.y)
        x2, y2 = max(self.start_x, event.x), max(self.start_y, event.y)
        if x2 - x1 > 5 and y2 - y1 > 5:
            self.result = (x1, y1, x2 - x1, y2 - y1)
        self.root.destroy()

    def get_result(self):
        return self.result


# ============ 2. SwinIR ============
def load_swinir():
    model = net(
        upscale=2, in_chans=3, img_size=64, window_size=8, img_range=1.,
        depths=[6, 6, 6, 6, 6, 6], embed_dim=180,
        num_heads=[6, 6, 6, 6, 6, 6], mlp_ratio=2,
        upsampler='pixelshuffle', resi_connection='1conv'
    )
    sd = torch.load(SWINIR_MODEL, map_location="cpu", weights_only=True)['params']
    model.load_state_dict(sd, strict=True)
    model.eval().to(DEVICE)
    return model


def upscale(model, image_bgr):
    img = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
    img = torch.from_numpy(img).permute(2, 0, 1).unsqueeze(0).to(DEVICE)
    with torch.no_grad():
        out = model(img)
    out = out.squeeze(0).permute(1, 2, 0).cpu().numpy()
    out = (out * 255.0).clip(0, 255).astype(np.uint8)
    return cv2.cvtColor(out, cv2.COLOR_RGB2BGR)


# ============ 3. OCR через subprocess ============
def run_ocr(image_path):
    result = subprocess.run(
        [OCR_PYTHON, RECOGNIZE_SCRIPT, image_path],
        capture_output=True, text=True, encoding='utf-8', errors='replace'
    )
    if result.returncode != 0:
        print("OCR error:")
        print(result.stderr)
        return ""
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            return f.read().strip()
    return ""


# ============ 4. Окно выбора текста (полный экран) ============
class TextChooser:
    def __init__(self, text):
        self.selected = None
        self.root = tk.Tk()
        self.root.title("Выберите текст")
        self.root.attributes('-topmost', True)
        self.root.attributes('-fullscreen', True)

        big_font = tkfont.Font(family="Consolas", size=14)

        # Блок кнопок — прилипает к низу
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill=tk.X, padx=10, pady=10, side=tk.BOTTOM)

        tk.Button(
            btn_frame, text="Копировать выделенное", font=("Arial", 12),
            command=self.copy_selected, bg='#4a90d9', fg='white', padx=20, pady=5
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame, text="Копировать всё", font=("Arial", 12),
            command=self.copy_all, padx=20, pady=5
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame, text="Отмена", font=("Arial", 12),
            command=self.root.destroy, padx=20, pady=5
        ).pack(side=tk.RIGHT, padx=5)

        # Подсказка — сверху
        tk.Label(
            self.root,
            text="Выделите фрагмент и нажмите «Копировать выделенное», или «Копировать всё»",
            font=("Arial", 12), pady=8
        ).pack(side=tk.TOP)

        # Текстовое поле — занимает оставшееся место
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_widget = tk.Text(
            frame, wrap=tk.WORD, font=big_font,
            yscrollcommand=scrollbar.set,
            selectbackground='#4a90d9', selectforeground='white'
        )
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.text_widget.yview)

        self.text_widget.insert('1.0', text)
        self.text_widget.focus_set()

        # Горячие клавиши
        self.root.bind('<Control-c>', lambda e: self.copy_selected())
        self.root.bind('<Control-Shift-C>', lambda e: self.copy_all())
        self.root.bind('<Escape>', lambda e: self.root.destroy())

        self.root.mainloop()

    def copy_selected(self):
        try:
            selected = self.text_widget.get(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            selected = ""
        if selected:
            self.selected = selected
            self.root.destroy()
        else:
            self.copy_all()

    def copy_all(self):
        self.selected = self.text_widget.get('1.0', tk.END).strip()
        self.root.destroy()

    def get_selected(self):
        return self.selected


# ============ 5. Main ============
def main():
    print("1. Выделите область...")
    selector = AreaSelector()
    area = selector.get_result()
    if not area:
        print("Отменено.")
        return

    x, y, w, h = area
    print(f"Область: {w}x{h}")

    img = ImageGrab.grab(bbox=(x, y, x + w, y + h))
    img.save(RAW_PATH)
    print(f"Сохранено: {RAW_PATH}")

    print("2. Апскейл SwinIR x2...")
    model = load_swinir()
    raw_bgr = cv2.imread(RAW_PATH)
    upscaled = upscale(model, raw_bgr)
    cv2.imwrite(UPSCALED_PATH, upscaled)
    print(f"Сохранено: {UPSCALED_PATH} ({upscaled.shape[1]}x{upscaled.shape[0]})")

    print("3. Распознавание...")
    text = run_ocr(UPSCALED_PATH)
    if not text:
        print("Текст не распознан.")
        return

    print(f"Распознано символов: {len(text)}")
    print("4. Просмотр текста...")

    chooser = TextChooser(text)
    selected = chooser.get_selected()

    if selected:
        pyperclip.copy(selected)
        print(f"\n=== Скопировано в буфер обмена ===")
        print(selected[:200])
        print("===================================")
    else:
        print("Отменено.")


if __name__ == "__main__":
    main()