import base64, time
from replit import db

class Event:
  #Attributes of events, due to change when HTML/CSS comes up for the website
  def __init__(self, id, header="", subheader="", subtext_right="", subtext_left="", image=None, image_data=None):
    self.id = id
    self.header = header
    self.subheader = subheader
    self.subtext_right = subtext_right
    self.subtext_left = subtext_left
    self.image = image
    
    if image: #image would be a location, for instanciations, we would expect to inject image_data as we already have it from previous go's
      with open(image, "rb") as i:
        lines = i.read()
        ba = bytearray(lines)
        
        base64_bytes = base64.b64encode(ba)
        base64_message = base64_bytes.decode('ascii')
        
        storable = "data:image/png;base64," + base64_message
      self.image_data = storable #store as a byte array to be stored in DB, postable as readable text via html, HTTPS can read it and then on new website it works as src
    
    else:
      self.image_data = image_data if image_data else ""
  
  def store_in_database(self):
    json_serializable_data = {"id": self.id, "header" : self.header, "subheader" : self.subheader, 
                              "subright" : self.subtext_right, "subleft" : self.subtext_left, "image" : self.image, "image_data" : self.image_data}
    db[self.id] = json_serializable_data
  
  def retrieve(id: str):
    data = db[id]
    return Event(*data.values()) #return either dict or object

  def load(attrs: dict): 
    return Event(attrs.id, attrs.header, attrs.subheader, attrs.subtext_right, attrs.subtext_left, attrs.image, attrs.image_data) # load dict or object
    
  #takes a 'check' function as a parameter to make matches
  def find_all(lmbda):
    found = []
    
    for key in db.keys():
      if lmbda(db[key]): #lambda function should take values from each key in DB
        found.append(key)
  
  def remove_from_database(name: str):
    del db[name]

