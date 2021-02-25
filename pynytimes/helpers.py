def raise_instance(variable, variable_name, types):
    if not isinstance(variable, types):
        readable_types = ""
        
        if isinstance(type, tuple):
            for i, _type in enumerate(list(types)):
                if i != 0:
                    readable_types += ", "
                readable_types += _type.__name__

        else:
            readable_types = types.__name__

        raise TypeError(f"{variable_name} needs to be {str(readable_types)}")