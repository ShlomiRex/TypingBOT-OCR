import os
import pyautogui
import configparser as ConfigParser
import PIL
import time

running = True

def run_once():
    global running

    #Take screenshot and save
    image_name = "screenshot.png"
    region_image_name = "region.png"
    image = pyautogui.screenshot(image_name)
    image.save(image_name)
    
    # Crop
    region_imgage = PIL.Image.open(image_name)
    region_imgage = region_imgage.crop((int(start_x), int(start_y), int(end_x), int(end_y)))
    region_imgage.save(region_image_name)

    #Crop image to fit bounds of text
    text_of_image_file_name = "imagetext" # Tesseract automatically adds .txt
    open(text_of_image_file_name+".txt","w+") # Create file
    os.system("tesseract " + region_image_name + " " + text_of_image_file_name)
    text_file = open(text_of_image_file_name+".txt","r")

    # Read text from tessaract
    text = text_file.read()
    text = text.replace("\n"," ").rstrip().lstrip().replace("  ", " ")
    text += " " # Last word doesn't have a space after it, we need to go to next image

    # Sometimes we finish fast and so the website will redirect to winner page
    # Need to stop program from writing to input box
    if len(text.split()) < 10:
        running = False
        return

    print(text)
    pyautogui.typewrite(text, interval=0, _pause=False)


if __name__ == "__main__":
    #Configuration
    configParser = ConfigParser.RawConfigParser()   
    configParser.read("settings.config")
    start_x = configParser.get("ScreenshotBounds","start_x")
    start_y = configParser.get("ScreenshotBounds","start_y")
    end_x = configParser.get("ScreenshotBounds","end_x")
    end_y = configParser.get("ScreenshotBounds","end_y")

    #Gives you time to set screen and go to the website
    time.sleep(5)

    for _ in range(100):
        if not running:
            break
        run_once()
