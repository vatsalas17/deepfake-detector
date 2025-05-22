from PIL import Image
import piexif

def print_exif_metadata(image_path):
    try:
        img = Image.open(image_path)
        print(f"Metadata for {image_path}:")

        # Try to get EXIF data via piexif
        exif_dict = piexif.load(img.info.get("exif", b""))
        if not exif_dict:
            print("No EXIF metadata found.")
            return

        # piexif separates EXIF into several IFDs
        for ifd_name in exif_dict:
            if ifd_name == "thumbnail":
                continue  # skip thumbnails

            print(f"\n{ifd_name} IFD:")
            for tag, value in exif_dict[ifd_name].items():
                tag_name = piexif.TAGS[ifd_name].get(tag, {"name": f"Unknown Tag {tag}"})["name"]
                # Decode bytes if possible (like ASCII or UTF-8 strings)
                if isinstance(value, bytes):
                    try:
                        value = value.decode('utf-8')
                    except Exception:
                        # If decoding fails, show raw bytes or hex
                        value = value.hex()
                print(f"  {tag_name}: {value}")

        # Also print info dictionary from PIL (often contains some metadata)
        if img.info:
            print("\nAdditional PIL info dictionary metadata:")
            for k, v in img.info.items():
                print(f"  {k}: {v}")

    except Exception as e:
        print(f"Error reading metadata: {e}")

# Example usage
image_path = r"D:/Deepfake Detector/sample.jpg"
print_exif_metadata(image_path)
