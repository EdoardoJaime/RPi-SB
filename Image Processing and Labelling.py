from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import time

import numpy as np
from PIL import Image
from tflite_runtime.interpreter import Interpreter

from picamera import PiCamera

import serial
import cv2
def translate_arduino(arduino_input):
    
    if arduino_input == "bin_open":
        return True
    if arduino_input == "bin_closed":
        return False

def take_picture(image_location):
    camera = PiCamera()
    #time.sleep(2)
    camera.capture(image_location)
    camera.close()


def load_labels(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]


def label_image(model_location,label_location,image_location):
    interpreter = Interpreter(
        model_path=model_location, num_threads=None)
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # check the type of the input tensor
    floating_model = input_details[0]['dtype'] == np.float32

    # NxHxWxC, H:1, W:2
    height = input_details[0]['shape'][1]
    width = input_details[0]['shape'][2]
    img = Image.open(image_location).resize((width, height))

    # add N dim
    input_data = np.expand_dims(img, axis=0)

    if floating_model:
        input_data = (np.float32(input_data) - 127.5) / 127.5

    interpreter.set_tensor(input_details[0]['index'], input_data)

    start_time = time.time()
    interpreter.invoke()
    stop_time = time.time()

    output_data = interpreter.get_tensor(output_details[0]['index'])
    results = np.squeeze(output_data)

    top_k = results.argsort()[-5:][::-1]
    labels = load_labels(label_location)

    #print('{:08.6f}: {}'.format(float(results[top_k[0]]), labels[top_k[0]]))
    #print('time: {:.3f}ms'.format((stop_time - start_time) * 1000))
    
    prediction = str(labels[top_k[0]])
    
    if prediction == "Paper" or prediction == "Cardboard":
        return "Paper"
    if prediction == "Metal" or prediction == "Glass" or prediction == "Recyc_Plastic":
        return "Dry"
    if prediction == "Non_Recyc_Plastic" or prediction == "Foil":
        return "General"
    if prediction == "Food":
        return "Organic"    
    #return str(labels[top_k[0]])
    
def preprocess_image(image):
    bilateral_filtered_image = cv2.bilateralFilter(image, 7, 150, 150)
    gray_image = cv2.cvtColor(bilateral_filtered_image, cv2.COLOR_BGR2GRAY)
    return gray_image

def obtain_contour(img1_path,img2_path):
    img1 = cv2.imread(img1_path)
    img1RGB = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    img1RGB_copy = img1RGB
    img2 = cv2.imread(img2_path)
    height, width, channels = img1.shape
    final = np.zeros((height,width,3), np.uint8)
    backgroundModel = np.zeros((1, 65), np.float64)
    foregroundModel = np.zeros((1, 65), np.float64)

    preprocessed_image1 = preprocess_image(img1)
    preprocessed_image2 = preprocess_image(img2)

    image_sub = cv2.absdiff(preprocessed_image1, preprocessed_image2)
    

    kernel = np.ones((5,5),np.uint8)
    #dilation = cv2.dilate(image_sub,kernel,iterations = 1)
    close_operated_image = cv2.morphologyEx(image_sub, cv2.MORPH_OPEN, kernel)
    ret, thresh = cv2.threshold(close_operated_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    median = cv2.medianBlur(thresh, 5)
    
    
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cont = cv2.drawContours(img1RGB, contours, -1, (100, 0, 255),2)
    Image.fromarray(cont).save("/home/pi/AI/Images/contour.jpeg")

    max_x = 0
    max_y = 0

    min_x = 9999999999
    min_y = 9999999999
    for contour in contours:
        
        for sub_contour in contour:
            new_x = sub_contour[0][0]
            new_y = sub_contour[0][1]
            if new_x > max_x:
                max_x = new_x
                
            if new_y > max_y:
                max_y = new_y

            if new_x < min_x:
                min_x = new_x
                
            if new_y < min_y:
                min_y = new_y
    
    rectangle = (min_x, min_y, max_x-min_x, max_y-min_y)

    
    #rect = cv2.rectangle(img_rect_RGB, (min_x,max_y),(max_x,min_y), (255, 0, 0), 2)
    #Image.fromarray(rect).save("rect.jpeg")
    return rectangle

def obtaining_image(img1_path,rect,sav_path):

    img = cv2.imread(img1_path)
    image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
           
    mask = np.zeros(image.shape[:2], np.uint8)
       
    backgroundModel = np.zeros((1, 65), np.float64)
    foregroundModel = np.zeros((1, 65), np.float64)
 
    cv2.grabCut(image, mask, rect,  
                backgroundModel, foregroundModel,
                1, cv2.GC_INIT_WITH_RECT)
       
    
    mask2 = np.where((mask == 2)|(mask == 0), 0, 1).astype('uint8')
       
    
    image = image * mask2[:, :, np.newaxis]

    #crop_img = image[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]
    
    img = Image.fromarray(image)
    img.save(sav_path)
  
