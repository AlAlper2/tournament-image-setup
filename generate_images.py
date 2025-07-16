import os
from tkinter import Tk, filedialog
from PIL import Image

def convert_png_to_jpg(path, output_size=None):
    img = Image.open(path).convert("RGB")
    if output_size:
        img = img.resize(output_size, Image.LANCZOS)
    jpg_path = os.path.splitext(path)[0] + ".jpg"
    img.save(jpg_path, "JPEG")
    return jpg_path

def create_triptych(jpg_paths, output_path, final_height=240):
    images = [Image.open(p) for p in jpg_paths]
    widths, heights = zip(*(i.size for i in images))
    total_width = sum(widths)
    max_height = max(heights)

    triptych = Image.new('RGB', (total_width, max_height), color=(255, 255, 255))

    x_offset = 0
    for img in images:
        triptych.paste(img, (x_offset, 0))
        x_offset += img.width

    triptych.save(output_path)

    # Resize to final height
    aspect_ratio = triptych.width / triptych.height
    new_width = int(final_height * aspect_ratio)
    triptych_resized = triptych.resize((new_width, final_height), Image.LANCZOS)
    small_output_path = os.path.splitext(output_path)[0] + "_small.jpg"
    triptych_resized.save(small_output_path, "JPEG")

def main():
    # GUI folder picker
    root = Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title="Select Folder with Tournament Images")
    if not folder:
        print("No folder selected.")
        return

    print(f"📂 Processing folder: {folder}")

    # Step 1: Convert 1st/2nd/3rd to JPG (640x640)
    jpgs = []
    for name in ["1st.png", "2nd.png", "3rd.png"]:
        input_path = os.path.join(folder, name)
        if os.path.exists(input_path):
            jpg_path = convert_png_to_jpg(input_path, output_size=(640, 640))
            jpgs.append(jpg_path)
            print(f"✅ Converted {name} → {os.path.basename(jpg_path)}")
        else:
            print(f"❌ Missing: {name}")

    # Step 2: Create awards.jpg and awards_small.jpg
    if len(jpgs) == 3:
        awards_path = os.path.join(folder, "awards.jpg")
        create_triptych(jpgs, awards_path)
        print("🏆 Created awards.jpg and awards_small.jpg")
    else:
        print("⚠️ Cannot create awards triptych: missing JPGs.")

    # Step 3: Convert promo.png → promo.jpg (no resize)
    promo_path = os.path.join(folder, "promo.png")
    if os.path.exists(promo_path):
        promo_jpg = convert_png_to_jpg(promo_path)  # No resize
        print(f"✅ Converted promo.png → {os.path.basename(promo_jpg)}")
    else:
        print("❌ promo.png not found.")

if __name__ == "__main__":
    main()
