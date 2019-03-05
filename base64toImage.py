import base64
from PIL import Image
import cv2
# from StringIO import StringIO
import numpy as np
from io import BytesIO

def base64toImage(base64_string):
	if "data:image" in str(base64_string):
		print("It is base64_string ")
	base64Str = base64_string.split(",")
	base64_string = base64Str[1]
	if len(base64_string) % 4:
		# not a multiple of 4, add padding:
		base64_string += '=' * (4 - len(base64_string) % 4)	
	sbuf = BytesIO()
	sbuf.write(base64.b64decode(base64_string))
	pimg = Image.open(sbuf)
	return cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)

def base64_str_to_image(base64_string):
	try:
		print("Base 64 to image file")				
	except Exception as e:
		print("{ Xception in base64_str_to_image() } ",str(e))
