#!/usr/bin/python

import urllib.request
from bs4 import BeautifulSoup

# spoof some headers so the request appears to be coming
# from a browser, not a bot
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
}

with open('out.txt', 'w', encoding='utf-8') as writer:

    url = 'http://totobro.com/shen-yin-wang-zuo-chapter-1/'

    while True:
        req = urllib.request.Request(url, headers=headers)
        html = urllib.request.urlopen(req)
        bsObj = BeautifulSoup(html.read(), 'html5lib')
        entry = bsObj.find('div', {'class': 'entry-content'})

        writer.write(str(entry))

        nextChapter = bsObj.find('a', href=True, text='Next Chapter')
        if nextChapter:
            url = nextChapter['href']
        else:
            break
