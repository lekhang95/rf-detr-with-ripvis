from PIL import Image
import os

INPUT_FOLDER  = r"C:\Users\ASUS\Downloads\rf-detr-with-ripvis\High-resolution"
OUTPUT_FOLDER = r"C:\Users\ASUS\Downloads\rf-detr-with-ripvis\High-resolution-300dpi"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

files = [f for f in os.listdir(INPUT_FOLDER)
         if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.tif', '.bmp'))]

print(f"{'File':<50} {'Kích thước (px)':<20} {'DPI cũ':<15} {'DPI mới':<10} {'Kết quả'}")
print("-" * 110)

for fname in sorted(files):
    src = os.path.join(INPUT_FOLDER, fname)
    # Luôn lưu ra PNG để đảm bảo chất lượng không mất
    base = os.path.splitext(fname)[0]
    dst = os.path.join(OUTPUT_FOLDER, base + ".png")

    try:
        img = Image.open(src)
        w, h = img.size
        old_dpi = img.info.get('dpi', 'N/A')

        # Chuyển sang RGB nếu cần (tránh lỗi khi save PNG với mode lạ)
        if img.mode in ('RGBA', 'RGB', 'L'):
            out = img
        else:
            out = img.convert('RGB')

        # Lưu với DPI = 300
        out.save(dst, dpi=(300, 300))

        print(f"{fname:<50} {str(w)+'x'+str(h):<20} {str(old_dpi):<15} {'300x300':<10} ✅ Đã lưu: {os.path.basename(dst)}")

    except Exception as e:
        print(f"{fname:<50} ❌ Lỗi: {e}")

print("\n✅ Hoàn tất! File đã được lưu tại:", OUTPUT_FOLDER)

# Xác nhận lại DPI của file output
print("\n--- Kiểm tra lại DPI file output ---")
for fname in sorted(os.listdir(OUTPUT_FOLDER)):
    if fname.lower().endswith('.png'):
        fpath = os.path.join(OUTPUT_FOLDER, fname)
        img = Image.open(fpath)
        dpi = img.info.get('dpi', 'N/A')
        w, h = img.size
        ok = "✅ ĐẠT" if dpi != 'N/A' and dpi[0] >= 299 else "❌"
        print(f"  {fname:<50} {str(w)+'x'+str(h):<20} DPI: {str(dpi):<15} {ok}")
