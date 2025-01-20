from uuid import UUID
import re
import weakref

from constants import ACADEMIC_TITLES, ORGANIZATION_TYPES

def is_non_empty_str(obj):
    if not isinstance(obj, str):
        return False
    if not obj.strip():
        return False
    return True


def is_non_negative_int(obj):
    if not isinstance(obj, int):
        return False
    if not obj >= 0:
        return False
    return True

def is_non_negative_float(obj): 
    if not isinstance(obj, float):
        return False
    if not obj >= 0:
        return False
    return True

    
'''
def is_non_empty_uuid(obj):
    if not isinstance(obj, UUID):
        return False
    if not bool(obj):
        return False
    return True'''


    #can be used only on objects with length
def length_check(obj, max_len):
    return 0 < len(obj) <= max_len


#check if it points to an existing object
def validate_weak_ref(weak_ref):
    if not isinstance(weak_ref, weakref.ReferenceType):
        return False

    if not weak_ref():
        return False

    return True

def validate_uuid_str(uuid_str:str):
    if not is_non_empty_str(uuid_str):
        return False

    try:
        # Attempt to create a UUID object from the string
        uuid_obj = UUID(uuid_str)
        # Check if the UUID is the nil UUID
        if uuid_obj == UUID(int=0):
            return False

        return True
    except ValueError:
        # The string is not a valid UUID
        return False


    
#validates first name and following if present
#validates last name
def validate_name(name):
    if not is_non_empty_str(name):
        return False

    #pretty inclusive regex pattern for names
    pattern = re.compile(r"^[A-Za-ząćęłńóśżźĄĘŁŃÓŚŻŹàáâäãåāæçčďèéêëēėęíîïīįìľłńñòóôöõōøœśšñřśţúùüūųýÿžźż]+(?:[-' ][A-Za-ząćęłńóśżźĄĘŁŃÓŚŻŹàáâäãåāæçčďèéêëēėęíîïīįìľłńñòóôöõōøœśšñřśţúùüūųýÿžźż]+)*$")
    if not bool(pattern.match(name)):
        return False

    return True


def validate_academic_title(title):
    if not is_non_empty_str(title):
        return False

    if title not in ACADEMIC_TITLES:
        return False

    return True


#uses organization types accepted by the database
def validate_organization_type(org_type):
    if not is_non_empty_str(org_type):
        return False
    
    if org_type not in ORGANIZATION_TYPES:
        return False
    
    return True


def validate_publication_year(year):
    if not isinstance(year, int):
        return False

    if not (1900 < year < 2050):
        return False

    return True


def validate_email(email):
    if not is_non_empty_str(email):
        return False

    #regex pattern for validating an email
    regex = r'^[a-zA-Z0-9]+([._][a-zA-Z0-9]+)*@[a-zA-Z0-9]+(\.[a-zA-Z]{2,})+$'
    if not re.search(regex, email): 
        return False 
        
    return True


def validate_url(url):
    if not is_non_empty_str(url):
        return False
        
    #regex pattern for validating urls
    regex = re.compile( 
        r'^https://bazawiedzy\.pb\.edu\.pl' # https and domain 
        r'(?:/?|[/?]\S+)$', re.IGNORECASE # path
    )
    if not re.match(regex, url):
        return False

    return True


#univarsal validation function
def validate_obj(obj, *validation_funcs, process_independently=False):
    """
    Validates the object passed using validation functions
    supports passing additional arguments to validation functions.

    Parameters:
    obj (any): The object to validate.
    validation_funcs (at least one function or tuple): validation functions
                                                       Each function can be provided as a tuple with additional args/kwargs.
                                                       Each function should take the value to validate as the first argument and return a boolean.
    process_independently (bool): if set to True, it will iterate over obj and treat each element separately
                                     - only to be used with iterables

    Returns:
    bool: True if all validations pass, False otherwise.
    list of bools: if process_independently == True

    Raises:
    ValueError: if no validation functions are provided
    TypeError: if obj is not an iterable but process_independently == True
    """
    if not validation_funcs:
        raise ValueError("validate_value: no validation functions were provided")

    def validate_singular(value):
        for validation_func in validation_funcs:
            if isinstance(validation_func, tuple):
                func, *func_args = validation_func
                if not func(value, *func_args):
                    return False
            else:
                if not validation_func(value):
                    return False
        return True

    if process_independently:
        result = []
        for singular in obj:
            result.append( validate_singular(singular) )
        return result
    else:
        if not validate_singular(obj):
            return False

    return True
