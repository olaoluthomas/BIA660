import requests
r = requests.get("http://api.github.com/users/olaoluthomas/repos")
json = r.text
2+2