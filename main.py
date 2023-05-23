#main imports
from flask import Flask, render_template, url_for
from flask_cors import CORS

from replit import db

from multiprocessing import Process

import requests, json, os, base64, time
#file imports
from helper import aware
from pprint import pprint

#this is to be run in a seperate process
from home import start_info_upload

def run_flask_app():
  app = Flask(__name__)
  CORS(app) #allows communication with web based application

  today_is = aware.get_day_type()
  weather_dict = aware.get_weather()
  
  if weather_dict['description'] is not None:
    description = weather_dict['description']
  else:
    description = None
  
  current = weather_dict['current']
  forecast = weather_dict['forecast']
  high_low = weather_dict['high_low']
  precip = weather_dict['precipitationPercent']
  
  @app.route('/')
  def home():
    #Runs on get request; Means it'll run on new sessions and when the user refreshes
    today_is = aware.get_day_type()
    weather_dict = aware.get_weather()
		
    if weather_dict['description'] is not None:
      description = weather_dict['description']
    else:
      description = None
			
    current = weather_dict['current']
    forecast = weather_dict['forecast']
    high_low = weather_dict['high_low']
    precip = weather_dict['precipitationPercent']
    
    #For quote generation
    JSON = requests.get('https://zenquotes.io/api/random').text
    quote = str(json.loads(JSON)[0]['q'])
		
		#Get background image based on weather context
    if 'cloud' in forecast.lower():
      weather_img_name = 'Cloudy.jpg'
    elif 'sun' in forecast.lower() or 'clear' in forecast.lower() or 'fair' in forecast.lower():
      weather_img_name = 'Sunny.jpeg'
    elif 'snow' in forecast.lower():
      weather_img_name = 'Snowy.jpeg'
    elif 'rain' in forecast.lower() or 'shower' in forecast.lower() or 'drizzle' in forecast.lower():
      weather_img_name = 'Rainy.jpeg'
    elif 'thunder' in forecast.lower() or 'lightning' in forecast.lower() or 'storm' in forecast.lower():
      weather_img_name = 'Thunder.jpeg'
    else:
      weather_img_name = 'Unknown.jpg'

    #convert img to b64
    with open("/home/runner/MHSNScrape/static/images/" + weather_img_name, "rb") as img:
      lines = img.read()
      ba = bytearray(lines)
      
      base64_bytes = base64.b64encode(ba)
      base64_message = base64_bytes.decode('ascii')
      
      storable = "data:image/png;base64," + base64_message
      weather_image = storable
    
    current = current.replace("F", "°")
    high_low = high_low.replace("F", "°")

    ads = []
    for key in db.keys():
      ads.append(dict(db[key]))

    #formatting data
    json_data = {
      "weather" : {
        "image" : weather_image,
        "current" : current,
        "high_low" : high_low,
        "forecast" : forecast,
        "description" : description,
        "precipitation" : precip,
      },
      
      "top_box" : {
        "quote" : quote,
        "AB" : today_is,
      },
      
      "advertisements" : ads,
      
    }

    #Renders website image
    template = render_template('MHSN.html', JSON=json.dumps(json_data))
    
    with open("previousRun.html", 'w') as f: #writes JSON html file to project for review
      f.write(template)

    return template
  
  if __name__ == '__main__': #posts website
    app.run(host="0.0.0.0", port=9050)

event_process = Process(target = start_info_upload)
event_process.start()

flask_process = Process(target = run_flask_app)
flask_process.start()

event_process.join() # so main thread doesn't kill everything after initializing the two processes