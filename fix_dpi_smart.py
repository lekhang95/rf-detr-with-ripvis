from PIL import Image
import os

INPUT_FOLDER  = r"C:\Users\ASUS\Downloads\rf-detr-with-ripvis\High-resolution"
OUTPUT_FOLDER = r"C:\Users\ASUS\Downloads\rf-detr-with-ripvis\High-resolution-300dpi\imgs"
TARGET_DPI = 300

# Yêu cầu tối thiểu: Full HD 1920x1080
MIN_WIDTH_PX = 1920
MIN_HEIGHT_PX = 1080

# Cho phép upscale lớn để đạt Full HD
MAX_UPSCALE_PERCENT = 200  # Cho phép upscale thoải mái

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

files = [f for f in os.listdir(INPUT_FOLDER)
         if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.tif', '.bmp'))]

print(f"{'File':<55} {'Original (px)':<15} {'Output (px)':<15} {'Width (cm)':<12} {'Action'}")
print("-" * 130)

stats = {'upscaled': 0, 'ok': 0, 'need_recreate': 0}

for fname in sorted(files):
    src = os.path.join(INPUT_FOLDER, fname)
    base = os.path.splitext(fname)[0]
    dst = os.path.join(OUTPUT_FOLDER, base + ".png")

    try:
        img = Image.open(src)
        w, h = img.size
        old_dpi = img.info.get('dpi', (72, 72))
        
        # Tính kích thước in ban đầu
        width_cm_original = (w / TARGET_DPI) * 2.54
        
        # Quyết định có cần upscale không
        final_img = img
        action = ""
        
        # Tính tỷ lệ cần để đạt Full HD
        scale_w = MIN_WIDTH_PX / w if w < MIN_WIDTH_PX else 1.0
        scale_h = MIN_HEIGHT_PX / h if h < MIN_HEIGHT_PX else 1.0
        scale_needed = max(scale_w, scale_h)  # Lấy tỷ lệ lớn hơn để đảm bảo cả 2 chiều đạt
        
        if scale_needed > 1.0:
            # CẦN UPSCALE
            new_w = int(w * scale_needed)
            new_h = int(h * scale_needed)
            scale_percent = (scale_needed - 1) * 100
            
            if scale_percent <= MAX_UPSCALE_PERCENT:
                # Upscale với LANCZOS
                final_img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                action = f"OK Upscale {scale_percent:.1f}% -> Full HD+"
                stats['upscaled'] += 1
            else:
                # Quá cao nhưng vẫn upscale (theo yêu cầu "cho chắc")
                final_img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                action = f"WARN Upscale {scale_percent:.1f}% (may reduce quality)"
                stats['need_recreate'] += 1
        else:
            # ĐỦ độ phân giải
            action = "OK Full HD+"
            stats['ok'] += 1
        
        # Lấy kích thước cuối cùng
        final_w, final_h = final_img.size
        width_cm_final = (final_w / TARGET_DPI) * 2.54
        
        # Giữ mode phù hợp
        if final_img.mode == 'RGBA':
            out = final_img
        elif final_img.mode in ('RGB', 'L', 'P'):
            out = final_img.convert('RGB')
        else:
            out = final_img.convert('RGB')

        # Lưu với DPI = 300
        out.save(dst, dpi=(TARGET_DPI, TARGET_DPI), compress_level=6)

        print(f"{fname:<55} {str(w)+'x'+str(h):<15} {str(final_w)+'x'+str(final_h):<15} {width_cm_final:>5.1f}cm     {action}")

    except Exception as e:
        print(f"{fname:<55} ERROR: {e}")

print("\n" + "="*130)
print(f"\nSTATISTICS:")
print(f"   OK Already Full HD:    {stats['ok']} images")
print(f"   OK Upscaled:           {stats['upscaled']} images")
print(f"   WARN Large upscale:    {stats['need_recreate']} images (may reduce quality)")
print(f"\nCompleted! Files saved to: {OUTPUT_FOLDER}")

# Kiểm tra lại output
print("\n" + "="*130)
print("--- VERIFY OUTPUT FILES ---\n")
output_files = [f for f in os.listdir(OUTPUT_FOLDER) if f.lower().endswith('.png')]
all_ok = True

for fname in sorted(output_files):
    fpath = os.path.join(OUTPUT_FOLDER, fname)
    img = Image.open(fpath)
    dpi = img.info.get('dpi', 'N/A')
    w, h = img.size
    width_cm = (w / TARGET_DPI) * 2.54
    
    dpi_ok = dpi != 'N/A' and dpi[0] >= 299
    size_ok = w >= MIN_WIDTH_PX and h >= MIN_HEIGHT_PX
    ok = "OK" if (dpi_ok and size_ok) else "FAIL"
    
    if ok == "FAIL":
        all_ok = False
    
    print(f"  {fname:<55} {str(w)+'x'+str(h):<15} DPI: {str(dpi):<15} {width_cm:>5.1f}cm  {ok}")

print("\n" + "="*130)
if all_ok:
    print("SUCCESS: All images meet requirements: DPI=300 and Resolution >= 1920x1080 (Full HD)")
    print("\nREADY TO SUBMIT - HIGH QUALITY!")
else:
    print("WARNING: Some images do not meet requirements!")

print("\nNOTES:")
print("   * All images upscaled to minimum Full HD (1920x1080)")
print("   * Upscale <100%: good quality with LANCZOS resampling")
print("   * Upscale >100%: may be slightly blurry but acceptable for journals")
print("   * DPI = 300 @ Full HD = ~16.3cm width (excellent for print)")
