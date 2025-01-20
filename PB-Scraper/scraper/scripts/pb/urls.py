from re import compile, escape
from uuid import UUID, uuid5
from logging import getLogger

from constants import NAMESPACE_BUT

logger = getLogger(__name__)

#allows you to pass a scrapy.http.Request in place of url
#in which case a request with constructed url will be returned
def request_support(func):
    def wrapper(request_or_url, new_page_num:int):
        if isinstance(request_or_url, str):
            return func(request_or_url, new_page_num)
        
        request = request_or_url
        url = func(request.url, new_page_num)
        return request.replace(url=url)
    #end of wrapper
    return wrapper


#replaces last occurence of 'pn=[number]' in url or appends one with a new number
@request_support
def change_page_number(url:str, new_page_num:int):
    #searching for '&pn=' followed by a number
    page_num_text = "&pn="
    pattern = compile(escape(page_num_text) + r'\d+')
    matches = list(pattern.finditer(url))
    
    page_num_text += str(new_page_num)

    if not matches:
        return url + page_num_text

    last_match = matches[-1] 
    start, end = last_match.span()
    return url[:start] + page_num_text + url[end:]



#returns BUT id from url or None if fails
#works with absolute and relative urls
#can be called with: specific profile urls, specific publication urls, specific organization urls
def get_but_id(url:str):
    try:
        id_and_noise = url.split('/')[-1]
        identifier = id_and_noise.split('?')[0]
    except IndexError:
        logger.error(f"get_but_id: provided url is not valid -> url: {url}")
        return None

    if not identifier.startswith("BUT"):
        if not identifier.startswith("WUT"): #university organization page specific
            logger.warning(f"get_but_id: could not find but id in provided url -> url: {add_parenthesis(url)}")
            return None

    return identifier


#extends get_but_id
#returns uuid as string
#return None if url is None or get_but_id fails
def get_id(url:str|None):
    if url is None:
        return None

    but_id = get_but_id(url)
    if not but_id:
        return None

    return str( uuid5(NAMESPACE_BUT, but_id) )

#removes everything after the first '?' character
#if not found returns the url provided
#do not use with urls with 'globalResultList'
def clean_but_url(url:str):
    parts = url.split('?')
    return parts[0]
