from PIL import Image
import os

INPUT_FOLDER  = r"C:\Users\ASUS\Downloads\rf-detr-with-ripvis\High-resolution"
OUTPUT_FOLDER = r"C:\Users\ASUS\Downloads\rf-detr-with-ripvis\High-resolution-300dpi"
TARGET_DPI = 300

# Yêu cầu tối thiểu của nhiều journals: width >= 8.5 cm (~1000px @ 300dpi)
MIN_WIDTH_CM = 8.5
MIN_WIDTH_PX = int(MIN_WIDTH_CM * TARGET_DPI / 2.54)  # ~1004 px

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

files = [f for f in os.listdir(INPUT_FOLDER)
         if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.tif', '.bmp'))]

print(f"{'File':<50} {'Kích thước (px)':<20} {'DPI cũ':<15} {'Kích thước in (cm)':<20} {'Cảnh báo'}")
print("-" * 130)

warnings = []

for fname in sorted(files):
    src = os.path.join(INPUT_FOLDER, fname)
    base = os.path.splitext(fname)[0]
    dst = os.path.join(OUTPUT_FOLDER, base + ".png")

    try:
        img = Image.open(src)
        w, h = img.size
        old_dpi = img.info.get('dpi', (72, 72))  # Default 72 nếu không có

        # Tính kích thước in thực tế với DPI 300
        width_cm = (w / TARGET_DPI) * 2.54
        height_cm = (h / TARGET_DPI) * 2.54
        size_cm = f"{width_cm:.1f}x{height_cm:.1f}"

        # Cảnh báo nếu độ phân giải thấp
        warning = ""
        if w < MIN_WIDTH_PX:
            warning = f"⚠️ Độ phân giải thấp ({width_cm:.1f}cm < {MIN_WIDTH_CM}cm)"
            warnings.append((fname, w, h, width_cm))

        # Giữ nguyên mode ảnh nếu có thể, ưu tiên RGBA/RGB
        if img.mode == 'RGBA':
            out = img
        elif img.mode in ('RGB', 'L', 'P'):
            out = img.convert('RGB')
        else:
            out = img.convert('RGB')

        # Lưu với DPI = 300, compression tối ưu cho PNG
        out.save(dst, dpi=(TARGET_DPI, TARGET_DPI), compress_level=6)

        print(f"{fname:<50} {str(w)+'x'+str(h):<20} {str(old_dpi):<15} {size_cm:<20} {warning or '✅'}")

    except Exception as e:
        print(f"{fname:<50} ❌ Lỗi: {e}")
        warnings.append((fname, 0, 0, 0))

print("\n" + "="*130)
print(f"✅ Hoàn tất! {len(files)} file đã được lưu tại: {OUTPUT_FOLDER}")

# Hiển thị cảnh báo tổng hợp
if warnings:
    print(f"\n⚠️ CÓ {len(warnings)} ẢNH CẦN LƯU Ý:")
    print("\nCác ảnh có độ phân giải thấp khi in với DPI 300:")
    for fname, w, h, width_cm in warnings:
        if w > 0:  # Không phải lỗi
            print(f"  • {fname}: {w}x{h}px → {width_cm:.1f}cm rộng")
            print(f"    💡 Đề xuất: Tạo lại ảnh với độ phân giải cao hơn (tối thiểu {MIN_WIDTH_PX}x{int(h*MIN_WIDTH_PX/w)}px)")

    print("\n📌 GHI CHÚ:")
    print("  - Nhiều journals yêu cầu ảnh rộng tối thiểu 8.5-17cm khi in")
    print("  - Chỉ thay đổi DPI KHÔNG tăng chất lượng ảnh")
    print("  - Nên tạo lại ảnh từ vector/source gốc với resolution cao hơn")
else:
    print("\n✅ TẤT CẢ ảnh đạt yêu cầu độ phân giải tối thiểu!")

# Xác nhận lại DPI của file output
print("\n--- KIỂM TRA LẠI FILE OUTPUT ---")
output_files = [f for f in os.listdir(OUTPUT_FOLDER) if f.lower().endswith('.png')]
all_ok = True
for fname in sorted(output_files):
    fpath = os.path.join(OUTPUT_FOLDER, fname)
    img = Image.open(fpath)
    dpi = img.info.get('dpi', 'N/A')
    w, h = img.size
    width_cm = (w / TARGET_DPI) * 2.54

    ok = "✅" if dpi != 'N/A' and dpi[0] >= 299 else "❌"
    if ok == "❌":
        all_ok = False

    print(f"  {fname:<50} {str(w)+'x'+str(h):<20} DPI: {str(dpi):<15} {width_cm:.1f}cm {ok}")

if all_ok:
    print("\n✅ Tất cả file output có DPI = 300")
else:
    print("\n❌ Có file không đạt DPI yêu cầu!")
