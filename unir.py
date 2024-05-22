import pandas as pd
import os


if __name__ == '__main__':
    print("Todo bien por aki")
    df = pd.read_excel("organismos.xlsx")
    print(os.listdir("shared_1"))
    print(os.listdir("shared_2"))
    print(os.listdir("shared_3"))
    print(os.listdir("shared_4"))

    for i in df["organismo_nombre"]:
        print(i)
        df1 = pd.DataFrame()
        df2 = pd.DataFrame()
        df3 = pd.DataFrame()
        df4 = pd.DataFrame()
        
        if os.path.exists(f"shared_1/{i}"):
            df1 = pd.read_excel(f"shared_1/{i}.xlsx")
        if os.path.exists(f"shared_2/{i}"):
            df2 = pd.read_excel(f"shared_2/{i}.xlsx")
        if os.path.exists(f"shared_3/{i}"):
            df1 = pd.read_excel(f"shared_3/{i}.xlsx")
        if os.path.exists(f"shared_4/{i}"):
            df1 = pd.read_excel(f"shared_4/{i}.xlsx")
        concat = pd.concat([df1,df2,df3,df4])
        concat.to_excel(f"unir/{i}.xlsx", index=False)
    print("Termino de guardar en excel")

        
        
