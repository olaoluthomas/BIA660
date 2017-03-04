import os
import json
import requests

from flask import Flask, request, Response
from textblob import TextBlob


app = Flask(__name__)

# FILL THESE IN WITH YOUR INFO
my_bot_name = 'slickbot' #e.g. zac_bot
my_slack_username = 'simeonthomas' #e.g. zac.wentzell

# main URL
slack_inbound_url = 'https://hooks.slack.com/services/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'
# test inbound URL
# slack_inbound_url = 'https://hooks.slack.com/services/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'


# this handles POST requests sent to your server at SERVERIP:41953/slack
@app.route('/slack', methods=['POST'])
def inbound():
    print '========POST REQUEST @ /slack========='
    response = {'username': my_bot_name, 'icon_emoji': ':squirrel:', 'text': ''}
    print 'FORM DATA RECEIVED IS:'
    print request.form

    channel = request.form.get('channel_name') # this is the channel name where the message was sent from
    username = request.form.get('user_name') # this is the username of the person who sent the message
    text = request.form.get('text') # this is the text of the message that was sent
    inbound_message = username + " in " + channel + " says: " + text
    print '\n\nMessage:\n' + inbound_message

    if username in [my_slack_username, 'zac.wentzell']:
        # Your code for the assignment must stay within this if statement
        response['text'] = 'Hi, ' + username

        # A sample response:
        if text == "What's your favorite color?":
            # You can use print statments to debug your code
            print 'Bot is responding to favorite color question'
            response['text'] = 'Blue!'
            print 'Response set correctly'


    if slack_inbound_url and response['text']:
        r = requests.post(slack_inbound_url, json=response)

    print '========REQUEST HANDLING COMPLETE========\n\n'

    return Response(), 200


# this handles GET requests sent to your server at SERVERIP:41953/
@app.route('/', methods=['GET'])
def test():
    return Response('Your flask app is running!')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=41953)

'''elif text.startswith("&lt;WHAT'S_THE_WEATHER_LIKE_AT&gt;:"):
    print 'Bot is responding to Task 4'
    texts = text.split(':')
    response['text'] = 'Searching weather information for ' + texts[1] + "Please wait..."
    print 'Response set correctly'

    r = requests.post(slack_inbound_url, json=response)

elif text in ['Hello','Hi','Hey',"What's up",'Yo','hello','hi', 'hey','yo']:
    print 'Bot is responding to salutation'
    response['text'] = 'Hi, ' + username
    print 'Response set correctly'

    r = requests.post(slack_inbound_url, json=response)'''