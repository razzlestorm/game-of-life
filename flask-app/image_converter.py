from PIL import Image

def resize(input_path):
    img = Image.open(input_path)
    img = img.resize((round(img.size[0], -1), round(img.size[1], -1)))
    img.save(input_path, img.format)

def binarize(input_path):
    img = Image.open(input_path)
    threshold = 200
    # converts pixels to either black or white.
    fn = lambda x : 255 if x > threshold else 0
    r = img.convert('L').point(fn, mode='1')
    r.save(input_path, img.format)
