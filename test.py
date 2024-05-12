import pandas as pd
from datetime import datetime
import re
import os
import time
import tarfile


def delete_old_logs(directory, file_extension=".log", days_old=7):
    # Obtener la fecha actual
    current_time = time.time()
    # Convertir los días a segundos
    age_in_seconds = days_old * 24 * 60 * 60
    
    # Iterar sobre los archivos en el directorio
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(file_extension):
                # Obtener la ruta completa del archivo
                file_path = os.path.join(root, file)
                # Obtener la fecha de modificación del archivo
                file_mtime = os.path.getmtime(file_path)
                # Calcular la antigüedad del archivo en segundos
                file_age = current_time - file_mtime
                # Si el archivo es más antiguo que el límite, eliminarlo
                if file_age > age_in_seconds:
                    os.remove(file_path)




date_format = "%Y/%m/%d"


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
##PersonalContratohonorarios = PersonalContratohonorarios.rename(columns={'remuneracionbruta': 'remuneracionbruta_mensual'})

def getFiles(carpeta):
    salida = []
    for archivo in os.listdir(carpeta):
        # Obtén la ruta completa del archivo
        ruta_completa = os.path.join(carpeta, archivo)
        # Verifica si es un archivo (y no una subcarpeta)
        if os.path.isfile(ruta_completa):
            # Haz algo con el archivo, por ejemplo, imprimir su nombre
            print(archivo)
            salida.append(archivo)
    return salida

def readCSV(nombreFile):
    if(nombreFile == "TA_PersonalPlanta.csv"):
        df = pd.read_csv(f"shared/{nombreFile}", low_memory=False,sep=";",encoding="latin",usecols=PersonalPlantaDICT)
    elif(nombreFile == "TA_PersonalContrata.csv"):
        df = pd.read_csv(f"shared/{nombreFile}", low_memory=False,sep=";",encoding="latin",usecols=PersonalContrataDICT)
    elif(nombreFile == "TA_PersonalCodigotrabajo.csv"):
        df = pd.read_csv(f"shared/{nombreFile}", low_memory=False,sep=";",encoding="latin",usecols=PersonalCodigotrabajoDICT)
    elif(nombreFile == "TA_PersonalContratohonorarios.csv"):
        df = pd.read_csv(f"shared/{nombreFile}", low_memory=False,sep=";",encoding="latin",usecols=PersonalContratohonorariosDICT)
        df = df.rename(columns={'remuneracionbruta': 'remuneracionbruta_mensual'})
    return df

def getDF(url,columnas):
    #return pd.read_csv(url, low_memory=False,sep=";",encoding="latin",usecols=columnas)
    return pd.read_csv(url, low_memory=False,sep=";",encoding="latin",usecols=columnas)



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

#if __name__ == '__main__':
#    print("Todo bien prueba 1")
#    getFiles("shared/")

def saveParcial(df,columna):
    organismo = df1[df1["organismo_nombre"] == columna]
    organismo.to_excel(f"organismo/{i}.xlsx", index=False)
    return 


if __name__ == '__main__':
    directory = "/home/runner/runners"
    #df1 = pd.read_csv("shared/TA_PersonalPlanta.csv", low_memory=False,sep=";",encoding="latin",usecols=PersonalPlantaDICT)
    df1 = pd.read_csv("shared/TA_PersonalPlanta.csv", low_memory=False,encoding="latin",usecols=PersonalPlantaDICT)
    df2 = pd.read_csv("shared/TA_PersonalContrata.csv", sep=";",encoding="latin",usecols=PersonalContrataDICT)
    #df3 = pd.read_csv("shared/TA_PersonalCodigotrabajo.csv", sep=";",encoding="latin",usecols=PersonalCodigotrabajoDICT)
    #df4 = pd.read_csv("shared/TA_PersonalContratohonorarios.csv", sep=";",encoding="latin",usecols=PersonalContratohonorariosDICT)
    #df4 = df4.rename(columns={'remuneracionbruta': 'remuneracionbruta_mensual'})
    df1 = addColumns(df1)
    df2 = addColumns(df2)
    #df3 = addColumns(df3)
    #df4 = addColumns(df4)
    merge = pd.concat([df1,df2])
    #for i in merge["organismo_nombre"].unique():
    #    organismo = merge[merge["organismo_nombre"] == i]
    #    organismo.to_excel(f"organismo/{i}.xlsx", index=False)
    # Llamar a la función para eliminar archivos de registro antiguos
    #delete_old_logs(directory)
    print(len(merge))
    #listaDF = [readCSV(name) for name in getFiles("shared")]
    #personal = pd.concat(listaDF)
    #df1 = pd.read_csv("shared/TA_PersonalPlanta.csv", low_memory=False,sep=";",encoding="latin",usecols=PersonalPlantaDICT)
    #df1 = addColumns(df1)
    #df2 = pd.read_csv("shared/TA_PersonalContrata.csv", sep=";",encoding="latin",usecols=PersonalContrataDICT)
    #df2 = addColumns(df2)

    #merge = pd.concat([df1,df2])

    #[saveParcial(df1,x) for x in df1["organismo_nombre"].unique()]
    #for i in merge["organismo_nombre"].unique():
    #    organismo = merge[merge["organismo_nombre"] == i]
    #    organismo.to_excel(f"organismo/{i}.xlsx", index=False)
    #print(2)
    #delete_old_logs(directory)

    """
    df2 = pd.read_csv("shared/TA_PersonalContrata.csv", sep=";",encoding="latin",usecols=PersonalContrataDICT)
    df2 = addColumns(df2)
    print(3)
    
    for i in df2["organismo_nombre"].unique():
        organismo = df2[df2["organismo_nombre"] == i]
        try:
            aux = pd.read_excel(f"organismo/{i}.xlsx")
            pd.concat([organismo,aux]).to_excel(f"organismo/{i}.xlsx", index=False)
        except:
            pd.concat([organismo]).to_excel(f"organismo/{i}.xlsx", index=False)
    #delete_old_logs(directory)
    df3 = pd.read_csv("shared/TA_PersonalCodigotrabajo.csv", sep=";",encoding="latin",usecols=PersonalCodigotrabajoDICT)
    df3 = addColumns(df3)
    print(4)
    for i in df3["organismo_nombre"].unique():
        organismo = df3[df["organismo_nombre"] == i]
        try:
            aux = pd.read_excel(f"organismo/{i}.xlsx")
            pd.concat([organismo,aux]).to_excel(f"organismo/{i}.xlsx", index=False)
        except:
            pd.concat([organismo]).to_excel(f"organismo/{i}.xlsx", index=False)
    """
    #delete_old_logs(directory)
    #df4 = pd.read_csv("shared/TA_PersonalContratohonorarios.csv", sep=";",encoding="latin",usecols=PersonalContratohonorariosDICT)
    #df4 = df4.rename(columns={'remuneracionbruta': 'remuneracionbruta_mensual'})
    #df4 = addColumns(df4)
    #for i in df1["organismo_nombre"].unique()[:15]:
    #    organismo = df4[df4["organismo_nombre"] == i]
    #    try:
    #        aux = pd.read_excel(f"organismo/{i}.xlsx")
    #        pd.concat([organismo,aux]).to_excel(f"organismo/{i}.xlsx", index=False)
    #    except:
    #        pd.concat([organismo]).to_excel(f"organismo/{i}.xlsx", index=False)
    #personal = pd.concat([df1,df2,df3,df4])
    #personal = pd.concat([df1])
    print(5)
    #personal["remuneracionbruta_mensual"] = personal["remuneracionbruta_mensual"].apply(getFloat)
    #personal["remuliquida_mensual"] = personal["remuliquida_mensual"].apply(getFloat)
    #personal["Nombres2"] = personal["Nombres"].apply(eliminar_espacios_adicionales)
    #personal["NOMBRECOMPLETO"] = personal.apply(getFullName,axis=1)
    #personal["Nombres2"] = personal["Nombres2"].apply(transformar_string) 
    #personal["NOMBRECOMPLETO2"] = personal["NOMBRECOMPLETO"].apply(transformar_string) 
    #print(6)
    #for i in personal["organismo_nombre"].unique()[:15]:
    #    organismo = personal[personal["organismo_nombre"] == i]
    #    organismo.to_excel(f"organismo/{i}.xlsx", index=False)
    #print(7)


    
