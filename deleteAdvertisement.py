from tkinter import *
from replit import db
from classStructure import Advertisement
from functions import clear_frame
from time import sleep
import os

def delete(ad_id, go_home):
  ad = Advertisement.load(Advertisement.retrieve(ad_id))
  if ad.image:
    try: #redundancy in case a user accidentily manually deletes an image 
      os.remove(ad.image) #deletes associated image
    except:
      print("Image location not syncronized with ad, please check the folder static/images/ad_backgrounds and make sure the associated image gets deleted")
  
  del db["ads"][ad_id]
  go_home()

def advertisement_deletion_screen(frame, create_home_screen):  # returns None if user backout, otherwise JSON
  clear_frame(frame)
  def go_home():
    clear_frame(frame)
    create_home_screen(frame)
  
  MAX_COLUMN = 0
  
  title_label = Label(frame, text="Advertisement Deletion")
  subtitle_label = Label(frame, text="Please select the ad which you would like to delete, then click the affirm button!")
  
  title_label.grid(row=0, column=MAX_COLUMN//2)
  subtitle_label.grid(row=1, column=MAX_COLUMN//2)

  #dropdown logic
  ad_ids = list(db["ads"].keys())
  current = StringVar()
  
  try:
    current.set(ad_ids[0])
    
  except IndexError: 
    clear_frame(frame)
    print("There are no registered ads in the database! Please submit an ad before you wish to delete one!")
    go_home()

  else:
    dropdown = OptionMenu(frame, current, *ad_ids)
    dropdown.grid(row=2,column=0)
  
    submit_button = Button(frame, text="DELETE SELECTED AD", command=lambda: delete(current.get(), go_home))
    submit_button.grid(row=3,column=0)
  
    home_button = Button(frame, text="RETURN HOME", command=go_home)
    home_button.grid(row=4,column=0)