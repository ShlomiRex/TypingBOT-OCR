import os
import pyautogui
import ConfigParser
import PIL
import time
import pytesseract

#Gives you time to set screen
time.sleep(3)

for x in range(1,30):

    #Configuration
    configParser = ConfigParser.RawConfigParser()   
    configFilePath = r'settings.config'
    configParser.read(configFilePath)
    start_x = configParser.get("ScreenshotBounds","start_x")
    start_y = configParser.get("ScreenshotBounds","start_y")
    end_x = configParser.get("ScreenshotBounds","end_x")
    end_y = configParser.get("ScreenshotBounds","end_y")

    print(start_x, start_y, end_x, end_y)

    #Constants
    image_name = "screenshot.png"
    text_of_image_file_name = "imagetext"

    #Take screenshot and save
    image = pyautogui.screenshot().save(image_name)
    #Crop image to fit bounds of text
    image2 = PIL.Image.open(image_name)
    image2 = image2.crop( ((int)(start_x), (int)(start_y), (int)(end_x), (int)(end_y)) )
    image2.save(image_name)
    os.system("tesseract " + image_name + " " + text_of_image_file_name + " -psm 7")
    text_file = open("imagetext.txt","r")

    text = text_file.read()
    pyautogui.typewrite(text)
    pyautogui.typewrite(' ')
    