import os
import shutil
import easyocr
from PIL import Image as img
from pylab import rcParams
from pdf2image import convert_from_path
from googletrans import Translator
import json
import base64
import argparse
from pymongo import MongoClient

CONNECTION_STRING = "mongodb+srv://tanishq777:tanishq777@cluster0.lzgyb.mongodb.net/ElectionMitra?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)

PROCESSING_IMG_PATH = ".\\static\\FILES\\PROCESSING_IMG"
PROCESSING_PDF_PATH = ".\\static\\FILES\\PROCESSING_FILE"
PROCESSED_IMG_PATH = ".\\static\\FILES\\PROCESSED_IMG"
PROCESSED_PDF_PATH = ".\\static\\FILES\\PROCESSED_FILE"
CROPPED_IMG_PATH = ".\\static\\FILES\\CROPPED_IMG"
TEMP_STORAGE_PATH = ".\\static\\FILES\\TEMP_STORAGE_PATH"
RESULT_PATH = ".\\static\\FILES\\RESULTS"

translator = Translator()
rcParams['figure.figsize'] = 16, 32
reader = easyocr.Reader(['en'])
reader_hindi = easyocr.Reader(['hi'])

def extract_img_from_pdf():
    print("converting pdf into images...", end='\n')
    # Store Pdf with convert_from_path function
    for file_name in os.listdir(PROCESSING_PDF_PATH):
        
        file_path = os.path.join(PROCESSING_PDF_PATH, file_name)
        images = convert_from_path(file_path)
    
        for i in range(len(images)):
            # Save pages as images in the pdf
            file = file_name.split('.')
            images[i].save(os.path.join(PROCESSING_IMG_PATH, f'{file[0]}_page_{str(i)}.jpeg'), 'JPEG')
            print(f'Created image {file_name}', end='\n')

        # move file to processed folder
        new_file_path = os.path.join(PROCESSED_PDF_PATH, file_name)
        shutil.move(file_path, new_file_path)

def crop_data_block_from_sheet():
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

        for i in range(10):
            for j in range(3):
                block_img = image1.crop((block_width * j, block_height*i, block_width* (j+1), block_height*(i+1)))
                block_img = block_img.convert("RGB")
                img_name = image_name.split('.')

                block_path = os.path.join(CROPPED_IMG_PATH, f'{img_name[0]}_page_{str(i)}_{str(j)}.jpeg')
                block_img.save(block_path, "JPEG")
                print(f"Created image {img_name}", end='\n')


        new_image_path = os.path.join(PROCESSED_IMG_PATH, image_name)
        shutil.move(image_path, new_image_path)

def extract_voter_name(filename):
    block_path = os.path.join(CROPPED_IMG_PATH, f'{filename}')

    block_img  = img.open(block_path)
    # width, height = block_img.width, block_img.height

    left = 120
    top = 45
    right = 350
    bottom = 80

    f1 = block_img.crop((left, top, right, bottom))
    f1 = f1.convert("RGB")
    temp_storage_path = os.path.join(TEMP_STORAGE_PATH, f'{filename}_fist_name.jpeg')
    f1.save(temp_storage_path, "JPEG")

    op = reader_hindi.readtext(temp_storage_path)
    st = ""
    for i in op:
      st+=(i[1]+" ")
    data = translator.translate(st).text
    if(len(data) == 3):
        last_name = data.split(" ")[0]
        first_name = data.split(" ")[1]
        middle_name = data.split(" ")[2]
    else:
        last_name = data.split(" ")[0]
        first_name = data.split(" ")[1]
        middle_name = ""
    
    print(f'Extracted Fist_name: {first_name}, Middle_name: {middle_name}, Last_name: {last_name} from file {filename}', end="\n")
    return last_name, first_name, middle_name

def extract_gender(filename):
    block_path = os.path.join(CROPPED_IMG_PATH, f'{filename}')

    block_img  = img.open(block_path)
    width, height = block_img.width, block_img.height

    left = 205
    top = block_img.height-40
    right = 260
    bottom = block_img.height

    f1 = block_img.crop((left, top, right, bottom))
    f1 = f1.convert("RGB")
    filename = filename.split('.')
    temp_storage_path = os.path.join(TEMP_STORAGE_PATH, f'{filename[0]}_gender.jpeg')
    f1.save(temp_storage_path, "JPEG")

    try:
        op = reader_hindi.readtext(temp_storage_path)
        print("output: ",op[0][1],end="\n\n")
        data = translator.translate(op[0][1]).text
        
        print(f"Extracted Gender: {data} from file: {filename}", end='\n')
        if data == 'PU':
            return "male"
        elif data=='Ms':
            return "female"
    except:
        print("[ERROR IN EXTRACTING GENDER]\n")
        return ""

def extract_voter_id(filename):
    block_path = os.path.join(CROPPED_IMG_PATH, f'{filename}')

    block_img  = img.open(block_path)
    # width, height = block_img.width, block_img.height

    left = 0
    top = 0
    right = 500
    bottom = 40

    f1 = block_img.crop((left, top, right, bottom))
    f1 = f1.convert("RGB")
    filename = filename.split('.')
    temp_storage_path = os.path.join(TEMP_STORAGE_PATH, f'{filename[0]}_voter_id.jpeg')
    f1.save(temp_storage_path, "JPEG")

    op = reader.readtext(temp_storage_path)
    st = ""
    for i in op:
      st+=(i[1]+" ")
    data = translator.translate(st).text
    voterID = data.split(" ")[1]
    print(f"Extracted VoterID: {voterID} from file: {filename}", end='\n')
    return voterID

def img_to_base64(filename):
    block_path = os.path.join(CROPPED_IMG_PATH, f'{filename}')
    # print(block_path, end='\n')
    with open(block_path, "rb") as img_file:
        imageString = base64.b64encode(img_file.read())
    print(f"Converted {filename} to base64", end='\n')
    return imageString

def extract_data(district, city, ward):

    extract_img_from_pdf()
    crop_data_block_from_sheet()

    client["voters"]
    c = client["ElectionMitra"]
    # voters = c["Voters"].find()
    addVoter = c["Voters"]

    for image_name in os.listdir(CROPPED_IMG_PATH):

        # print(image_name,end='\n')
        last_name, first_name, middle_name = extract_voter_name(image_name)
        voter_id = extract_voter_id(image_name)
        voter_gender = extract_gender(image_name)
        img_base64 = img_to_base64(image_name)

        voter = {
            "firstName" : first_name,
            "middleName" : middle_name,
            "lastName" : last_name,
            "gender": voter_gender,
            "voterID" : voter_id,
            # "imageString": str(img_base64)[2:-2],
            "district":district,
            "city":city,
            "ward":ward
        }
        print(voter, end="\n")
        # print(img_base64, end="\n")

        # voters = c["voters"].find()
        print(f"Stored data of {voter_id} to Database", end='\n\n')
        # addVoter.insert_one(voter)
        # shutil.rmtree(CROPPED_IMG_PATH)
        # shutil.rmtree(TEMP_STORAGE_PATH)
  



if __name__=="__main__":
    # print(extract_voter_name("trial_page_0_page_0_0"))
    # print(extract_voter_id("trial_page_0_page_0_0"))
    # print(img_to_base64("trial_page_0_page_0_0"))
    # print(extract_gender("trial (1)-pages-4_page_0_page_1_1.jpeg"))
    # print(reader_hindi.readtext("C:\\Users\\asdha\Desktop\\EDI-IV\\ElectionMitraColab\\static\\FILES\\TEMP_STORAGE_PATH\\trial (1)-pages-4_page_0_page_1_1_gender.jpeg"))

    parser = argparse.ArgumentParser()
    parser.add_argument("district", help="Enter District")
    parser.add_argument("city", help="Enter City")
    parser.add_argument("ward", help="Enter Ward")
    args = parser.parse_args()
    # print(args.district, args.ward, args.city)
    extract_data(args.district, args.city, args.ward)


# 











