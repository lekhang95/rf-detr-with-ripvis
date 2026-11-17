from PIL import Image
import os

folder = r"C:\Users\ASUS\Downloads\rf-detr-with-ripvis\High-resolution"

files = [f for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.tif', '.bmp'))]

if not files:
    print("Không tìm thấy file ảnh nào trong thư mục.")
else:
    print(f"{'File':<50} {'Kích thước (px)':<20} {'DPI':<15} {'Đạt 300 DPI?'}")
    print("-" * 100)
    for fname in sorted(files):
        fpath = os.path.join(folder, fname)
        try:
            img = Image.open(fpath)
            w, h = img.size
            dpi = img.info.get('dpi', None)
            if dpi:
                dpi_x, dpi_y = dpi
                ok = "✅ ĐẠT" if dpi_x >= 300 and dpi_y >= 300 else "❌ CHƯA ĐẠT"
                dpi_str = f"{dpi_x:.0f} x {dpi_y:.0f}"
            else:
                ok = "⚠️  Không có DPI metadata"
                dpi_str = "N/A"
            print(f"{fname:<50} {str(w)+'x'+str(h):<20} {dpi_str:<15} {ok}")
        except Exception as e:
            print(f"{fname:<50} Lỗi: {e}")
