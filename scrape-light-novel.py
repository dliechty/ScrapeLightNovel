#!/usr/bin/python

import urllib.request
from bs4 import BeautifulSoup
import argparse
import logging
import platform
import subprocess
import unidecode
import re
from shutil import move

DEFAULT_START_URL = 'http://totobro.com/shen-yin-wang-zuo-chapter-1/'
DEFAULT_LOG_FILE = 'log.txt'
DEFAULT_TITLE = 'Shen Yin Wang Zuo'

FILE_HEADER = ('<!DOCTYPE html>\n<html>\n<head>'
               '\n<title>' + DEFAULT_TITLE +
               '</title>\n</head>\n<body>\n###TOC###')

FILE_FOOTER = '</body>\n</html>'

BAD_STRINGS = ['Previous Chapter.*', 'Next Chapter.*']

LOGGING_FORMAT = '%(asctime)-15s %(levelname)s %(message)s'

LOG_LEVEL = logging.INFO

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

argParser.add_argument('-t', '--title',
                       help='Title and base name of output file',
                       default=DEFAULT_TITLE)
argParser.add_argument('-s', '--site',
                       help='URL of first chapter to scrape.',
                       default=DEFAULT_START_URL)
argParser.add_argument('-l', '--log', help='Log file',
                       default=DEFAULT_LOG_FILE)


def main():
    args = argParser.parse_args()

    logging.basicConfig(filename=get_path(args.log),
                        level=LOG_LEVEL, format=LOGGING_FORMAT, filemode='a')

    url = args.site

    logging.info('Writing to output file: [%s]', args.title)

    counter = 0

    with open(args.title, 'w', encoding='utf-8') as writer:

        writer.write(FILE_HEADER)

        chapters = []

        while True:
            counter += 1

            logging.debug('Retrieving URL: [%s]', url)
            req = urllib.request.Request(url, headers=headers)
            html = urllib.request.urlopen(req)
            bs_obj = BeautifulSoup(html.read(), 'html5lib')
            entry = bs_obj.find('div', {'class': 'entry-content'})

            text_list = [' '.join(ch.stripped_strings)
                         for ch in entry if hasattr(ch, 'stripped_strings')]

            text_list = [unidecode.unidecode(s) for s in text_list]

            for i in range(0, len(text_list)):
                for pattern in BAD_STRINGS:
                    if re.match(pattern, text_list[i]):
                        text_list[i] = ''

                preview = False
                if re.match('.*Chapter \d{1,}.*', text_list[i]):
                    if text_list[i - 1] == 'Preview:':
                        text_list[i - 1] = ''
                        preview = True

                    clean_chapter = re.sub(r'(.*)(Chapter \d{1,}.*)',
                                           r'\2', text_list[i])
                    text_list[i] = ('\n\n<h1 id="ch' + str(counter) + '">' +
                                    ('Preview: ' if preview else '') +
                                    clean_chapter + '</h1>')

                    chapters.append(('ch' + str(counter), clean_chapter))

                if re.match('1\.', text_list[i]):
                    text_list[i] = '\n' + text_list[i]

            text_list = [('<p>' + s + '</p>' if
                          not s.startswith('\n\n<h1>Chapter') else s)
                         for s in text_list if s]

            text = '\n'.join(text_list)

            text += '\n<div class="pagebreak"></div>'

            writer.write(text)

            if counter % 25 == 0:
                logging.info('Done with [%i] chapters.', counter)

            next_chapter = bs_obj.find('a', href=True, text='Next Chapter')
            if next_chapter:
                url = next_chapter['href']
            else:
                break

        writer.write(FILE_FOOTER)

        writer.write(build_toc(chapters))
        logging.info('Done scraping. Grabbed [%s] chapters.', counter)

    logging.info('Renaming file [%s] to [%s].',
                 args.title, args.title + '_' + str(counter) + '.html')
    move(args.title, args.title + '_' + str(counter) + '.html')


def get_path(path):
    """Convert path to cygwin format if running on a cygwin platform"""

    if 'CYGWIN' in platform.system():
        path = subprocess.getoutput('cygpath ' + path)
    return path


def build_toc(chapters):
    boiler_top = '<div id="toc">\n<h2>\nTable of Contents <br />\n</h2>\n<ul>\n'
    boiler_bot = '</ul>\n</div>\n<div class="pagebreak"></div>'

    toc = boiler_top

    for link, text in chapters:
        toc += '<li><a href="#' + link + '">' + text + '</a></li>\n'

    toc += boiler_bot
    return toc


if __name__ == '__main__':
    main()
