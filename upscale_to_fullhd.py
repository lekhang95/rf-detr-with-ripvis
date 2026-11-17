from PIL import Image
import os
import sys

INPUT_FOLDER  = r"C:\Users\ASUS\Downloads\rf-detr-with-ripvis\High-resolution"
OUTPUT_FOLDER = r"C:\Users\ASUS\Downloads\rf-detr-with-ripvis\High-resolution-300dpi\imgs"
TARGET_DPI = 300
MIN_WIDTH_PX = 1920
MIN_HEIGHT_PX = 1080

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

files = [f for f in os.listdir(INPUT_FOLDER)
         if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.tif', '.bmp'))]

total = len(files)
print(f"Processing {total} files...\n")

for idx, fname in enumerate(sorted(files), 1):
    src = os.path.join(INPUT_FOLDER, fname)
    base = os.path.splitext(fname)[0]
    dst = os.path.join(OUTPUT_FOLDER, base + ".png")

    try:
        img = Image.open(src)
        w, h = img.size
        
        # Calculate scale needed
        scale_w = MIN_WIDTH_PX / w if w < MIN_WIDTH_PX else 1.0
        scale_h = MIN_HEIGHT_PX / h if h < MIN_HEIGHT_PX else 1.0
        scale = max(scale_w, scale_h)
        
        if scale > 1.0:
            new_w = int(w * scale)
            new_h = int(h * scale)
            final_img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
            action = f"Upscaled {int((scale-1)*100)}%"
        else:
            final_img = img
            new_w, new_h = w, h
            action = "Already HD"
        
        # Convert mode if needed
        if final_img.mode == 'RGBA':
            out = final_img
        elif final_img.mode in ('RGB', 'L', 'P'):
            out = final_img.convert('RGB')
        else:
            out = final_img.convert('RGB')

        # Save
        out.save(dst, dpi=(TARGET_DPI, TARGET_DPI), compress_level=6)
        
        print(f"[{idx}/{total}] {fname}")
        print(f"        {w}x{h} -> {new_w}x{new_h} | {action}")
        sys.stdout.flush()

    except Exception as e:
        print(f"[{idx}/{total}] ERROR {fname}: {e}")
        sys.stdout.flush()

print(f"\n{'='*80}")
print(f"DONE! All files saved to:")
print(OUTPUT_FOLDER)
print(f"{'='*80}")
