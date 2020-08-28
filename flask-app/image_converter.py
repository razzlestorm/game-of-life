from PIL import Image
import imghdr

def resize(input_path):
    img = Image.open(input_path)
    if img.size[0] >= 50:
        img = img.resize((50, 50)) 
    else:
        img = img.resize((50, 50))
    img.convert('RGB').save(input_path, 'JPEG')

def binarize(input_path):
    img = Image.open(input_path)
    threshold = 200
    # converts pixels to either black or white.
    fn = lambda x : 255 if x > threshold else 0
    r = img.convert('L').point(fn, mode='1')
    r.save(input_path, img.format)


def validate_image(stream):
    header = stream.read(512)  # 512 bytes should be enough for a header check
    stream.seek(0)  # reset stream pointer
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')