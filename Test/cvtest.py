import cv2 as cv
import numpy as np
from PIL import Image
import pytesseract as tess

tess.pytesseract.tesseract_cmd = r"D:\ProgrammingSoftware\Tesseract-OCR\tesseract.exe"

#cv.imshow("Report", img)
filepath = 'r1.jpg'
img = cv.imread(filepath)

extracted_text = tess.image_to_string(img)

#img1 = np.array(Image.open(filepath))
#text = pytesseract.image_to_string(img1)
print(extracted_text)
