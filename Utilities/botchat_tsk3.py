import requests, json, time

text = "<I_NEED_HELP_WITH_CODING>: python magic methods [python]"
drop = text.split(":")
query = drop[1]
query = query.replace(" [", ".").replace("] ", ".").replace("[", ".").replace("]", ".").strip().split(".")
for item in query:
    if not bool(item):
        query.remove(item)
question = query[0]
tags = query[1:]
tagged = tags[0]
for i in range(1, len(tags), 1):
    tagged += ";" + tags[i]  # this loop can be replaced by ";".join(list)
url = 'https://api.stackexchange.com/2.2/search/advanced?order=desc&sort=votes&q=' + question + '&tagged=' + tagged + '&site=stackoverflow'


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
            answer_lst.append(str(results[i]['title']) + ", " + "<" + str(results[i]['link']) + "|Link>" + ", " + str(
                results[i]['answer_count']) + ", " + time.ctime(results[i]['creation_date']))
    else:
        for i in range(0, len(results), 1):  # we're returning as many questions as possible
            answer_lst.append(str(results[i]['title']) + ", " + "<" + str(results[i]['link']) + "|Link>" + ", " + str(
                results[i]['answer_count']) + ", " + time.ctime(results[i]['creation_date']))
    ansr_strng = "\n".join(item for item in answer_lst)
    return ansr_strng

spin = req_overflow(url)

2 + 2
