import requests
from BeautifulSoup import BeautifulSoup
import re


IGNORE_WORD_LIST = ['a', 'an', 'the', 'on', 'in', 'for', 'and','to','it','of']
MAX_WORD_LIST = 10
RESULT_LIST = {}

def parse(url):
    web_page = requests.get(url)
    webpage_content = BeautifulSoup(web_page.content)
    all_tags = webpage_content.findAll(text=True)
    content = ''
    for i in all_tags:
        content += i
    
    potential_words = filter (lambda x:re.match("^[a-zA-Z]+$",x),[x for x in re.split("[\s:/,.:]",content)])
    potential_words = filter(lambda x: x not in IGNORE_WORD_LIST,potential_words)

    result = dict([(x, potential_words.count(x)) for x in potential_words])

    # covert into set so unique counts
    result_occurence = set([potential_words.count(x) for x in potential_words])
    # find legnth of set
    len_set = len(result_occurence)
    #convert into list and find the last element which gives the max occurence of a word
    result_list = list(result_occurence)
    max_ocuurence = result_list[len_set -1]

    # now go though each element in dictionary which is equal to max_ocuurence, reverse till 1, max words to pick is 10
    
    fetch_words_with_max_occurence(result, max_ocuurence)
    return RESULT_LIST

def fetch_words_with_max_occurence(result, max_ocuurence):
    
    if len(RESULT_LIST) == MAX_WORD_LIST:
        return

    for k,v in result.iteritems():
        if v == max_ocuurence:
            RESULT_LIST[k] = v
            if len(RESULT_LIST) == MAX_WORD_LIST:
                return
            
            
    fetch_words_with_max_occurence(result, max_ocuurence - 1)
