from tkinter import *
from replit import db
from classStructure import Event

from uploadEvent import create_event_screen
from deleteEvent import create_deletion_screen

#screens
from functions import clear_frame

def create_home_screen(frame):
  clear_frame(frame)
  
  def create_event_pathway():
    clear_frame(frame)
    create_event_screen(frame, create_home_screen)

  def delete_event_pathway():
    clear_frame(frame)
    create_deletion_screen(frame, create_home_screen)
    
  #Labels
  title_label = Label(frame, text="MHSNDash Information Upload")
  choice_label = Label(frame, text="Will you be uploading or deleting an event?")
  #Label placement
  title_label.grid(row=0, column=1)
  choice_label.grid(row=1, column=1)
  
  #Buttons
  event_button = Button(frame, text="UPLOAD EVENT", command=create_event_pathway)
  advertisement_button = Button(frame, text="DELETE EVENT", command=delete_event_pathway)
  
  #Button placement
  event_button.grid(row = 2, column = 0)
  advertisement_button.grid(row = 2, column = 2)

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