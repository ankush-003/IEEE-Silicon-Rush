#Importing libraries
import cv2
import pytesseract
import numpy as np
 
#Loading image using OpenCV
img = cv2.imread('sample.png')
 
#Preprocessing image
#Converting to grayscale
gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 
#creating Binary image by selecting proper threshold
binary_image = cv2.threshold(gray_image ,130,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
 
#Inverting the image
inverted_bin = cv2.bitwise_not(binary_image)
 
#Some noise reduction
kernel = np.ones((2,2),np.uint8)
processed_img = cv2.erode(inverted_bin, kernel, iterations = 1)
processed_img = cv2.dilate(processed_img, kernel, iterations = 1)
 
#Applying image_to_string method
text = pytesseract.image_to_string(processed_img)
 
print(text)