from tkinter import *
from replit import db
from classStructure import Event
from functions import clear_frame
from time import sleep
import os

def delete(event_id, go_home):
  event = Event.load(Event.retrieve(event_id))
  if event.image:
    try: #redundancy in case a user accidentily manually deletes an image 
      os.remove(event.image) #deletes associated image
    except:
      print("Image location not syncronized with event, please check the folder static/images/event_backgrounds and make sure the associated image gets deleted")
  
  del db["events"][event_id]
  go_home()

def event_deletion_screen(frame, create_home_screen):  # returns None if user backout, otherwise JSON
  clear_frame(frame)
  def go_home():
    clear_frame(frame)
    create_home_screen(frame)
  
  MAX_COLUMN = 0
  
  title_label = Label(frame, text="Event Deletion")
  subtitle_label = Label(frame, text="Please select the event which you would like to delete, then click the affirm button!")
  
  title_label.grid(row=0, column=MAX_COLUMN//2)
  subtitle_label.grid(row=1, column=MAX_COLUMN//2)

  #dropdown logic
  event_ids = list(db["events"].keys())
  current = StringVar()
  
  try:
    current.set(event_ids[0])
    
  except IndexError: 
    clear_frame(frame)
    print("There are no registered events in the database! Please submit an ad before you wish to delete one!")
    go_home()

  else:
    dropdown = OptionMenu(frame, current, *event_ids)
    dropdown.grid(row=2,column=0)
  
    submit_button = Button(frame, text="DELETE SELECTED EVENT", command=lambda: delete(current.get(), go_home))
    submit_button.grid(row=3,column=0)
  
    home_button = Button(frame, text="RETURN HOME", command=go_home)
    home_button.grid(row=4,column=0)