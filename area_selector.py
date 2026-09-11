import tkinter as tk
from PIL import Image, ImageTk, ImageGrab


class AreaSelector:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-alpha', 0.3)
        self.root.attributes('-topmost', True)
        self.root.configure(bg='black')
        self.root.config(cursor='crosshair')

        self.canvas = tk.Canvas(
            self.root, cursor='crosshair', bg='black',
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Подсказка
        self.canvas.create_text(
            self.root.winfo_screenwidth() // 2, 30,
            text="Зажмите ЛКМ и растяните рамку. Esc — отмена.",
            fill='white', font=('Arial', 16)
        )

        self.start_x = None
        self.start_y = None
        self.rect = None
        self.result = None

        self.canvas.bind('<ButtonPress-1>', self.on_press)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)
        self.root.bind('<Escape>', lambda e: self.root.destroy())

        self.root.mainloop()

    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline='red', width=2
        )

    def on_drag(self, event):
        if self.rect:
            self.canvas.coords(
                self.rect,
                self.start_x, self.start_y,
                event.x, event.y
            )

    def on_release(self, event):
        x1 = min(self.start_x, event.x)
        y1 = min(self.start_y, event.y)
        x2 = max(self.start_x, event.x)
        y2 = max(self.start_y, event.y)

        w = x2 - x1
        h = y2 - y1

        if w > 5 and h > 5:
            self.result = (x1, y1, w, h)

        self.root.destroy()

    def get_result(self):
        return self.result


if __name__ == "__main__":
    selector = AreaSelector()
    area = selector.get_result()
    if area:
        x, y, w, h = area
        print(f"Выделенная область: x={x}, y={y}, w={w}, h={h}")

        # Захватываем область
        img = ImageGrab.grab(bbox=(x, y, x + w, y + h))
        img.save(r"E:\capture_raw.png")
        print("Сохранено: E:\\capture_raw.png")
    else:
        print("Область не выделена.")