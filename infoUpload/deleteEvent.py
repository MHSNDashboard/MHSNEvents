from tkinter import *
from replit import db
from classStructure import Event
from functions import clear_frame

def create_deletion_screen(frame, go_home):  # returns None if user backout, otherwise JSON
  title_label = Label(frame, text="Event Deletion")
  