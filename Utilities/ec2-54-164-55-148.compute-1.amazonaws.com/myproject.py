import os, json, requests, random, time

from flask import Flask, request, Response

application = Flask(__name__)

# FILL THESE IN WITH YOUR INFO
my_bot_name = 'slickbot' #e.g. zac_bot
my_slack_username = 'simeonthomas'#e.g. zac.wentzell

# main URL
slack_inbound_url = 'https://hooks.slack.com/services/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'
# test inbound URL
#slack_inbound_url = 'https://hooks.slack.com/services/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'


# this handles POST requests sent to your server at SERVERIP:41953/slack
@application.route('/slack', methods=['POST'])
def inbound():
    # Adding a delay so that all bots don't answer at once (could overload the API).
    # This will randomly choose a value between 0 and 10 using a uniform distribution.
    delay = random.uniform(0, 10)
    time.sleep(delay)
    print '========POST REQUEST @ /slack========='
    response = {'username': my_bot_name, 'icon_emoji': ':squirrel:', 'text': ''}
    print 'FORM DATA RECEIVED IS:'
    print request.form

    channel = request.form.get('channel_name') # this is the channel name where the message was sent from
    username = request.form.get('user_name') # this is the username of the person who sent the message
    text = request.form.get('text') # this is the text of the message that was sent
    inbound_message = username + " in " + channel + " says: " + text
    print '\n\nMessage:\n' + inbound_message

    # This function takes a Stack Overflow link as input and spits out response['text']
    def req_overflow(link):
        data = requests.get(link)
        dic = json.loads(data.text)
        answers = dic['items']
        results = []
        if answers:
            for answer in answers:
                if answer['is_answered']:
                    results.append(answer)
        answer_lst = []
        if len(results) > 4:  # we're returning 5 questions
            for i in range(0, 5, 1):
                answer_lst.append(
                    str(results[i]['title']) + ", " + "<" + str(results[i]['link']) + "|Link>" + ", " + str(
                        results[i]['answer_count'])+ " response(s)" + ", " + time.ctime(results[i]['creation_date']))
        else:
            for i in range(0, len(results), 1):  # we're returning as many questions as possible
                answer_lst.append(
                    str(results[i]['title']) + ", " + "<" + str(results[i]['link']) + "|Link>" + ", " + str(
                        results[i]['answer_count'])+ " response(s)" + ", " + time.ctime(results[i]['creation_date']))
        ansr_strng = "\n".join(item for item in answer_lst)
        return ansr_strng

    if username in [my_slack_username, 'zac.wentzell']:
        if '&lt;I_NEED_HELP_WITH_CODING&gt;:' and '[' in text:
            print 'Bot is responding to Task 3'
            drop = text.split(":")
            query = drop[1]
            query = query.replace(" [", ".").replace("] ", ".").replace("[",".").replace("]",".").strip().split(".")
            for item in query:
                if not bool(item):
                    query.remove(item)
            question = query[0]
            tags = query[1:]
            tagged = tags[0]
            for i in range(1, len(tags), 1):
                tagged += ";"+tags[i] # this loop can be replaced by ";".join(list)
            url = 'https://api.stackexchange.com/2.2/search/advanced?order=desc&sort=votes&q='+question+'&tagged='+tagged+'&site=stackoverflow'
            # Now, we call the function req which will take a url as input and spit out a dictionary of lists
            my_string = req_overflow(url)
            if my_string:
                response['text'] = "Here are some useful results to try:\n\n"+ my_string +"\n\n(Waited for {}s before responding)".format(delay)
            else:
                response['text'] = "I'm sorry, your search returned 0 results.\n\n(Waited for {}s before responding)".format(delay)

            r = requests.post(slack_inbound_url, json=response)
            print 'Response set correctly'

        elif text.startswith('&lt;I_NEED_HELP_WITH_CODING&gt;:'):
            print 'Bot is responding to Task 2'
            query = text.split(':')[1].strip()
            url = 'https://api.stackexchange.com/2.2/search/advanced?order=desc&sort=votes&q=' + query + '&site=stackoverflow'
            my_string = req_overflow(url)
            if my_string:
                response['text'] = "Here are some useful results to try:\n\n" + my_string +"\n\n(Waited for {}s before responding)".format(delay)
            else:
                response['text'] = "I'm sorry, your search returned 0 results.\n\n(Waited for {}s before responding)".format(delay)

            r = requests.post(slack_inbound_url, json=response)
            print 'Response set correctly'

        elif text.startswith("&lt;WHAT'S_THE_WEATHER"):
            print 'Bot is responding to Task 4'
            string = text.split(":")
            location = string[1].strip()
            w_url = ''
            if str(location):
                w_url = 'http://api.openweathermap.org/data/2.5/weather?q='+location+'&APPID=a295d9b1395bfe5bc776408b9cb2e3f8'
            elif int(location):
                w_url = 'http://api.openweathermap.org/data/2.5/weather?zip='+location+',us&APPID=a295d9b1395bfe5bc776408b9cb2e3f8'

            data = requests.get(w_url)
            w_son = json.loads(data.text)
            if w_son:
                nam = str(w_son['name'])
                con = str(w_son['sys']['country'])
                wth = str(w_son['weather'][0]['description'])
                tmp = str(w_son['main']['temp'] - 273.15)+" C"
                high = str(w_son['main']['temp_max'] - 273.15)+" C"
                low = str(w_son['main']['temp_min'] - 273.15)+" C"
                wind = str(w_son['wind']['speed'])+" mph"
                response['text'] = "It's "+tmp+" in "+nam+", "+con+" with "+wth+".\nThe expected extremes for today are "+high+" and "+low+".\n\nWinds of "+wind+"\n(Waited for {}s before responding)".format(delay)
            else:
                response['text'] = "Cannot interpret.\nPlease provide an actionable location\n\n(Waited for {}s before responding)".format(delay)
            r = requests.post(slack_inbound_url, json=response)
            print 'Response set correctly'

        elif text == '&lt;BOTS_RESPOND&gt;':
            print 'Bot is responding to Task 1'
            response['text'] = "I'm " + my_bot_name + " and I belong to " + my_slack_username + ". I live at 54.164.55.148.\n\n(Waited for {}s before responding)".format(delay)
            r = requests.post(slack_inbound_url, json=response)
            print 'Response set correctly'

        else:
            print "Bot doesn't know how to handle this"
            response['text'] = '''I didn't get that...
            I handle queries that start with &lt;I_NEED_HELP_WITH_CODING&gt;:
            or &lt;WHAT'S_THE_WEATHER_LIKE_AT&gt;: <city>
            Give it another go!'''
            r = requests.post(slack_inbound_url, json=response)
            print 'Response set correctly'

    print '========REQUEST HANDLING COMPLETE========\n\n'

    return Response(), 200


# this handles GET requests sent to your server at SERVERIP:41953/
@application.route('/', methods=['GET'])
def test():
    return Response('Your flask app is running!')


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=41953)