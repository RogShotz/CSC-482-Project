import requests
import json
import re

text = 'Abraham Lincoln'
api_url = 'https://api.api-ninjas.com/v1/historicalevents?text={}'.format(text)

def brandon_bot(irc, msg, sender, channel):
    if re.search('when was [a-zA-Z ]+ born\?', msg):
        print("Matched with brandon_bot")
    # if msg == 'example':
    #     irc.send(
    #             channel, f"{sender}: example bot q/a")
    #     pass
    # #TODO: call query()
    print("Called brandon_bot()")
    return

def query():
    response = requests.get(api_url, headers={'X-Api-Key': 'c6mubGVsRHZzPTs1FvREDQ==rKAIsRLjFmd5a5LW'})
    if response.status_code == requests.codes.ok:
        json_obj = json.loads(response.text)
        print(json.dumps(json_obj, indent=4))
    else:
        print("Error:", response.status_code, response.text)


if __name__ == "__main__":
    query()