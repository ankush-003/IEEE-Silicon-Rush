from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
import sys
import time
import pandas as pd
from requests import get, post
import json

def index(request):
    #shome(request)
    return render(request,'html1.html')

"""def home(request):
    imglink = "https://s3-ap-southeast-2.amazonaws.com/media.mieducation.production/logos/OpIwRHug1Syv739PFy1Z8VSILSDKVtgzt0ibFVLV.jpeg"
    response = requests.get('https://api.ocr.space/parse/imageurl?apikey=K86164000988957&url={}'.format(imglink)).json()
    return render(request,'home.html',{'response':response})
    """

def home(request):
    # -*- coding: utf-8 -*-
    """
    Spyder Editor
    INTRODUCTION
    This is a script file to perform the following operations:

        1.Use Microsoft Azure Computer vision Cognitive service to extract text from images (OCR) stored on Blob storage or any link.
        2.Export the extracted text to an MS Excel file on your desktop for further analysis
    
        pip install --upgrade azure-cognitiveservices-vision-computervision
        pip install pillow
        pip install azure-storage-blob
    """

    """ IMPORT LIBRARIES """



    """ CREATE A PYTHON DATAFRAME TO STORE OUTPUT """
    output=pd.DataFrame()

    """ AUTHENTICATE TO COMPUTER VISION """

    subscription_key = "<<REPLACE_subscription_key>>"
    endpoint = "<<REPLACE_endpoint>>"

    computervision_client = ComputerVisionClient('https://healthify.cognitiveservices.azure.com/', CognitiveServicesCredentials('6a34dfc3a2354a2c92c8ac9afd49adaa'))

    """ CALL THE API AND GET RESULTS (TEXT IN AN IMAGE), THEN PRINT THE RESULTS LINE BY LINE """

    print("===== Batch Read File - remote =====")

    # Get an image with handwritten text, REPLACE image link as per your requirements
    remote_image_handw_text_url = "https://news.cancerconnect.com/.image/t_share/MTc5OTc1MDg4NDc1Njc3ODE4/image-placeholder-title.png"

    # Call API with URL and raw response (allows you to get the operation location)
    recognize_handw_results = computervision_client.read(remote_image_handw_text_url,  raw=True)

    # Get the operation location (URL with an ID at the end) from the response
    operation_location_remote = recognize_handw_results.headers["Operation-Location"]

    # Grab the ID from the URL
    operation_id = operation_location_remote.split("/")[-1]

    # Call the "GET" API and wait for it to retrieve the results 
    while True:
        get_handw_text_results = computervision_client.get_read_result(operation_id)
        
        if get_handw_text_results.status not in ['notStarted', 'running']:
            break
        time.sleep(1)

    # Print the detected text, line by line
    if get_handw_text_results.status == OperationStatusCodes.succeeded:
        for text_result in get_handw_text_results.analyze_result.read_results:
            for line in text_result.lines:
                print(line.text)
                ser = pd.Series(line.text)
                output = output.append (ser,ignore_index=True)
                #print(line.bounding_box)
                
    print()
    # Export the Output to MS Excel with custom sheet name
    output.to_excel("Words1x.xlsx", sheet_name="WordList")

def converted(request):
    home(request)


import cv2 as cv

import numpy as np

def click():
    cam = cv.VideoCapture(0)

    cv.namedWindow("test")

    img_counter = 0

    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv.imshow("test", frame)

        k = cv.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k%256 == 13:
            # SPACE pressed
            img_name = "opencv_frame_{}.png".format(img_counter)
            cv.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1

    cam.release()

    cv.destroyAllWindows()
    return img_counter, img_name


def clickreport(request):
    img_counter, img_name = click()
    return render(request, "click.html", {"img_counter":img_counter, "imgsrc":img_name})





