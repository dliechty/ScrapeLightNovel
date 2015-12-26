#!/usr/bin/python

import urllib.request
from bs4 import BeautifulSoup
import argparse
import logging
import platform
import subprocess

DEFAULT_START_URL = 'http://totobro.com/shen-yin-wang-zuo-chapter-1/'
DEFAULT_OUTPUT_FILE = 'out.txt'
DEFAULT_LOG_FILE = 'log.txt'

LOGGING_FORMAT = '%(asctime)-15s %(levelname)s %(message)s'

LOG_LEVEL = logging.DEBUG

# spoof some headers so the request appears to be coming
# from a browser, not a bot
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
}

# Set up command line arguments
argParser = argparse.ArgumentParser(description='Scrape all blog content '
                                    'from long-running posts separate by '
                                    'chapters.')

argParser.add_argument('-o', '--outputfile', help='Output File',
                       default=DEFAULT_OUTPUT_FILE)
argParser.add_argument('-s', '--site',
                       help='URL of first chapter to scrape.',
                       default=DEFAULT_START_URL)
argParser.add_argument('-l', '--log', help='Log file',
                       default=DEFAULT_LOG_FILE)


def main():

    args = argParser.parse_args()

    logging.basicConfig(filename=getPath(args.log),
                        level=LOG_LEVEL, format=LOGGING_FORMAT, filemode='a')

    url = args.site

    logging.info('Writing to output file: [%s]', args.outputfile)

    with open(args.outputfile, 'w', encoding='utf-8') as writer:

        counter = 0

        while True:
            logging.debug('Retrieving URL: [%s]', url)
            req = urllib.request.Request(url, headers=headers)
            html = urllib.request.urlopen(req)
            bsObj = BeautifulSoup(html.read(), 'html5lib')
            entry = bsObj.find('div', {'class': 'entry-content'})

            writer.write(str(entry))

            counter += 1
            if counter % 25 == 0:
                logging.info('Done with [%i] chapters.', counter)

            nextChapter = bsObj.find('a', href=True, text='Next Chapter')
            if nextChapter:
                url = nextChapter['href']
            else:
                break


def getPath(path):
    '''Convert path to cygwin format if running on a cygwin platform'''

    if 'CYGWIN' in platform.system():
        path = subprocess.getoutput('cygpath ' + path)
    return path

if __name__ == '__main__':
    main()
