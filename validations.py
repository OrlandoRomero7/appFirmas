import re
#from gui import address_part1,address_part2,telefone
#Validaciones

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

""" def validate_email():
    email_regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,}$'
    email= email_field.get()
    if email and not re.search(email_regex, email):
        error_label.configure(text="Correo inválido")
    else:
        error_label.configure(text="") """

def validate_cellphone_input(value_if_allowed):
    if value_if_allowed == "":
        return True
    elif value_if_allowed.isdigit() and len(value_if_allowed) <= 10:
        return True
    else:
        return False
    



#-----------------------------------------------------------
#Formats
# ----------------------------------------------

def custom_title(s):
    no_capitalize = ["y", "e", "o", "u", "de"]
    words = s.split(' ')
    for i in range(len(words)):
        if words[i].lower() not in no_capitalize or i == 0:  # Convertimos la palabra a minúsculas antes de verificar
            words[i] = words[i].capitalize()
        else:
            words[i] = words[i].lower()  # Convertimos la palabra a minúsculas si está en la lista
    return ' '.join(words)

def format_cellphone(cellphone):
    digits = ''.join(filter(str.isdigit, cellphone))
    formatted_number = f"({digits[:3]}) {digits[3:6]}.{digits[6:10]}"
    return formatted_number


def city_select(city):
    global address_part1,address_part2,telefone
    if city == "Ensenada":
        address_part1 = "Blvd. Teniente Azueta #130 int. 210"
        address_part2 = "Recinto Portuario, Ensenada B.C. C.P. 22800"
        telefone = "(646) 175.7732"
        return address_part1,address_part2,telefone
    else:
        address_part1 = "Av. Alejandro Von Humboldt 17618-Int. B,"
        address_part2 = "Garita de Otay, 22430 Tijuana, B.C."
        telefone = "(664) 624.8323"
        return address_part1,address_part2,telefone
