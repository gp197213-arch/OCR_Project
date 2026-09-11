import torch
import cv2
import numpy as np
import sys
import os

sys.path.append(r"E:\OCR_Project\SwinIR")
from models.network_swinir import SwinIR as net

MODEL_PATH = r"E:\OCR_Project\SwinIR\model_zoo\swinir\001_classicalSR_DF2K_s64w8_SwinIR-M_x4.pth"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


def load_swinir_model():
    model = net(
        upscale=4,
        in_chans=3,
        img_size=64,
        window_size=8,
        img_range=1.,
        depths=[6, 6, 6, 6, 6, 6],
        embed_dim=180,
        num_heads=[6, 6, 6, 6, 6, 6],
        mlp_ratio=2,
        upsampler='pixelshuffle',
        resi_connection='1conv'
    )
    sd = torch.load(MODEL_PATH, map_location="cpu", weights_only=True)['params']
    model.load_state_dict(sd, strict=True)
    model.eval()
    model = model.to(DEVICE)
    return model


def upscale_image(model, image_bgr):
    img = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
    img = torch.from_numpy(img).permute(2, 0, 1).unsqueeze(0).to(DEVICE)
    with torch.no_grad():
        output = model(img)
    output = output.squeeze(0).permute(1, 2, 0).cpu().numpy()
    output = (output * 255.0).clip(0, 255).astype(np.uint8)
    return cv2.cvtColor(output, cv2.COLOR_RGB2BGR)


if __name__ == "__main__":
    test_img_path = r"E:\OCR_Project\test_input.png"
    if not os.path.exists(test_img_path):
        print(f"Файл {test_img_path} не найден.")
        sys.exit(1)

    print("Загрузка модели SwinIR-M...")
    model = load_swinir_model()
    print("Модель загружена.")

    img = cv2.imread(test_img_path)
    print(f"Вход: {img.shape}")

    result = upscale_image(model, img)
    print(f"Выход: {result.shape}")

    out_path = r"E:\OCR_Project\test_output_swinir.png"
    cv2.imwrite(out_path, result)
    print(f"Результат сохранён: {out_path}")