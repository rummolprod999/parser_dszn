import re
import urllib.parse
import urllib.request

import lxml.html
import timeout_decorator

export_text = 'organizations.txt'
start_url = 'https://dszn.ru/department/subordinate'
def main():
    get_page(start_url)

def get_page(url):
    page = download_page(url)
    extract_links(page)
    print(page)



@timeout_decorator.timeout(35)
def download_page(url):
    req = urllib.request.Request(url=url)
    handler = urllib.request.urlopen(req, timeout=30)
    page = handler.read().decode('utf-8')
    return page

def extract_links(page):
    pass