# -*- coding: utf-8 -*-
import requests, json

text = "<WHAT'S_THE_WEATHER_LIKE_AT?>: Newark"
if text.startswith("<WHAT"):
    string = text.split(":")
    location = string[1].strip()
    if str(location):
        w_url = 'http://api.openweathermap.org/data/2.5/weather?q='+location+'&APPID=a295d9b1395bfe5bc776408b9cb2e3f8'
    elif int(location):
        w_url = 'http://api.openweathermap.org/data/2.5/weather?zip='+location+',us&APPID=a295d9b1395bfe5bc776408b9cb2e3f8'

data = requests.get(w_url)
w_son = json.loads(data.text)
wth = str(w_son['weather'][0]['description'])
tmp = str(w_son['main']['temp'] - 273.15)+" °C"
high = str(w_son['main']['temp_max'] - 273.15)+" °C"
low = str(w_son['main']['temp_min'] - 273.15)+" °C"
wind = str(w_son['wind']['speed'])+" mph"
gust = str(w_son['wind']['gust'])+" mph"

forecast = "It's "+tmp+" with "+wth+".\nThe expected extremes for today are "+high+" and "+low+".\nWinds of "+wind+" and gusts of "+gust+". "

2+2
