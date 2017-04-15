import json, requests, time, random


delay = random.uniform(0, 10)
time.sleep(delay)
text = "<WHAT'S_THE_WEATHER_LIKE_AT?>: 11211"
string = text.split(":")
location = string[1].strip()
w_url = ''
if int(location):
    w_url = 'http://api.openweathermap.org/data/2.5/weather?zip=' + location + ',us&APPID=a295d9b1395bfe5bc776408b9cb2e3f8'
else:
    w_url = 'http://api.openweathermap.org/data/2.5/weather?q=' + location + '&APPID=a295d9b1395bfe5bc776408b9cb2e3f8'

data = requests.get(w_url)
w_son = json.loads(data.text)
if w_son:
    nam = str(w_son['name'])
    con = str(w_son['sys']['country'])
    wth = str(w_son['weather'][0]['description'])
    tp = str(w_son['main']['temp'] - 273.15) + " C"
    high = str(w_son['main']['temp_max'] - 273.15) + " C"
    low = str(w_son['main']['temp_min'] - 273.15) + " C"
    wind = str(w_son['wind']['speed']) + " mph"

    answer = "It's " + tp + " in " + nam + ", " + con + " with " + wth + ".\nThe expected extremes for today are " + high + " and " + low + ".\nWinds of " + wind + "\n\n(Waited for {}s before responding)".format(delay)

2+2
