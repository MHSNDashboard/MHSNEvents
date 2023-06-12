import os
from tkinter import *
from replit import db
from hashlib import sha256 # to protect uploading application

from classStructure import Event
from uploadEvent import create_event_screen
from deleteEvent import event_deletion_screen

from uploadAdvertisement import create_advertisement_screen
from deleteAdvertisement import advertisement_deletion_screen
from functions import clear_frame

def create_home_screen(frame):
  clear_frame(frame)
    
  password_entry = Entry(frame)
  def create_event_pathway():
    if sha256(password_entry.get().encode('utf-8')).hexdigest() == os.getenv("AUTHENTICATION_PASSWORD"):
      clear_frame(frame)
      create_event_screen(frame, create_home_screen)
    else:
      print("PASSWORD INCORRECT, PLEASE TRY AGAIN")

  def create_advertisement_pathway():
    if sha256(password_entry.get().encode('utf-8')).hexdigest() == os.getenv("AUTHENTICATION_PASSWORD"):
      clear_frame(frame)
      create_advertisement_screen(frame, create_home_screen)
    else:
      print("PASSWORD INCORRECT, PLEASE TRY AGAIN")

  def delete_advertisement_pathway():
    if sha256(password_entry.get().encode('utf-8')).hexdigest() == os.getenv("AUTHENTICATION_PASSWORD"):
      clear_frame(frame)
      advertisement_deletion_screen(frame, create_home_screen)
    else:
      print("PASSWORD INCORRECT, PLEASE TRY AGAIN")
  
  def delete_event_pathway():
    if sha256(password_entry.get().encode('utf-8')).hexdigest() == os.getenv("AUTHENTICATION_PASSWORD"):
      clear_frame(frame)
      event_deletion_screen(frame, create_home_screen)
    else:
      print("PASSWORD INCORRECT, PLEASE TRY AGAIN")
      
  #Labels
  title_label = Label(frame, text="MHSNDash Event Editor")
  choice_label = Label(frame, text="Will you be uploading/deleting an event/advertisement?")
  
  #Label placement
  title_label.grid(row=0, column=1)
  choice_label.grid(row=1, column=1)
  
  #Buttons
  event_button = Button(frame, text="UPLOAD EVENT", command=create_event_pathway)
  delete_event_button = Button(frame, text="DELETE EVENT", command=delete_event_pathway)

  advertisement_button = Button(frame, text="UPLOAD ADVERTISEMENT", command=create_advertisement_pathway)
  delete_advertisement_button = Button(frame, text="DELETE ADVERTISEMENT", command=delete_advertisement_pathway)
  
  password_entry.insert(0, "Password:")
  
  #Button placement
  event_button.grid(row = 2, column = 0)
  delete_event_button.grid(row = 4, column = 0)
  
  password_entry.grid(row = 3, column = 1)

  advertisement_button.grid(row = 2, column = 2)
  delete_advertisement_button.grid(row = 4, column = 2)
      
def start_info_upload():
  root = Tk()
  width = root.winfo_reqwidth()
  height = root.winfo_reqheight()
  
  root.title("MHSNDash Data Interface!")
  root.configure(width=500, height=500)
  
  frame = Frame(root) #only frame that will exist
  frame.pack(side="top", expand=True, fill="both")
  
  create_home_screen(frame)
  root.mainloop() #End of program, for longevity