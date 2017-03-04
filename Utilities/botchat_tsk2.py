import time, requests, json


def req(link): # function to retrieve json data from the stack overflow API
    data = requests.get(link)
    dic = json.loads(data.text)
    answers = dic['items']
    results = []
    if answers:
        for answer in answers:
            if answer['is_answered']:
                results.append(answer)
    formatted_list = []
    varr = ""
    if len(results) > 4:
        for i in range(0, 5, 1):
            formatted_list.append(str(results[i]['title']) + ', ' + str(results[i]['link']) + ', ' + str(
                results[i]['answer_count']) + ' responses' + ', ' + time.ctime(
                results[i]['creation_date']) + '\n\n')
            varr += formatted_list[i]
    else:
        for i in range(0, len(results), 1):
            formatted_list.append(str(results[i]['title']) + ', ' + str(results[i]['link']) + ', ' + str(
                results[i]['answer_count']) + ' responses' + ', ' + time.ctime(
                results[i]['creation_date']) + '\n\n')
            varr += formatted_list[i]
    return varr

text = '<I_NEED_HELP_WITH_CODING>: how to find duplicates in a list python'
query = text.split(':')[1].strip()
url = 'https://api.stackexchange.com/2.2/search/advanced?order=desc&sort=votes&q=' + query + '&site=stackoverflow'
my_string = req(url)


# url = 'https://api.stackexchange.com/2.2/search/advanced?order=desc&sort=votes&q=' + query + '&site=stackoverflow'
2+2