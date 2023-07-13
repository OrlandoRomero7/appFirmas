def validate_name_input(value_if_allowed):
    if len(value_if_allowed) <= 26 and all(c.isalpha() or c.isspace() or c == '.' for c in value_if_allowed):
        return True
    else:
        return False

def validate_position_input(value_if_allowed):
    if len(value_if_allowed) <= 29 and all(c.isalpha() or c.isspace() for c in value_if_allowed):
        return True
    else:
        return False
    
def validate_ext_input(value_if_allowed):
    if value_if_allowed == "":
        return True
    elif value_if_allowed.isdigit() and len(value_if_allowed) <= 3:
        return True
    else:
        return False

def validate_email_input(value_if_allowed):
    allowed_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._@')
    if set(value_if_allowed).issubset(allowed_chars):
        return True
    else:
        return False



def validate_cellphone_input(value_if_allowed):
    if value_if_allowed == "":
        return True
    elif value_if_allowed.isdigit() and len(value_if_allowed) <= 10:
        return True
    else:
        return False