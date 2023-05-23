#modules
from tkinter import *

import os
from time import sleep
from multiprocessing import Process
from threading import Thread

#local imports
from replit import db
from classStructure import Event
from functions import clear_frame, wait_for_file, get_event_images, get_image_path

#primary functions

#Checks to see on submit if values entered are okay
def check(id, evar): #add more checks with pertinence to text length, to prevent wrapping on HTML CSS side
  t = "\n"
  illegal = ".,()[]!@#$%^&*_-+={}\|;:\\\"\'<>?/~`"
  
  if not id:
    return False

  if id in db.keys():
    t += "This event ID is taken, please return home and remove the mentioned event, or enter a different event ID\n"
  
  if " " in id or "\n" in id or "\t" in id:
    t += "Please refrain from using spaces, newlines, and tab characters in eventID\n"
  
  # if len([x for x in id if x.isdigit()]) > 0: num characters are okay
  #   t += "Please refrain from using number characters in eventID\n"
  
  if len([x for x in id if x in illegal]) > 0:
    t += "Please refrain from using special characters in eventID\n"
  
  evar.set(t)
  return t == "\n" # t will remain \n if no issues are found in event submission

def submit(valid_event, evar, go_home, header, subheader, st_right, st_left, id): # this runs regardless but tf: bool will decide whether or not to upload class data to DB assuming all checks passed
  #reformatting labels to raw data
  header = header.get()
  subheader = subheader.get()
  st_right = st_right.get()
  st_left = st_left.get()
  
  id = id.get()

  if valid_event:
    for img in get_event_images(): 
      if "temp" in img and img.split(".")[0][-1].isdigit(): #uploaded image is both valid and new, therefore we sync it to the ID for future use
        os.rename(get_image_path("event") + img, get_image_path("event") + id + ".jpg") # will prevent file deletion and sync it to the event
        image = get_image_path("event") + id + ".jpg"
        break
    else:
      image = None
    
    e = Event(id=id, header=header, subheader=subheader, subtext_right=st_right, subtext_left=st_left, image=image)
    e.store_in_database()
    
    go_home()
    
def create_event_screen(frame, create_home_screen): # returns None if user backout, otherwise JSON
  clear_frame(frame)

  MAXCOLUMN = 5 #used for centering
  title_label = Label(frame, text="Event Edit/Upload").grid(row=0, column=0, columnspan=MAXCOLUMN)
  
  header_label = Label(frame, text="Event Header")
  subheader_label = Label(frame, text="Event Subheader")
  subtext_right_label = Label(frame, text="Right Bottom Subtext")
  subtext_left_label = Label(frame, text="Left Bottom Subtext")
  event_id_label = Label(frame, text="Event ID")
  
  header_entry = Entry(frame);header_entry.insert(0, "Coding Club Meet")
  subheader_entry = Entry(frame);subheader_entry.insert(0, "Thursday 3/14/2023")
  subtext_right_entry = Entry(frame);subtext_right_entry.insert(0, "Block 4")
  subtext_left_entry = Entry(frame);subtext_left_entry.insert(0, "Room 2412")
  event_id_entry = Entry(frame);event_id_entry.insert(0, "For future event reference")

  widgets = [
    [header_label, subheader_label, subtext_right_label, subtext_left_label, event_id_label],
    [header_entry, subheader_entry, subtext_right_entry, subtext_left_entry, event_id_entry]
  ]

  for i in range(len(widgets)): 
    for k in range(len(widgets[i])):
      widgets[i][k].grid(row=i+1, column=k)#+1 as row 0 contains title for frame

  evar = StringVar() #will be passed into different process to update error messages
  error_label = Label(frame, textvariable=evar) #text will be modified due script upon checked conditions
  error_label.grid(row=5, column=0, columnspan=MAXCOLUMN)

  def kill_invalid_images():
    for img in get_event_images():
      if "temp" in img and img.split(".")[0][-1].isdigit():
        os.remove(get_image_path("event") + img)
  
  def kill_process_then(process, func):
    process.kill()
    func(frame)
    kill_invalid_images() # fix images first in submit to ID name, so it wont delete valid images
  
  go_home = lambda: kill_process_then(p, create_home_screen)
  
  instruction_label = Label(frame, text="\nPlease read before submitting an event\nTo upload an image(optional) please(in order)...\n1) Find the filebar to your left\n2) Navigate to the folder in static/images/event_backgrounds\n3) Upload your image inside of the aforemenetioned folder\n4) Click SUMBIT EVENT when form is completely done!\n\nDO NOT UPLOAD MORE THAN 1 IMAGE, OR REMOVE AN IMAGE FROM THE FOLDER!\nIF YOU MAKE A MISTAKE GO BACK TO THE HOME SCREEN AND TRY AGAIN")
  instruction_label.grid(row=3, column=0, columnspan=MAXCOLUMN)

  iuvar = StringVar()
  
  image_uploaded_label = Label(frame, textvariable=iuvar)
  image_uploaded_label.grid(row=4, column=0, columnspan=MAXCOLUMN//2)
  iuvar.set("Image Uploaded? NO")
  
  form_complete_button = Button(frame, text="SUBMIT EVENT", command=lambda: submit(check(event_id_entry.get(), evar), evar, go_home,
                                                                                  header_entry,
                                                                                  subheader_entry,
                                                                                  subtext_right_entry, 
                                                                                  subtext_left_entry,
                                                                                  event_id_entry
                                                                                ))
  form_complete_button.grid(row=4, column=(MAXCOLUMN//2))
  
  home_button = Button(frame, text="RETURN HOME", command=go_home)
  home_button.grid(row=4, column=(MAXCOLUMN//2)+1)

  #begins thread to check for image upload in the event_backgrounds folder
  p = Process(target=wait_for_file, args=(get_image_path("event"),))
  p.start() #This process is killed upon going to the homescreen or successful event submission.

  def wait_for_process_kill(proc, label):
    while proc.is_alive():
      sleep(1)
          
    for img in get_event_images():
      if "temp" in img and img.split(".")[0][-1].isdigit(): #uploaded image is both valid and new, therefore we sync it to the ID for future use
        label.set("Image Uploaded? YES")
        return

  t = Thread(target=wait_for_process_kill, args=(p, iuvar))
  t.start() #thread will kill itself upon process kill, which will occur when returning home, submitting an event, or uploading and image