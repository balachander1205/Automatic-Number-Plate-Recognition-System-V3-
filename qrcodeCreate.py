import qrcode
from datetime import datetime

def generateQRCode(qrcodefilename, data, numplateimgpath, imagefilepath, alpr_id):
    now = datetime.now()
    currdate = now.strftime("%Y-%m-%d")
    now_1 = datetime.now()    
    cur_datetime = now_1.strftime("%Y-%m-%d %H:%M")
    global startdatetime
    startdatetime = cur_datetime
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data("<data>")
    qr.add_data("<id>"+alpr_id+"</id>")
    qr.add_data("<veh_img>"+imagefilepath+"</veh_img>")
    qr.add_data("<img>"+numplateimgpath+"</img>")
    qr.add_data("<date>"+currdate+"</date>")
    qr.add_data("<time>"+cur_datetime+"</time>")    
    qr.add_data("<qrcode>"+qrcodefilename+"</qrcode>")
    qr.add_data("</data>")
    qr.make(fit=True)

    img = qr.make_image()
    file_extension = "png"
    file_name = qrcodefilename+"."+file_extension  # created file with extention
    img.save(file_name,file_extension.upper()) #write qrcode encoded data to the image file.
    return startdatetime
## End of QRCode generation
