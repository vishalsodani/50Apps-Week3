import requests
from BeautifulSoup import BeautifulSoup, Comment
import re



IGNORE_WORD_LIST = ['a', 'an', 'the', 'on', 'in', 'for', 'and','to','it','of']
MAX_WORD_LIST = 10


def parse(url):
    web_page = requests.get(url)
    webpage_content = BeautifulSoup(web_page.content)
    
    
    map(lambda tag: tag.extract(),webpage_content.findAll({'script':True}))
    map(lambda tag: tag.extract(),webpage_content.findAll(text=lambda x: isinstance(x, Comment)))

    
    all_tags = webpage_content.findAll(text=True)
    content =  map(lambda x: x,all_tags)
    content = " ".join(content)
    content = re.sub(r'&.+;','',content)
    content = re.sub(r'\r\n|\n|\\|/',' ',content)

    #return result_list
    potential_words = filter (lambda x:re.match("^[a-zA-Z]+$",x),[x for x in re.split("[\s:/,.:]",content)])
    potential_words = filter(lambda x: x not in IGNORE_WORD_LIST,potential_words)
    potential_words = map(lambda x : x.lower(),potential_words)

    result = dict([(x, potential_words.count(x)) for x in potential_words])

    # covert into set so unique counts
    result_occurence = set([potential_words.count(x) for x in potential_words])
    # find legnth of set
    len_set = len(result_occurence)
    #convert into list and find the last element which gives the max occurence of a word
    result_list = list(result_occurence)
    max_ocuurence = result_list[len_set -1]

    # now go though each element in dictionary which is equal to max_ocuurence, reverse till 1, max words to pick is 10
    result_list = {}
    fetch_words_with_max_occurence(result, max_ocuurence, result_list)

    return result_list    

def fetch_words_with_max_occurence(result, max_ocuurence,result_list):
    
    if len(result_list) == MAX_WORD_LIST:
        return

    for k,v in result.iteritems():
        if v == max_ocuurence:
            result_list[k] = v
            if len(result_list) == MAX_WORD_LIST:
                return
            
            
    fetch_words_with_max_occurence(result, max_ocuurence - 1,result_list)
