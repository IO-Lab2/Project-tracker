from logging import getLogger

logger = getLogger(__name__)

#tries to convert text to int
#text can by of any type
#returns None if it fails
def try_make_int(text):
    try:
        return int( text.strip() )
    except ValueError:
        logger.debug(f"try_make_int : could not convert str \"{text}\" to int") 
    except Exception:
        logger.debug(f"try_make_int : could not convert type {type(text).__name__} to int") 

    return None

#tries to convert text to float
#text can by of any type
#returns None if it fails
def try_make_float(text):
    try:
        fl_str = text.strip() #if text isn't str will raise TypeError
        fl_str = fl_str.replace(',', '')
        return float( fl_str )
    except ValueError:
        logger.debug(f"try_make_float : could not convert str \"{text}\" to float") 
    except Exception:
        logger.debug(f"try_make_float : could not convert type {type(text).__name__} to float") 

    return None
