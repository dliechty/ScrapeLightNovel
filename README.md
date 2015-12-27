# Scrape Light Novel
This is a small Python script to scrape all chapters from a web-based light novel translation into one file. The goal is to convert the output into a format compatible with the amazon kindle reader, and automatically send the results to a specified kindle.

The expected usage is to specify the URL of the first chapter, and the scraper starts there and follows all 'Next Chapter' links until no more content is available. It then takes the resulting output and converts to a format compatible with the kindle.

NOTE: The project is in its early stages. Right now it ONLY supports a single site and doesn't convert to a kindle format. It simply outputs the main content to a text file.

Here is the usage text:

```
usage: scrape-light-novel.py [-h] [-t TITLE] [-s SITE] [-l LOG]

Scrape all blog content from long-running posts separate by chapters.

optional arguments:
  -h, --help            show this help message and exit
  -t TITLE, --title TITLE
                        Title and base name of output file
  -s SITE, --site SITE  URL of first chapter to scrape.
  -l LOG, --log LOG     Log file
```
