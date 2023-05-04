#main imports
from flask import Flask, render_template, url_for
from flask_cors import CORS

import requests, json, os
#file imports
from helper import aware
from pprint import pprint

def run_flask_app():
	app = Flask(__name__)
	CORS(app)

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
		print("working")
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
			type_ = 'Cloudy.jpg'
		elif 'sun' in forecast.lower() or 'clear' in forecast.lower() or 'fair' in forecast.lower():
			type_ = 'Sunny.jpeg'
		elif 'snow' in forecast.lower():
			type_ = 'Snowy.jpeg'
		elif 'rain' in forecast.lower() or 'shower' in forecast.lower() or 'drizzle' in forecast.lower():
			type_ = 'Rainy.jpeg'
		elif 'thunder' in forecast.lower() or 'lightning' in forecast.lower() or 'storm' in forecast.lower():
			type_ = 'Thunder.jpeg'
		else:
			type_ = 'Unknown.jpg'
		
		weather_image = url_for('static', filename=f'images/{type_}')

		sep = "␟" #Delimeter I'm using is ASCII 31, line separator character "␟"
		
		#Needs to come out as [bigTexts: [...], middleTexts: [...] etc]
		def unpackAdvertContents(original, file = "advertisingDB.txt"): #TODO add file parsing
			
			if os.stat(file).st_size == 0:
				return original
			else:
				with open(file, "r") as f: #storing them as[Ad 1: [bgtxt, mdtxt...], Ad 2: [...] etc]
					lines = "\n".join(f.read().split("\n")[1:]) # each advertisement instance
					newAds = original
					
					if len(lines) > 1 and "\n" in lines: #there are multiple ads to display
						lines = lines.split("\n")
						for line in lines:
							params = line.split(sep) #each element of the advert
							for iter_, param in enumerate(params): 
								if sep in param:
									param.replace(sep, "")

								#checks for file extensions, if there are, redirect it to the folder it resides in
								if len([param.endswith("." + x) for x in ["jpg", "jpeg", "png", "gif", "ai", "pdf", "eps"] if param.endswith("." + x)]) >= 1:
									param = url_for("static", filename = ("images/advertisingBackgrounds/" + param))
									
								newAds[iter_].append(param)
					else:
						params = lines.split(sep) #each element of the advert
						for iter_, param in enumerate(params):
							if sep in param:
								param.replace(sep, "")

							#checks for file extensions, if there are, redirect it to the folder it resides in
							if len([param.endswith("." + x) for x in ["jpg", "jpeg", "png", "gif", "ai", "pdf", "eps"] if param.endswith("." + x)]) >= 1:
								param = url_for("static", filename = ("images/advertisingBackgrounds/" + param))
								
							newAds[iter_].append(param)
			
			for i in range(len(newAds)):
				newAds[i] = sep.join(newAds[i])

			return newAds
				
		
		advertisingAdvert = [
					["Want an ad on the dashboard?"],
					["Reach out to Tujaguem@middletownk12.org for info on how to add an advert"],
					["Your name, credits"],
					["More room for text"],
					["None"]
				]

		#As long as these are packed correctly here, order doesn't matter until we get to the other file.
		curBigText, curMiddleText, curSmallTextOne, curSmallTextTwo, curBackground = unpackAdvertContents(advertisingAdvert)
		
		current = current.replace("F", "°")
		high_low = high_low.replace("F", "°")

		#Starts website
		template = render_template('MHSN.html', 
								#weather stuff
							   	forecast=forecast, current=current, high_low=high_low, 
							   	# weather_image=weather_image, 
                  description=description, precip = precip,
							   
							  	#quotes n dayType
							   	quote=quote, today_is=today_is,
							   
								#advertisements
							   	bigText = curBigText, 
							   	middleText = curMiddleText,
							   	smallTextOne = curSmallTextOne, smallTextTwo = curSmallTextTwo,
							   	background = curBackground,

							   	len = len, #used for jinja if statements
							 	listSeparator = sep
							)
    
		with open("htmlfile.html", 'w') as f:
			f.write(template)
			
		return template
	if __name__ == '__main__':
		app.run(host="0.0.0.0", port=8080)

run_flask_app()