import re
import datetime
from json import load
from urllib.request import urlopen, Request

def get_subreddit_data(sr):
    url = 'http://www.reddit.com/r/{}.json?limit=250'.format(sr)
    return load(urlopen(Request(url, headers={'User-agent': 'your bot 0.1'})))

hash = {}
blackList = ["BOOM", "RIP", "MOON", "GO", "THE",
"BE", "WITH", "IPO", "GAY", "BEAR", "WSB", "IN", 
"TV", "DD", "PART", "VA", "ME", "TO", "YOU", 
"LIFE", "AM", "EST", "GANG", "CEO", "ALL", "FAQ"
"IRA", "YOLO", "FULL", "FBI", "CIA", "MOST", "IN",
"IM", "VS"]
date = datetime.datetime.now()
hourConv = date.hour
if (hourConv > 12):
    hourConv -= 12

#Used to determine which stock subreddit to read through
data = get_subreddit_data('wallstreetbets')


with open('WSB ' + str(date.month) + '-' + str(date.day) + ' ' + str(hourConv) + ':' + str(date.minute) + ' ' + str(date.strftime("%p")) + '.txt', 'w') as outfile:
    for post in data['data']['children']:
        title = post['data']['title']
        titleSplit = title.split()
        for x in titleSplit:
            if re.search("^[\"\'\-\$]*[A-Z]{2,4}[\.\!\,\?\;\:\-\"\']*$", x):
                ticker = re.findall("[A-Z]{2,4}", x)
                if ticker[0] not in blackList:
                    if ticker[0] in hash.keys():
                        newValue = hash.get(ticker[0]) + 1
                        hash.update({ticker[0]: newValue})
                    else:
                        hash[ticker[0]] = 1
    sortedTickers = sorted(hash.items(), key=lambda tup: tup[1], reverse=True)
    
    for x in sortedTickers:
        if x[1] != 1:
            print("Ticker: " + str(x[0]) + " Count: " + str(x[1]), file = outfile)
            # tr