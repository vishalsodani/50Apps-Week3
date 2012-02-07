import requests
from BeautifulSoup import BeautifulSoup
import re


IGNORE_WORD_LIST = ['a', 'an', 'the', 'on', 'in', 'for', 'and','to']

def parse(url):
    web_page = requests.get(url)
    webpage_content = BeautifulSoup(web_page.content)
    content = ''
    for i in webpage_content.body:
        if i.string:
            content += i.string
    
    
    #p = re.compile(r"\b[a-z]+\b")
    
    potential_words = filter (lambda x:re.match("^[a-zA-Z]+$",x),[x for x in re.split("[\s:/,.:]",content)])
    potential_words = filter(lambda x: x not in IGNORE_WORD_LIST,potential_words)

    result = dict([(x, potential_words.count(x)) for x in potential_words])
    return result
    
