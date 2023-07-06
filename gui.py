import customtkinter as ctk
import cairo
from PIL import Image, ImageFont
import os
import re
from pathlib import Path
import shutil
import subprocess

# THEME
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

# Variables globales para almacenar los textos de cada campo
name = ""
position = ""
email = ""
cellphone = ""
address_part1 = ""
address_part2 = ""
telefone = ""
ext = ""

def mostrar_vista_previa():
    global surface
    # Cargar la imagen a modificar
    surface = cairo.ImageSurface.create_from_png("images/FrenteVacio.png")
    # Se crea un contexteo
    context = cairo.Context(surface)

    # Configurar la fuente y el texto
    font_path = "Fonts/microsoft_jhenghei.ttf"
    context.select_font_face(font_path)
    context.set_source_rgb(255, 255, 255)  # Color del texto

    # Dibujar el texto con fondo transparente
    x_name = 705
    y_name = 40
    #x_position = 672
    y_position = 62
    x_telefone = 680
    y_telefone = 95
    x_ext = 810
    y_ext = 95
    #x_email = 650
    
    #x_cellphone = 680
    
    if cellphone == "":
        x_address_part1 = 622
        y_address_part1 = 145
        #x_address_part2 = 592
        y_address_part2 = 165
    else:
        #global x_cellphone
        
        x_address_part1 = 622
        y_address_part1 = 165
        #x_address_part2 = 592
        y_address_part2 = 185
    
    #name
    context.set_font_size(19)
    context.move_to(x_name, y_name)
    context.show_text(name)

    #POSITION-----------------------------------------
    # Mide el ancho del texto previo
    extents = context.text_extents(name)
    ancho_name = extents.width
    # Mide el ancho del texto a centrar
    extents = context.text_extents(position)
    ancho_position = extents.width
    # Calcula la posición X para centrar el texto
    x_position = (x_name + ancho_name/2) - (ancho_position/2)
    # Dibujar
    context.set_font_size(18)
    context.move_to(x_position, y_position)
    context.show_text(position)
    #-------------------------------------------------

    #TELEFONE----------------------------------------
    context.move_to(x_telefone, y_telefone)
    context.show_text(telefone)
    #------------------------------------------------

    #EXT----------------------------------------
    context.move_to(x_telefone+130, y_telefone)
    context.show_text(ext)
    #------------------------------------------------

    #CELLPHONE--------------------------------------
    if telefone != "" and cellphone != "":
        y_cellphone = 115
        # Mide el ancho del texto previo
        extents = context.text_extents(telefone)
        extents2 = context.text_extents(ext)
        ancho_telefone = extents.width + extents2.width
        # Mide el ancho del texto a centrar
        extents = context.text_extents(cellphone)
        ancho_cellphone = extents.width
        # Calcula la posición X para centrar el texto
        x_cellphone = (x_telefone + ancho_telefone/2) - (ancho_cellphone/2)
        
        #Dibujar
        context.move_to(x_cellphone, y_cellphone)
        context.show_text(cellphone)
        #icono
        icono = cairo.ImageSurface.create_from_png("images/WhatsappIcon.png")
        icono_x = x_cellphone - 25
        icono_y = y_cellphone - 13
       # Dibujar el icono en el contexto como máscara
        context.save()  # Guardar el estado actual del contexto
        context.set_source_surface(icono, icono_x, icono_y)
        context.paint_with_alpha(1)  # Utilizar la imagen como máscara con opacidad completa
        context.restore()  # Restaurar el estado del contexto
    #-------------------------------------------------

    #EMAIL-------------------------------------------
    if cellphone != "":
        y_email = 135
        # Mide el ancho del texto previo
        extents = context.text_extents(cellphone)
        ancho_cellphone = extents.width
        # Mide el ancho del texto a centrar
        extents = context.text_extents(email)
        ancho_email = extents.width
        # Calcula la posición X para centrar el texto
        x_email = (x_cellphone + ancho_cellphone/2) - (ancho_email/2)
        context.move_to(x_email, y_email)
    else:
        y_email = 110
        # Mide el ancho del texto previo
        extents = context.text_extents(telefone) 
        extents2 = context.text_extents(ext) 
        ancho_telefone = extents.width + extents2.width
        # Mide el ancho del texto a centrar
        extents = context.text_extents(email)
        ancho_email = extents.width
        # Calcula la posición X para centrar el texto
        x_email = (x_telefone + ancho_telefone/2) - (ancho_email/2)
        context.move_to(x_email, y_email)

    #Dibujar
    
    context.show_text(email)
    #-----------------------------------------------

    #ADDRESS-------------------------------------------
    #address_part1
    context.set_font_size(17)
    context.move_to(x_address_part1, y_address_part1)
    context.show_text(address_part1)
    # Mide el ancho del texto previo
    extents = context.text_extents(address_part1)
    ancho_address_part1 = extents.width
    # Mide el ancho del texto a centrar
    extents = context.text_extents(address_part2)
    ancho_address_part2 = extents.width
    # Calcula la posición X para centrar el texto
    x_address_part2 = (x_address_part1 + ancho_address_part1/2) - (ancho_address_part2/2)
    #Dibujar
    #address_part2
    context.move_to(x_address_part2, y_address_part2)
    context.show_text(address_part2)
    #-------------------------------------------------

    # Guardar la imagen modificada
    surface.write_to_png("imagen_modificada.png")

    # Cargar la imagen modificada en el widget de imagen
    width, height = 954, 266
    raw_preview = Image.open(
        'imagen_modificada.png')
    resized_preview = raw_preview.resize((width, height))
    converted_preview = ctk.CTkImage(resized_preview, size=(954, 266))
    firma_preview.configure(root, image=converted_preview, text=None)

# Funciones para actualizar los textos de los campos
def actualizar_name(event):
    global name
    global position
    name = name_field.get()
    name = custom_title(name)
    if name != "":
        position_field.configure(state="normal")
    else: 
        position_field.delete(0, ctk.END)
        position_field.configure(state="disabled")
    mostrar_vista_previa()


def actualizar_position(event):
    global position
    global name
    if name != "":
        position = position_field.get()
        position = custom_title(position)
        mostrar_vista_previa()

def actualizar_ext(event):
    global ext
    global telefone
    
    ext = ext_field.get()
    ext = "  " + "Ext." + ext
    #telefone = telefone + "  " + "Ext." + ext
    mostrar_vista_previa()

def actualizar_email(event):
    global email
    global telefone
    email = email_field.get()
    validate_email()
    if error_label.cget("text") == "":
        mostrar_vista_previa()

def actualizar_cellphone(event):
    global cellphone
    cellphone = cellphone_field.get()
    if cellphone != "":
        cellphone = format_cellphone(cellphone)
    mostrar_vista_previa()

def actualizar_addressAndTelefone(event):
    global address_part1
    global address_part2
    global telefone
    address_part1 = address_part1
    address_part2 = address_part2
    telefone = telefone
    if telefone != "":
        email_field.configure(state="normal")
        ext_field.configure(state="normal")
    else: 
        email_field.delete(0, ctk.END)
        email_field.configure(state="disabled")
    mostrar_vista_previa()

# Crear una ventana de Tkinter
root = ctk.CTk()
root.geometry("954x550")  # WidthxHeight
root.resizable(False,False)
root.title("Generador de Firmas")
root.iconbitmap(r'images/icon.ico')

#-----------------------------------------------------------
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

def validate_email():
    email_regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,}$'
    email= email_field.get()
    if email and not re.search(email_regex, email):
        error_label.configure(text="Correo inválido")
    else:
        error_label.configure(text="")

def validate_cellphone_input(value_if_allowed):
    if value_if_allowed == "":
        return True
    elif value_if_allowed.isdigit() and len(value_if_allowed) <= 10:
        return True
    else:
        return False
    
user_homefolder = str(Path.home())   
def save_result():
    global surface
    global name
    first_name_text = name
    if first_name_text != "":
        export_firma_folder = (user_homefolder +
                            '/Downloads/' + first_name_text)
        export_file_name = first_name_text + ".png"
        if os.path.exists(export_firma_folder):
            shutil.rmtree(export_firma_folder)
        os.makedirs(export_firma_folder)
        export_front = (export_firma_folder + '/' +
                        'Frente_' + export_file_name)

        surface.write_to_png(export_front)

        formatted_path = os.path.normpath(export_firma_folder)
        subprocess.Popen(r'explorer /open,"{}"'.format(formatted_path))


#-----------------------------------------------------------

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

# ----------------------------------------------
################### City ###############################################3

city_CTkLabel = ctk.CTkLabel(
    root, text="Ciudad:", font=("NotoSans-Bold", 20, "bold"), text_color="#595959")
city_CTkLabel.place(x=256, y=272,)

city_field = ctk.CTkComboBox(
    root, fg_color="white", corner_radius=7,  width=170, font=("Amiko", 15),values=["Ensenada", "Tijuana"],command=city_select)
city_field.place(x=350, y=273,)
city_field.set("Seleccionar")

# Crear un botón para mostrar la vista previa del segundo campo
add_city_button = ctk.CTkButton(
    root, text="+", width=24, height=24, font=("NotoSans-Bold", 17, "bold"), text_color="#ffffff")
add_city_button.place(x=530, y=274,)
# Bind the field user input storing to keys and click
add_city_button.bind("<Button-1>",  actualizar_addressAndTelefone)
city_field.bind("<Return>", actualizar_addressAndTelefone)
city_field.bind("<Tab>", actualizar_addressAndTelefone) 

################### NAME ###############################
first_name_CTkLabel = ctk.CTkLabel(
    root, text="Nombre:", font=("NotoSans-Bold", 20, "bold"), text_color="#595959")
first_name_CTkLabel.place(x=256, y=312,)

name_field = ctk.CTkEntry(
    root, fg_color="white", corner_radius=7,  width=170, font=("Amiko", 15))
name_field.place(x=350, y=313,)
name_field.configure(validate="key",
                           validatecommand=(root.register(validate_name_input), '%P'))

# Crear un botón para mostrar la vista previa del primer campo
add_firstname_button = ctk.CTkButton(
    root, text="+", width=24, height=24,   font=("NotoSans-Bold", 17, "bold"), text_color="#ffffff")
add_firstname_button.place(x=530, y=314,)
# Bind the field user input storing to keys and click
add_firstname_button.bind("<Button-1>",  actualizar_name)
name_field.bind("<Return>", actualizar_name)
name_field.bind("<Tab>", actualizar_name)


#--------------------------------------------------------------
########################## POSITION ####################################################3

position_CTkLabel = ctk.CTkLabel(
    root, text="Puesto:", font=("NotoSans-Bold", 20, "bold"), text_color="#595959")
position_CTkLabel.place(x=256, y=352,)

position_field = ctk.CTkEntry(
    root, fg_color="white", corner_radius=7,  width=170, font=("Amiko", 15))
position_field.place(x=350, y=353,)
position_field.configure(validate="key", state="disabled",
                         validatecommand=(root.register(validate_position_input), '%P'))



# Crear un botón para mostrar la vista previa del segundo campo
add_position_button = ctk.CTkButton(
    root, text="+", width=24, height=24,   font=("NotoSans-Bold", 17, "bold"), text_color="#ffffff")
add_position_button.place(x=530, y=354,)
# Bind the field user input storing to keys and click
add_position_button.bind("<Button-1>",  actualizar_position)
position_field.bind("<Return>", actualizar_position)
position_field.bind("<Tab>", actualizar_position)

#---------------------------------------------------------------------------------
########################## EXT ####################################################3

ext_CTkLabel = ctk.CTkLabel(
    root, text="Ext.:", font=("NotoSans-Bold", 20, "bold"), text_color="#595959")
ext_CTkLabel.place(x=256, y=392,)

ext_field = ctk.CTkEntry(
    root, fg_color="white", corner_radius=7,  width=170, font=("Amiko", 15))
ext_field.place(x=350, y=393,)
ext_field.configure(validate="key", state="disabled",
                         validatecommand=(root.register(validate_ext_input), '%P'))



# Crear un botón para mostrar la vista previa del segundo campo
add_ext_button = ctk.CTkButton(
    root, text="+", width=24, height=24,   font=("NotoSans-Bold", 17, "bold"), text_color="#ffffff")
add_ext_button.place(x=530, y=394,)
# Bind the field user input storing to keys and click
add_ext_button.bind("<Button-1>",  actualizar_ext)
ext_field.bind("<Return>", actualizar_ext)
ext_field.bind("<Tab>", actualizar_ext)

#---------------------------------------------------------------------------------
########################### Email ##############################################


email_CTkLabel = ctk.CTkLabel(
    root, text="Correo:", font=("NotoSans-Bold", 20, "bold"), text_color="#595959")
email_CTkLabel.place(x=256, y=432,)

email_field = ctk.CTkEntry(
    root, fg_color="white", corner_radius=7,  width=170, font=("Amiko", 15))
email_field.place(x=350, y=433,)
email_field.configure(validate="key",state="disabled",
                         validatecommand=(root.register(validate_email_input), '%P'))
error_label = ctk.CTkLabel(root, text="",text_color="#FF0000")
error_label.place(x=580, y=433)


# Crear un botón para mostrar la vista previa del segundo campo
add_email_button = ctk.CTkButton(
    root, text="+", width=24, height=24, font=("NotoSans-Bold", 17, "bold"), text_color="#ffffff")
add_email_button.place(x=530, y=434,)
# Bind the field user input storing to keys and click
add_email_button.bind("<Button-1>",  actualizar_email)
email_field.bind("<Return>", actualizar_email)
email_field.bind("<Tab>", actualizar_email) 


########################### Cellphone ##############################################

cellphone_CTkLabel = ctk.CTkLabel(
    root, text="Celular:", font=("NotoSans-Bold", 20, "bold"), text_color="#595959")
cellphone_CTkLabel.place(x=256, y=472,)

cellphone_field = ctk.CTkEntry(
    root, fg_color="white", corner_radius=7,  width=170, font=("Amiko", 15))
cellphone_field.place(x=350, y=473,)
cellphone_field.configure(validate="key",
                         validatecommand=(root.register(validate_cellphone_input), '%P'))

# Crear un botón para mostrar la vista previa del segundo campo
add_cellphone_button = ctk.CTkButton(
    root, text="+", width=24, height=24, font=("NotoSans-Bold", 17, "bold"), text_color="#ffffff")
add_cellphone_button.place(x=530, y=474,)
# Bind the field user input storing to keys and click
add_cellphone_button.bind("<Button-1>",  actualizar_cellphone)
cellphone_field.bind("<Return>", actualizar_cellphone)
cellphone_field.bind("<Tab>", actualizar_cellphone) 

####################### SAVE ########################################################

button_save = ctk.CTkButton(master=root, text="Guardar", width=50,
                                 height=32, command=save_result)
button_save.place(x=650, y=473)



#-----------------------------------------------------------------------------------------
# Crear un widget de imagen para mostrar la vista previa
raw_preview = Image.open(
    'images/FrenteVacio.png')

width, height = 954, 266
resized_preview = raw_preview.resize((width, height))

# Convert the resized image to PhotoImage
converted_preview = ctk.CTkImage(resized_preview, size=(954, 266))

# Create a CTkLabel widget to display the image
firma_preview = ctk.CTkLabel(root, image=converted_preview, text=None, )

firma_preview.place(x=0, y=0)

# Ejecutar el bucle principal de Tkinter
root.mainloop()
