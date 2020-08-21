from PIL import Image

def binarize(input_img, output_img):
	img = Image.open(f'{input_img}')
	threshold = 200
	# converts pixels to either black or white.
	fn = lambda x : 255 if x > threshold else 0
	r = img.convert('L').point(fn, mode='1')
	r.save(f'{output_img}')
