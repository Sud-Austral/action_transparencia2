import pandas as pd
from datetime import datetime
import re
import os
import time
import tarfile
import requests


base = "https://www.cplt.cl/transparencia_activa/datoabierto/archivos/"
deseadas =["Nombres","Paterno","Materno","organismo_nombre",'anyo', 'Mes','tipo_calificacionp']


TA_PersonalPlanta                       = f"{base}TA_PersonalPlanta.csv"
TA_PersonalContrata                     = f"{base}TA_PersonalContrata.csv"
TA_PersonalCodigotrabajo                = f"{base}TA_PersonalCodigotrabajo.csv"
TA_PersonalContratohonorarios           = f"{base}TA_PersonalContratohonorarios.csv"


PersonalPlantaDICT                = deseadas+["remuliquida_mensual",'Tipo cargo', 'remuneracionbruta_mensual']
PersonalContrataDICT              = deseadas+["remuliquida_mensual",'Tipo cargo','remuneracionbruta_mensual'] 
PersonalCodigotrabajoDICT         = deseadas+["remuliquida_mensual",'Tipo cargo', 'remuneracionbruta_mensual']
PersonalContratohonorariosDICT    = deseadas+['remuliquida_mensual','tipo_pago','num_cuotas','remuneracionbruta']

def eliminar_espacios_adicionales(cadena):
    if(type(cadena) == float):
        return "NO"
    return re.sub(r'\s+', ' ', cadena).strip()

def getFullName(fila):
    name = fila["Nombres2"]
    apellidoP = fila['Paterno']
    apellidoM = fila['Materno']
    return f"{name} {apellidoP} {apellidoM}"

def transformar_string(texto):
    # Convertir a mayúsculas
    texto = texto.upper()
    # Reemplazar tildes por letras sin tilde
    texto = texto.replace('Á', 'A').replace('É', 'E').replace('Í', 'I').replace('Ó', 'O').replace('Ú', 'U')
    # Reemplazar la letra "ñ" por "n"
    texto = texto.replace('Ñ', 'N')
    return texto

def getFloat(numero):
    try:
        return float(numero[:-2])
    except:
        return 0




def descarga():
    PersonalPlanta             = getDF(TA_PersonalPlanta              ,PersonalPlantaDICT)
    PersonalContrata           = getDF(TA_PersonalContrata            ,PersonalContrataDICT)
    PersonalCodigotrabajo      = getDF(TA_PersonalCodigotrabajo       ,PersonalCodigotrabajoDICT)
    PersonalContratohonorarios = getDF(TA_PersonalContratohonorarios  ,PersonalContratohonorariosDICT)
    personal = pd.concat([PersonalContrata,PersonalPlanta,PersonalCodigotrabajo,PersonalContratohonorarios])
    return personal

def getFecha(fecha):
    try:
        return datetime.strptime(fecha, date_format)
    except:
        return None

def consolidar():
    personal = descarga()
    personal["remuneracionbruta_mensual"] = personal["remuneracionbruta_mensual"].apply(getFloat)
    personal["remuliquida_mensual"] = personal["remuliquida_mensual"].apply(getFloat)
    personal["Nombres2"] = personal["Nombres"].apply(eliminar_espacios_adicionales)
    personal["NOMBRECOMPLETO"] = personal.apply(getFullName,axis=1)
    personal["Nombres2"] = personal["Nombres2"].apply(transformar_string) 
    personal["NOMBRECOMPLETO2"] = personal["NOMBRECOMPLETO"].apply(transformar_string) 
    for i in personal["organismo_nombre"].unique():
        organismo = personal[personal["organismo_nombre"] == i]
        organismo.to_excel(f"organismo/{i}.xlsx", index=False)

def addColumns(personal):
    personal["remuneracionbruta_mensual"] = personal["remuneracionbruta_mensual"].apply(getFloat)
    personal["remuliquida_mensual"] = personal["remuliquida_mensual"].apply(getFloat)
    personal["Nombres2"] = personal["Nombres"].apply(eliminar_espacios_adicionales)
    personal["NOMBRECOMPLETO"] = personal.apply(getFullName,axis=1)
    personal["Nombres2"] = personal["Nombres2"].apply(transformar_string) 
    personal["NOMBRECOMPLETO2"] = personal["NOMBRECOMPLETO"].apply(transformar_string) 
    return personal

url = 'https://www.cplt.cl/transparencia_activa/datoabierto/archivos/TA_PersonalPlanta.csv'
output_file = 'TA_PersonalPlanta.csv'
chunk_size = 1048576  # 1 MB

def download_file(url, output_file, chunk_size):
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        with open(output_file, 'wb') as file:
            for chunk in response.iter_content(chunk_size=chunk_size):
                file.write(chunk)
                print(f"Downloaded {file.tell()} bytes")
    
    print(f"Download complete. File saved as {output_file}")

if __name__ == '__main__':
    #df = pd.read_csv(f"TA_PersonalPlanta.csv", low_memory=False,sep=";",encoding="latin",usecols=PersonalPlantaDICT)
    #df = pd.read_csv(f"TA_PersonalPlanta.csv", low_memory=False,sep=";",encoding="latin")
    #chunk_size = 1024 * 1024
    #df = pd.read_csv(TA_PersonalPlanta, low_memory=False,sep=";",encoding="latin",chunksize=chunk_size)
    #print(df.columns)
    #df = addColumns(df)
    #for i in df["organismo_nombre"].unique():
    #    organismo = df[df["organismo_nombre"] == i]
    #    organismo.to_excel(f"build1/{i}.xlsx", index=False)
    
    url = 'https://www.cplt.cl/transparencia_activa/datoabierto/archivos/TA_PersonalPlanta.csv'
    headers = {'Range': 'bytes=0-1004857600'}  # 0-1048575 bytes son los primeros 1 MB
"""
    response = requests.get(url, headers=headers, stream=True)

    if response.status_code == 200:  # El código de estado 206 indica que se ha recibido una respuesta parcial
        with open('partial_file.csv', 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
    else:
        print("No se pudo obtener la porción del archivo. Código de estado:", response.status_code)
   
"""
    download_file(url, output_file, chunk_size)
    df = pd.read_csv(output_file, low_memory=False,sep=";",encoding="latin",usecols=PersonalPlantaDICT)
    df = addColumns(df)
    for i in df["organismo_nombre"].unique():
        organismo = df[df["organismo_nombre"] == i]
        organismo.to_excel(f"build1/{i}.xlsx", index=False)
    if os.path.exists(output_file):
        os.remove(output_file)
        print(f"File {output_file} has been deleted.")
    else:
        print(f"File {output_file} not found.")
