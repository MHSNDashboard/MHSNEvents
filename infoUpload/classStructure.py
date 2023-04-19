import base64, threading, time
from replit import db

class Event:
  #Attributes of events, due to change when HTML/CSS comes up for the website
  def __init__(self, id, title="", date="", location_time="", image=None, image_data=None):
    self.id = id
    self.title = title
    self.date = date
    self.location_time = location_time
    
    if image:
      with open(image, "rb") as i:
        lines = i.read()
        ba = bytearray(lines)
        
        base64_bytes = base64.b64encode(ba)
        base64_message = base64_bytes.decode('ascii')
        
        storable = "data:image/png;base64," + b64  
      self.image_data = storable #store as a byte array to be stored in DB, postable as readable text via html, HTTPS can read it and then on new website it works as src
    
    else:
      self.image_data = image_data if image_data else None
  
  def store_in_database(self):
    db[self.name] = self
  
  def retrieve(name: str):
    return db[name]

  def load(attrs: dict): 
    return Event(attrs['id'], attrs['title'], attrs['date'], attrs['location_time'], image_data=attrs['image_data'])
    
  #takes a 'check' function as a parameter to make matches
  def find_all(lmbda):
    found = []
    
    for key in db.keys():
      if lmbda(key):
        found.append(key)
  
  def remove_from_database(name: str):
    del db[name]

