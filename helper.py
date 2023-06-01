from bs4 import BeautifulSoup
import requests, os, re, datetime

class aware:
  def get_day_type():
    url = "https://north.middletownk12.org/"
    soup = BeautifulSoup(requests.get(url).content, "lxml")
    
    today = datetime.date.today()
    monthDay = "/".join([str(int(x)) for x in today.strftime("%m/%d/%y").split("/")[:-1]])
    schedule = str(soup.find_all("h2", text = re.compile(monthDay)))
    
    ADAY = "A Day" in schedule
    BDAY = "B Day" in schedule
    
    FULLDAY = "Full Day" in schedule
    
    day = 'A' if ADAY else 'B' if BDAY else ""
    return day
	
  def get_weather():
		
    def isPertinent(x, *args, accuracy = 1):
      c = 0
      x = str(x).lower()
    
      for check in args:
        if check in x:
          c += 1
      return c >= accuracy

    def getNumericalValue(x):
      x = str(x)
      res = re.findall(r"(\d*F)", str(x))
      return res[0]

    url = "https://www.wunderground.com/hourly/us/nj/middletown/07748"
    soup = BeautifulSoup(requests.get(url).content, 'lxml')
    
    hilo = soup.find_all("p", attrs = {"_ngcontent-sc247" : ""}) #might be buggy, this part 
    
    try:
      hi, lo = sorted([getNumericalValue(x) for x in hilo if isPertinent(x, "high", "low", "wind", accuracy = 1)])[::-1]
    except ValueError: #occurs rarely, but after multiple tries, this is the most efficient/least crashing solution
      hi, lo = "", ""
		
    url = "https://weather.com/weather/today/l/5d8130b82a144fa9b4c4ca952fbf58a58f1931f3aec139bc0cdc71b113bce84e"
    soup = BeautifulSoup(requests.get(url).content, "lxml")
    cur = soup.find("span", re.compile("(CurrentConditions--tempValue--\w*)")).text[:-1] + "F"
    forecast = soup.find("div", re.compile("CurrentConditions--phraseValue--[\w\d]*")).text
    
    description = soup.find("h2", re.compile("AlertHeadline--alertText--[\w\d]*"))

    if description is not None:
      description = description.text      

    #Precipitation values
    options = soup.find_all("a", re.compile("Column--innerWrapper--[\w\d]* Button--default--[\w\d]*"), href="/weather/tenday/l/5d8130b82a144fa9b4c4ca952fbf58a58f1931f3aec139bc0cdc71b113bce84e")
    
    today = [x for x in options if "Today" in x.get_text()][0]
    precip = today.find("span", re.compile("Column--precip--[\w\d]*"))
    
    stringParse = precip.get_text()
    precipChance = "".join([x for x in stringParse if x.isdigit() or x == "%"])
		
    if precipChance == '0%':
      precipChance = ""
		
    final = {
      'forecast' : forecast, #FIX ONCE AVAILABLE
      'high_low' : f"{hi}/{lo}",
      'current'  : cur,
      'description' : description,
      'precipitationPercent' : precipChance
    }
		
    return final  
	
  def from_military_to_standard(hour, minute=None, str=None):
    if hour == 12:
      ampm = 'PM'
    elif hour == 24:
      ampm = 'AM'
    elif hour > 12:
      hour -= 12
      ampm = 'PM'
    elif hour < 12:
      ampm = 'AM'
    if str == True and minute is not None:
      return f'{hour}:{minute} {ampm}'
    else:
      return hour, ampm  
	
  def fix_zero(minute, second):
    if second < 10:
      second = '0' + str(second)
    if minute < 10:
      minute = '0' + str(minute)
    return minute, second


clear = lambda: os.system('clear')