import os
from time import sleep
from threading import Thread

#misc
def clear_frame(frame):
  for widgets in frame.winfo_children():
    widgets.destroy()
    
#Image stuff
IMAGE_PATH = "/home/runner/MHSNScrape/static/images/"
get_image_path = lambda type_: IMAGE_PATH + type_ + "_backgrounds/"

def get_images(path):
  return [img for img in os.listdir(path)]

def get_event_images():
  PATH = IMAGE_PATH + "event_backgrounds"
  return get_images(PATH)

def get_advertising_images():
  PATH = IMAGE_PATH + "advertising_backgrounds"
  return get_images(PATH)
  
def find_difference(before: list, after: list):
  if len(before) == len(after):
    return None
    
  b = sorted(before.copy())
  b.append("filler") #lists of equal length so we can make comparisons on last element
  
  a = sorted(after.copy())
  
  for i in range(len(b)):
    if b[i] != a[i]:
      return a[i] #new file will always be in after list, b[i] == a[i+1] assuming we hit the difference

def get_recent_upload(PATH):
  end = os.lisdir()

def wait_for_file(PATH): #planned to be threaded
  
  before = get_event_images()
  current = before

  temporary_name = "temp" + str(len(before) + 1)
  while not find_difference(before, current):
    current = get_event_images()
    sleep(1)
    
  uploaded_image = find_difference(before, current)
  
  temporary_name = IMAGE_PATH + ("event_backgrounds/" if "event" in PATH else "advertising_backgrounds/") + temporary_name + "." + uploaded_image.split(".")[1]
  
  if uploaded_image.split(".")[1] not in ("jpeg", "jpg", "png"):
    os.rename(PATH + uploaded_image, PATH + "must_be_JPEG_JPG_or_PNG.jpg") #we cannot update labels from different process, therefore this convoluted fix will have to suffice
    sleep(1)
    os.remove(PATH + "must_be_JPEG_JPG_or_PNG.jpg")
    return

  print(f"New file uploaded, {uploaded_image}\nPlease continue your submission")
  
  os.rename(PATH + uploaded_image, temporary_name) #keeps file extension, changes name to length of directory for access during submit faze

  
  