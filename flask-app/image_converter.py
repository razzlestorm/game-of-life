from PIL import Image
import imghdr

def resize(input_path):
    img = Image.open(input_path)
    if img.size[0] >= 200:
        img = img.resize((200, 200)) 
    else:
        img = img.resize((round(img.size[0], -1), round(img.size[1], -1)))
    img.save(input_path, img.format)

def binarize(input_path):
    img = Image.open(input_path)
    threshold = 127
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