from functools import wraps
from logging import getLogger

from knowledge_scraper.items import ScientistItem, PublicationItem, BibliometricsItem, OrganizationItem
from utils.misc import get_by_keys, process_based_on_type, add_parenthesis
from utils.basic_validation import validate_weak_ref

logger = getLogger(__name__)

def item_type_based_processing(func):
    '''
    based on an item's type extracts and passes some of its fiels as kwargs

    for ScientistItem:
        formats 'name' using 'academic_title', 'first_name' and 'last_name'
        passes 'profile_url'
        "name" and "profile_url" can no longer be used as keyword in **kwargs

    for PublicationItem:
        passes "title"
        passes "scientist_id"
        "title" and "scientist_id" can no longer be used as keywords in **kwargs

    for BibliometricsItem:
        passes "scientist_id"
        "scientist_id" can no longer be used as a keyword in **kwargs

    for OrganizationItem:
        passes "name"
        "name" can no longer be used as a keyword in **kwargs
    '''


    #main body of the decorator
    @wraps(func)
    def wrapper(*args, **kwargs):

        #handlers

        #formats name using 'academic_title', 'first_name' and 'last_name' - all present need to be strings
        #passes profile_url
        #returns a dict
        def get_extra_scientist(sc):
            extra = dict()

            keys = ["academic_title", 'first_name', 'last_name']
            name_parts = get_by_keys(sc, keys)
            name = " ".join( name_parts.values() )
            if name:
                extra["name"] = name
        
            url = sc.get("profile_url")
            if url:
                extra["profile_url"] = url

            return extra
        #end of get_extra_scientist

        def get_extra_bibliometrics(bibl):
            sc_ref = bibl.get("scientist_ref")
            if validate_weak_ref(sc_ref):
                sc = sc_ref()
                if isinstance(sc, ScientistItem):
                    return get_extra_scientist( sc )

            logger.error("get_item_msg - item_type_based_processing - get_exta_bibliometrics: BibliometricsItem does not have a valid ScientistItem reference")
            return {"scientist_ref" : "invalid"}
        #end of get_extra_bibliometrics

        #get_extra_bibliometrics = lambda bibl: get_by_keys(bibl, "scientist_id")
        get_extra_publication = lambda p: get_by_keys(p, ["title", "scientist_id"])
        get_extra_organization = lambda org: get_by_keys(org, "name")

        # assigning a function that extracts information from items and returns it as a dictionary
        handlers = {
            ScientistItem : get_extra_scientist,
            PublicationItem : get_extra_publication,
            BibliometricsItem : get_extra_bibliometrics,
            OrganizationItem : get_extra_organization
        }

        item = find_item( handlers.keys(), args, kwargs )
        if not item:
            # item does not have a handler
            return func(*args, **kwargs)

        extra =  process_based_on_type(item, handlers)
        return func(*args, **extra, **kwargs)
    #end of wrapper


    def find_item( types, args, kwargs ):
        '''
        searches for an item that is of type from types
        first checks for "item" in kwargs 
        then checks args

        types: list of types of interest
        args: list of args
        kwargs: dict of kwargs

        returns: the first item found
                 None if no type was matched
        '''
        # checking for item in kwargs
        if "item" in kwargs:
            item = kwargs["item"]
            if type(item) in types:
                return item

        # checking args
        for arg in args:
            if type(arg) in types:
                return arg

        return None
    #end of find_item


    return wrapper
#end of item_type_based_processing

@item_type_based_processing
def get_item_msg(event:str, item, description=None, *, add_identifier=False, **kwargs) -> str:
    '''
    for logging
    event: string specyfying what is happening
    description: optional str specyfing why event is happening
        example event="Stopped parsing item", description="item lacks name"
    item: item for identification
    add_identifier: boolean indicating whether 'identifier' from item should be added to the msg
    kwargs: things that you want to add to further identify item (accepts None as a value for a key)
        example url="www.example.com" will result in 'url: "www.example.com";' added at the end of a msg

    uses:
    type(item) 
    item['identifier'] if an item has 'identifier' and it is not None

    returns formatted str message
    '''
    item_type = type(item).__name__
    msg = f'{event} - {item_type}'
    if description is not None:
        msg += ' - ' + description

    #return message-formated key and value
    def format_extra(key:str, value): 
        v_text = add_parenthesis(value)
        return f" {key}: {v_text};"
    #end of format_extra

    extra_identifiers = []

    if add_identifier:
        identifier = item.get('identifier')
        if identifier:
            extra_identifiers.append( format_extra('identifier', identifier) )

    for key in kwargs:
        extra_identifiers.append(  format_extra(key, kwargs.get(key)) )

    if extra_identifiers:
        msg += " ->"
    for extra in extra_identifiers:
        msg += extra

    return msg

#returns "Invalid key: item[key]" string
#accepts None values as well as keys without values
def get_invalid_value_msg(item, key):
    v_text = add_parenthesis( item.get(key) )
    return f"Invalid {key}: {v_text}."
