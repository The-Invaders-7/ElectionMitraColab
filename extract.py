import cv2 
import os
import shutil
import easyocr
from PIL import Image as img
from pylab import rcParams
# import matplotlib.pyplot as plt
# from IPython.display import Image
from pdf2image import convert_from_path
import json


PROCESSING_IMG_PATH = ".\\static\\FILES\\PROCESSING_IMG"
PROCESSING_FILE_PATH = ".\\static\\FILES\\PROCESSING_FILE"
PROCESSED_IMG_PATH = ".\\static\\FILES\\PROCESSED_IMG"
PROCESSED_FILE_PATH = ".\\static\\FILES\\PROCESSED_FILE"
CROPPED_IMG_PATH = ".\\static\\FILES\\CROPPED_IMG"
RESULT_PATH = ".\\static\\FILES\\RESULTS"

rcParams['figure.figsize'] = 16, 32
reader = easyocr.Reader(['hi', 'en'])

'''

# Store Pdf with convert_from_path function

for file_name in os.listdir(PROCESSING_FILE_PATH):
    
    file_path = os.path.join(PROCESSING_FILE_PATH, file_name)
    images = convert_from_path(file_path)
 
    for i in range(len(images)):
        # Save pages as images in the pdf
        file = file_name.split('.')
        images[i].save(os.path.join(PROCESSING_IMG_PATH, f'{file[0]}_page_{str(i)}.jpeg'), 'JPEG')

    # move file to processed folder
    new_file_path = os.path.join(PROCESSED_FILE_PATH, file_name)
    shutil.move(file_path, new_file_path)
'''

for image_name in os.listdir(PROCESSING_IMG_PATH):
    
    image_path = os.path.join(PROCESSING_IMG_PATH, image_name)
    image = img.open(image_path)

    width, height = image.width, image.height
    left = 40
    top = 220
    right = width-60
    bottom = height-150

    image1 = image.crop((left, top, right, bottom))
    image1 = image1.convert("RGB")

    block_width, block_height = image1.width/3, image1.height/10

    print(image_name, block_height, block_width)

    for i in range(10):
        for j in range(3):
            block_img = image1.crop((block_width * j, block_height*i, block_width* (j+1), block_height*(i+1)))
            block_img = block_img.convert("RGB")
            img_name = image_name.split('.')

            block_path = os.path.join(CROPPED_IMG_PATH, f'{img_name[0]}_page_{str(i)}_{str(j)}.jpeg')
            block_img.save(block_path, "JPEG")


    new_image_path = os.path.join(PROCESSED_IMG_PATH, image_name)
    # shutil.move(image_path, new_image_path)


from googletrans import Translator
translator = Translator()

from googletrans import Translator
translator = Translator()
info = {}

for cropped_img in os.listdir(CROPPED_IMG_PATH):
    data = []
    snippet_path = os.path.join(CROPPED_IMG_PATH, cropped_img)
    text = reader.readtext(snippet_path)
    for line in text:
        tr_data = translator.translate(line[1]).text
        data.append(tr_data)
    info[cropped_img] = data
    print("image ", cropped_img, " completed")

with open("information.json","w") as file:
    json.dump(info, file)










