import pandas as pd
import os

def mostrar_archivos_y_peso(carpeta):
    # Recorre todos los archivos en la carpeta
    for archivo in os.listdir(carpeta):
        # Crea la ruta completa al archivo
        ruta_completa = os.path.join(carpeta, archivo)
        
        # Verifica si es un archivo (y no una carpeta)
        if os.path.isfile(ruta_completa):
            # Obtiene el tamaño del archivo en bytes
            tamaño_bytes = os.path.getsize(ruta_completa)
            
            # Convierte el tamaño a megabytes
            tamaño_megas = tamaño_bytes / (1024 * 1024)
            
            # Muestra el nombre del archivo y su tamaño en megabytes
            print(f"Archivo: {archivo}, Tamaño: {tamaño_megas:.2f} MB")


if __name__ == '__main__':
    print("Todo bien por aki")
    df = pd.read_excel("organismos.xlsx")
    #print(os.listdir("."))
    #print(os.listdir("shared_1"))
    #print(os.listdir("shared_2"))
    #print(os.listdir("shared_3"))
    #print(os.listdir("shared_4"))
    for i in df["organismo_nombre"][:500000]:
        print(i)
        df1 = pd.DataFrame()
        df2 = pd.DataFrame()
        df3 = pd.DataFrame()
        df4 = pd.DataFrame()
        
        if os.path.exists(f"shared_1/{i}.xlsx"):
            df1 = pd.read_excel(f"shared_1/{i}.xlsx")
        if os.path.exists(f"shared_2/{i}.xlsx"):
            df2 = pd.read_excel(f"shared_2/{i}.xlsx")
        if os.path.exists(f"shared_3/{i}.xlsx"):
            df1 = pd.read_excel(f"shared_3/{i}.xlsx")
        if os.path.exists(f"shared_4/{i}.xlsx"):
            df1 = pd.read_excel(f"shared_4/{i}.xlsx")
        concat = pd.concat([df1,df2,df3,df4])
        concat.to_excel(f"unir/{i}.xlsx", index=False)
    print("Termino de guardar en excel")
    mostrar_archivos_y_peso("unir")

        
        
