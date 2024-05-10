import pandas as pd

PersonalPlantaDICT                = deseadas+["remuliquida_mensual",'Tipo cargo', 'remuneracionbruta_mensual']
PersonalContrataDICT              = deseadas+["remuliquida_mensual",'Tipo cargo','remuneracionbruta_mensual'] 
PersonalCodigotrabajoDICT         = deseadas+["remuliquida_mensual",'Tipo cargo', 'remuneracionbruta_mensual']
PersonalContratohonorariosDICT    = deseadas+['remuliquida_mensual','tipo_pago','num_cuotas','remuneracionbruta']

if __name__ == '__main__':
    df = pd.read_csv(f"TA_PersonalPlanta.csv", low_memory=False,sep=";",encoding="latin",usecols=PersonalPlantaDICT)
    df.to_excel("TA_PersonalPlanta.csv", index=False)