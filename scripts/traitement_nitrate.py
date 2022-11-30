import pandas as pd
from pathlib import Path
import json



def main():
    path_to_repo_input = str(Path(__file__).resolve().parent.parent) + "/extracted_data/"
    path_to_repo_output = str(Path(__file__).resolve().parent.parent) + "/json_data/"
    #print(path_to_repo_input+ 'NiD_France_2020_Data_diffusion.xls')
    df1 = pd.read_excel(path_to_repo_input+ 'NiD_France_2020_Data_diffusion.xls',sheet_name='NiD_GW_Stat')
    df1=df1[df1["ND_Drinking"]==True]
    df1=df1[["ND_NatStatCode","Longitude","Latitude"]]
    df2 = pd.read_excel('NiD_France_2020_Data_diffusion.xls',sheet_name='NiD_GW_AnnConc')
    df2=df2[["ND_NatStatCode","ND_AvgAnnValue"]]
    df = pd.merge(df2,df1, on='ND_NatStatCode', how='inner')
    dff1 = pd.read_excel('NiD_France_2020_Data_diffusion.xls',sheet_name='NiD_SW_Stat')
    dff1=dff1[["ND_NatStatCode","Longitude","Latitude"]]
    dff2 = pd.read_excel('NiD_France_2020_Data_diffusion.xls',sheet_name='NiD_SW_AnnConc')
    dff2=dff2[["ND_NatStatCode","ND_AvgAnnValue"]]
    dff = pd.merge(dff2,dff1, on='ND_NatStatCode', how='inner')

    resultat = {"eau_souterraines":df.to_dict('records'), "eau_superficielles":dff.to_dict('records')}
    
    #transformer le dictionaire en fichier json et le mettre dans json_data
    with open(path_to_repo_output+"Result_nitrate.json", "w") as outfile:
            json.dump(resultat, outfile)

if __name__ == '__main__':
    main()