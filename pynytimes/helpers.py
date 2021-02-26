from datetime import datetime
import re

try:
    import orjson
except ImportError:
    orjson = None

def raise_instance(variable, variable_name, types):
    """Raise if not correct instance"""
    if not isinstance(variable, types):
        readable_types = ""
        
        if isinstance(types, tuple):
            for i, _type in enumerate(types):
                if i != 0:
                    readable_types += ", "
                readable_types += _type.__name__

        else:
            readable_types = types.__name__

        error_message = f"{variable_name} needs to be {readable_types}"

        raise TypeError(error_message)

def parse_json(res):
    """Parse JSON using orjson if possible"""
    if orjson is None:
        return res.json()
    else:
        return orjson.loads(res.content)

def raise_for_status(res):
    """Raise error for invalid status"""
    if res.status_code == 400: 
            raise ValueError("Error 400: Invalid input")
    elif res.status_code == 401: 
        raise ValueError("Invalid API Key")
    elif res.status_code == 404: 
        raise RuntimeError("Error 404: This page is not available")

    res.raise_for_status()

def parse_date(date_string, date_type):
    """Parse date_string into datetime.datetime or datetime.date object"""
    date = datetime.datetime.now()

    # If date_string is None return None
    if date_string is None:
        return None

    # Parse rfc3339 dates from string
    elif date_type == "rfc3339":
        # Fix for Python 3.6, can be removed when support is dropped
        if date_string[-3] == ":":
            date_string = date_string[:-3] + date_string[-2:]
        
        date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S%z")

    # Parse date only strings
    elif date_type == "date-only":
        year_only = re.match(r"^(\d){4}-00-00$", date_string)
        
        if year_only:
            date =  datetime.strptime(date_string, "%Y-00-00").date()
        else:
            date = datetime.strptime(date_string, "%Y-%m-%d").date()
                    
    elif date_type == "date-time":
        date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")

    return date