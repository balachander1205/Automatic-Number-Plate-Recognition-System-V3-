# import pyqrcode
# qr = pyqrcode.create("HORN O.K. PLEASE.")
# result = qr.png('E:/MY-PROJECTS/pythonRest-ANPR/static/NumberPlates/2018-03-07/qrcodes/8936fb12-b7cb-438e-9db1-5d65e5b554f0_qrcode.png', scale=6)
# print(qr.data)

import sys, qrcode

d = qrcode.Decoder()
if d.decode('E:/MY-PROJECTS/pythonRest-ANPR/static/NumberPlates/2018-03-07/qrcodes/8936fb12-b7cb-438e-9db1-5d65e5b554f0_qrcode.png'):
	print('result: ' + d.result)
else:
	print('error: ' + d.error)