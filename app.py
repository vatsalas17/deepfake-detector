from flask import Flask, render_template, request
import piexif
import os

app = Flask(__name__)

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_metadata(image_path):
    try:
        exif_dict = piexif.load(image_path)
    except Exception:
        return None

    metadata = {}
    for ifd_name in exif_dict:
        if exif_dict[ifd_name] is not None:
            metadata[ifd_name] = {}
            for tag in exif_dict[ifd_name]:
                try:
                    tag_name = piexif.TAGS[ifd_name][tag]["name"]
                except KeyError:
                    tag_name = str(tag)
                value = exif_dict[ifd_name][tag]
                # Decode bytes to string if possible
                if isinstance(value, bytes):
                    try:
                        value = value.decode(errors='ignore')
                    except Exception:
                        pass
                metadata[ifd_name][tag_name] = value
    return metadata

def is_fake(metadata):
    """
    Simple fake detection logic:
    If metadata is missing or very sparse, consider FAKE.
    Otherwise, REAL.
    (You can improve this logic based on your needs)
    """
    if not metadata:
        return True
    # Example: if '0th' IFD has no Software tag, flag as fake (just a sample rule)
    if '0th' not in metadata or 'Software' not in metadata['0th']:
        return True
    # You can add more sophisticated checks here
    return False

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    metadata = None

    if request.method == 'POST':
        if 'image' not in request.files:
            result = "No file part"
        else:
            file = request.files['image']
            if file.filename == '':
                result = "No selected file"
            elif file and allowed_file(file.filename):
                filename = file.filename
                # Save uploaded file temporarily
                temp_path = os.path.join("temp_upload.jpg")
                file.save(temp_path)

                metadata = extract_metadata(temp_path)
                if is_fake(metadata):
                    result = "FAKE"
                else:
                    result = "REAL"

                # Delete temp file after processing
                os.remove(temp_path)
            else:
                result = "Invalid file type. Allowed: png, jpg, jpeg, gif."

    return render_template('index.html', result=result, metadata=metadata)


if __name__ == '__main__':
    app.run(debug=True)
