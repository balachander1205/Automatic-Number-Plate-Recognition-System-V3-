# import sys, qrcode
# from PIL import Image

# qr = qrcode.QRCode(
#     version=1,
#     error_correction=qrcode.constants.ERROR_CORRECT_L,
#     box_size=10,
#     border=4,
# )
# qr.add_data('Hello Balu')
# qr.make(fit=True)

# img = qr.make_image()
# file_name = 'testQR'
# file_extension = "png"
# file_name = file_name+"."+file_extension
# # image_file = open(file_name) #will open the file, if file does not exist, it will be created and opened.
# img.save(file_name,file_extension.upper()) #write qrcode encoded data to the image file.
# # image_file.close() #close the opened file handler.

# def decodeQRCode():
#     d = qr.Decoder()
#     if d.decode('E:/MY-PROJECTS/pythonRest-ANPR/static/NumberPlates/2018-03-07/qrcodes/8936fb12-b7cb-438e-9db1-5d65e5b554f0_qrcode.png'):
#         print('result: ' + d.result)
# decodeQRCode()


import configparser
config = configparser.RawConfigParser()

config.read('ConfigFile.properties')

print(config.get('DatabaseSection', 'database.dbname'))