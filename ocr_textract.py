import textract
text = textract.process('static/temp/4839.png', encoding='ascii', 
                        method='tesseract')