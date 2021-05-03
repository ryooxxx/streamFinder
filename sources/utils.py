

#import sources.consts as consts

from urllib import error
from googlesearch import search
import requests
import bs4
import re
import os
import sys
import importlib

from urllib.parse import unquote
import sources.consts as consts

def duckduckgo_this(keywords: str, max_results: int=15) -> set:
    url = 'https://duckduckgo.com/html/?q='

    url = url+keywords.replace(" ","+")

    res = requests.get(url, headers={"User-Agent":"curl"})
    doc = bs4.BeautifulSoup(res.text, 'html.parser')

    results = doc.find_all("a", class_="result__a")
    res = set()
    for result in results:
        res.add( unquote(result["href"].split("uddg=")[1].split("&rut=")[0] ) )

    return res

def google_this(what: str, row: int, n: int, offset: int=0, SafeSearch="off", lang="fr", tld="fr"):
    print(f"Searching for {what}")
    try:
        res = search(what, tld=tld, num=row, start=offset, stop=n, pause=5, lang=lang, safe=SafeSearch, extra_params={'filter': '0'})
    except error.HTTPError:
        print("Google cooldown... you need a to change your IP")
    return res


def is_not_garbage(url: str) -> bool:
    if any([True for element in consts.black_list_websites if element in url ]):
        return False
    return True


def get_external_urls(title:str) -> set:
    links = set()
    sys.path.insert(0, "sources/plugin")
    for file in os.listdir("sources/plugin"):
        if not re.match(r"^[a-zA-Z\d_]+\.py$", file):
            continue
        name = file[:-3]
        print(f"Running module {name}")
        module = importlib.import_module(name)
        links |= module.Movie().get_movie(title)
    sys.path.pop(0)
    return links


def url_threading(url: str) -> set:
    if url == "":
        return set()
    #print(f"requesting {url!s}")
    try:
        content = requests.get(url)
    except:
        return set()
    res = set()
    doc = bs4.BeautifulSoup(content.text, 'html.parser')
    ifr = doc.find_all("iframe")
    for iframe in ifr:
        for url in re.findall(consts.reg_url, iframe.__str__()):
            res.add(url)
    return res
