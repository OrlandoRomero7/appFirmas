import pandas as pd
import cairo
import os
from pathlib import Path
import shutil
import subprocess
import numpy as np


#Leer excel de operativo
ruta_archivo = "EmpleadosFirmasEnsenada.xlsx"
nombre_hoja = "Operativo"
datos_excel = pd.read_excel(ruta_archivo, sheet_name=nombre_hoja, usecols=[1, 2, 4, 5, 6, 7])

#Se indica a que columna correspondra cada varaible
nombre_completo = datos_excel.iloc[:, 0].str.split(" ", expand=True)
nombre = nombre_completo[2]
primer_apellido = nombre_completo[0]
puesto = datos_excel.iloc[:, 1]
extension = datos_excel.iloc[:, 2]
correo = datos_excel.iloc[:, 3]
celular = datos_excel.iloc[:, 4]
carrera = datos_excel.iloc[:, 5]
 
# Variables globales para almacenar los textos de cada campo
name = ""
position = ""
email = ""
cellphone = ""
address_part1 = "Blvd. Teniente Azueta #130 int. 210"
address_part2 = "Recinto Portuario, Ensenada B.C. C.P. 22800"
""" address_part1 = "Av. Alejandro Von Humboldt 17618-Int. B,"
address_part2 = "Garita de Otay, 22430 Tijuana, B.C." """
telefone = ""
num_ensenada = "(646) 175.7732"
num_tijuana = "(664) 624.8323"
ext = ""
studies = ""
nameAndStudies = ""


#Funcion que muestra los textos en la iamgen
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

    ################ NAME AND POSITION ##############################

    cuadro_name_x = 685
    cuadro_name_y = 14
    cuadro_name_ancho = 250
    cuadro_name_alto = 25

    cuadro_position_x = 685
    cuadro_position_y = 35
    cuadro_position_ancho = 250
    cuadro_position_alto = 25

    # Calcular la posición de los textos
    context.set_font_size(19)
    #name_extends = context.text_extents(nameAndStudies)
    name_extends = context.text_extents(nameAndStudies)
    context.set_font_size(18)
    position_extends = context.text_extents(position)

    margen_vertical_name = cuadro_name_alto - name_extends.height

    name_x = cuadro_name_x + (cuadro_name_ancho - name_extends.width) / 2
    name_y = cuadro_name_y + margen_vertical_name + name_extends.height

    margen_vertical_position = cuadro_position_alto - position_extends.height

    position_x = cuadro_position_x + (cuadro_position_ancho - position_extends.width) / 2
    position_y = cuadro_position_y + margen_vertical_position + position_extends.height

    """ # Dibujar el cuadro de texto transparente
    context.rectangle(cuadro_x, cuadro_y, cuadro_ancho, cuadro_alto)
    context.set_source_rgba(0, 0, 0, 1)
    context.fill() """

    # Dibujar los textos centrados dentro del cuadro
    context.set_source_rgb(255, 255, 255)  # Establecer color del texto
    
    context.set_font_size(19)
    context.move_to(name_x, name_y)
    context.show_text(nameAndStudies)

    context.set_font_size(18)
    context.move_to(position_x, position_y)
    context.show_text(position) 

    ##########################TELEFONE, EXT, CELLPHONE########################################
    # Dimensiones Cuadro de texto telefono, correo, celular y address
    if cellphone == "":
        cuadro_tel_x = 645
        cuadro_tel_y = 70
        cuadro_tel_ancho = 290
        cuadro_tel_alto = 50
        #cuadro address
        cuadro_addr_x = 580
        cuadro_addr_y = 125
        cuadro_addr_ancho = 330
        cuadro_addr_alto = 50
    else:
        cuadro_tel_x = 645
        cuadro_tel_y = 70
        cuadro_tel_ancho = 290
        cuadro_tel_alto = 60
        #cuadro address
        cuadro_addr_x = 580
        cuadro_addr_y = 135
        cuadro_addr_ancho = 330
        cuadro_addr_alto = 50

    if ext == "":
        telefone = num_ensenada
    else:
        telefone = num_ensenada + " ext." + ext 

    """ if ext == "":
        telefone = num_tijuana
    else:
        telefone = num_tijuana + " ext." + ext  """

    telefone_extents = context.text_extents(telefone)
    email_extents = context.text_extents(email)
    cellphone_extents = context.text_extents(cellphone)

    margen_vertical_tel = (cuadro_tel_alto - (telefone_extents.height + email_extents.height + cellphone_extents.height)) / 2

    #####telefone
    telefone_x = cuadro_tel_x + (cuadro_tel_ancho - telefone_extents.width) / 2
    telefone_y = cuadro_tel_y + margen_vertical_tel + telefone_extents.height

    if cellphone == "":
        #####email
        email_x = cuadro_tel_x + (cuadro_tel_ancho - email_extents.width) / 2
        email_y = cuadro_tel_y + margen_vertical_tel + telefone_extents.height + 20
    else:
        #icono
        icono = cairo.ImageSurface.create_from_png("images/WhatsappIcon.png")
        ####cellphone
        cellphone_x = cuadro_tel_x + (cuadro_tel_ancho - cellphone_extents.width) / 2
        cellphone_y = cuadro_tel_y + margen_vertical_tel + telefone_extents.height + 20
        icono_x = cellphone_x - 25
        icono_y = cellphone_y - 15
        # Dibujar el icono en el contexto como máscara
        context.save()  # Guardar el estado actual del contexto
        context.set_source_surface(icono, icono_x, icono_y)
        context.paint_with_alpha(1)  # Utilizar la imagen como máscara con opacidad completa
        context.restore()  # Restaurar el estado del contexto 
        #####email
        email_x = cuadro_tel_x + (cuadro_tel_ancho - email_extents.width) / 2
        email_y = cuadro_tel_y + margen_vertical_tel + cellphone_extents.height + 40

    context.rectangle(cuadro_tel_x, cuadro_tel_y, cuadro_tel_ancho, cuadro_tel_alto)
    context.set_source_rgba(0, 0, 0, 0)

    context.set_source_rgb(255, 255, 255)
    context.move_to(telefone_x, telefone_y)
    context.show_text(telefone)
    if cellphone != "":
        context.move_to(cellphone_x, cellphone_y)
    context.show_text(cellphone)

    context.move_to(email_x, email_y)
    context.show_text(email)

    ######################### ADDRESS ##################################
    context.set_font_size(17)
    address_part1_extents = context.text_extents(address_part1)
    address_part2_extents = context.text_extents(address_part2)

    margen_vertical_address = (cuadro_addr_alto - (address_part1_extents.height + address_part2_extents.height)) / 2

    address_part1_x = cuadro_addr_x + (cuadro_addr_ancho - address_part1_extents.width) / 2
    address_part1_y = cuadro_addr_y + margen_vertical_address+ address_part1_extents.height

    address_part2_x = cuadro_addr_x + (cuadro_addr_ancho - address_part2_extents.width) / 2
    address_part2_y = cuadro_addr_y + margen_vertical_address+ address_part1_extents.height + 20

    context.rectangle(cuadro_addr_x, cuadro_addr_y, cuadro_addr_ancho, cuadro_addr_alto)
    context.set_source_rgba(0, 0, 0, 0)
    context.set_source_rgb(255, 255, 255)
    
    
    context.move_to(address_part1_x, address_part1_y)
    context.show_text(address_part1)

    context.move_to(address_part2_x, address_part2_y)
    context.show_text(address_part2)


    # Guarda la imagen modificada con todos los textos ya ingresados
    surface.write_to_png("imagen_modificada.png")

#Se foratea el nombre y puesto de la persona
def custom_title(s):
    no_capitalize = ["y", "e", "o", "u", "de"]
    words = s.split(' ')
    for i in range(len(words)):
        word = words[i]
        if "-" in word:
            hyphen_index = word.index("-")
            first_part = word[:hyphen_index].capitalize()
            second_part = word[hyphen_index + 1:].capitalize()
            words[i] = f"{first_part}-{second_part}"
        elif word.lower() not in no_capitalize or i == 0:
            words[i] = word.capitalize()
        else:
            words[i] = word.lower()
    return ' '.join(words)



def format_cellphone(cellphone):
    digits = ''.join(filter(str.isdigit, cellphone))
    formatted_number = f"({digits[:3]}) {digits[3:6]}.{digits[6:10]}"
    return formatted_number

#Se guarda cada firma en un folder, con el nombre de la persona
user_homefolder = str(Path.home()) 
def save_result():
    global surface
    global name,position
    first_name_text = name
    if first_name_text != "":
        operavio_folder = os.path.join(user_homefolder, 'Downloads', nombre_hoja)
        os.makedirs(operavio_folder, exist_ok=True)
        export_firma_folder = os.path.join(operavio_folder, first_name_text)
        os.makedirs(export_firma_folder, exist_ok=True)
        export_file_name = first_name_text + ".png"
        export_front = os.path.join(export_firma_folder, 'Frente_' + export_file_name)
        surface.write_to_png(export_front)

    

# Recorre cada fila y los valores se le asignan a las varaibles locales que son las que se insertan en la imagen
for nom, ape, pue, ex, co, celu, carre in zip(nombre, primer_apellido, puesto, extension, correo, celular, carrera):
    
    name = nom + " " + ape
    name = custom_title(str(name))
    studies = str(carre)
    if studies == "nan": 
        studies = ""
        nameAndStudies = name
    else:
        studies = carre
        nameAndStudies = studies + " " + name 
      
    position = custom_title(str(pue))

    if np.isnan(ex):
        ext = ""
    else:
        ext = str(ex).split(".")[0]
    email = str(co)
    if email == "nan":
        email = ""
    cellphone = str(celu)
    if cellphone == "nan":
        cellphone = "" 
    else:
        cellphone = format_cellphone(cellphone)
    mostrar_vista_previa()
    save_result()
    name = ""
    position = ""
    

