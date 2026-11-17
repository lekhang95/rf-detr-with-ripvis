from PIL import Image
import os

OUTPUT_FOLDER = r"C:\Users\ASUS\Downloads\rf-detr-with-ripvis\High-resolution-300dpi\imgs"
TARGET_DPI = 300
MIN_WIDTH_PX = 1920
MIN_HEIGHT_PX = 1080

print("="*100)
print("VERIFY OUTPUT IMAGES FOR JOURNAL SUBMISSION")
print("="*100)
print(f"\n{'File':<60} {'Size (px)':<18} {'DPI':<12} {'Width (cm)':<12} {'Status'}")
print("-"*100)

files = sorted([f for f in os.listdir(OUTPUT_FOLDER) if f.lower().endswith('.png')])
all_ok = True
count_ok = 0
count_fail = 0

for fname in files:
    fpath = os.path.join(OUTPUT_FOLDER, fname)
    try:
        img = Image.open(fpath)
        w, h = img.size
        dpi = img.info.get('dpi', (0, 0))
        width_cm = (w / TARGET_DPI) * 2.54
        
        dpi_ok = dpi[0] >= 299 if dpi != (0, 0) else False
        size_ok = w >= MIN_WIDTH_PX and h >= MIN_HEIGHT_PX
        
        if dpi_ok and size_ok:
            status = "OK PASS"
            count_ok += 1
        else:
            status = "FAIL"
            count_fail += 1
            all_ok = False
            
        dpi_str = f"{int(dpi[0])}" if dpi != (0, 0) else "N/A"
        
        print(f"{fname:<60} {str(w)+'x'+str(h):<18} {dpi_str:<12} {width_cm:<12.1f} {status}")
        
    except Exception as e:
        print(f"{fname:<60} ERROR: {e}")
        count_fail += 1
        all_ok = False

print("\n" + "="*100)
print(f"\nSUMMARY:")
print(f"   OK:    {count_ok}/{len(files)} images")
print(f"   FAIL:  {count_fail}/{len(files)} images")

if all_ok:
    print(f"\n{'='*100}")
    print("SUCCESS: ALL IMAGES MEET JOURNAL REQUIREMENTS!")
    print(f"{'='*100}")
    print("\n+ DPI = 300")
    print(f"+ Resolution >= 1920x1080 (Full HD)")
    print(f"+ Width @ 300 DPI = ~16.3cm (excellent for print)")
    print("\nREADY TO SUBMIT - HIGH QUALITY!")
else:
    print(f"\n{'='*100}")
    print("WARNING: SOME IMAGES DO NOT MEET REQUIREMENTS")
    print(f"{'='*100}")

print(f"\nOutput folder: {OUTPUT_FOLDER}")
