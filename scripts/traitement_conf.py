import pandas as pd
import json
from pathlib import Path
from IPython.display import display

# json template:
#{  [annee: [ {"month":mois
#               "departs": [ {"code":code ....},
#                          ]
#               "nature_eau_conf_bacterio": [{"domaineparconf": 0-75, "%eso": , ...}, {"groupe":75-80, ....}]
#               "nature_eau_conf_chimique": [{"domaineparconf": 0-75, "%eso": , ...}, {"groupe":75-80, ....}]
# 
#            ]
#   ] 
# }

# liste des années à étudier
annees = ["2016", "2017", "2018", "2019", "2020", "2021"] 

#annees = ["2016"]

# renvoie un dictionnaire contenant le mois et une liste de dictionnaires 
# des données de chaque départements pour le mois en question
def resultats_departs_mois(donnees, mois):
    donnees_departs = []
    #liste des codes des départements
    departs = donnees["cddept"].unique()
    for code in range(len(departs)):
        depart = departs[code]
        donnees_depart = {"cddept": depart}
        total_row = len(donnees[(donnees["cddept"]==depart)])
        donnees_depart['conformbacterio'] = 100*len(donnees[(donnees["plvconformitebacterio"]=="C")][(donnees["cddept"]==depart)]) / total_row
        donnees_depart['conformchimique'] = 100*len(donnees[(donnees["plvconformitechimique"]=="C")][(donnees["cddept"]==depart)]) / total_row
        #donnees_depart['conformrefbactreio'] = 100*len(donnees[(donnees["plvconformiterefbacterio"]=="C")][(donnees["cddept"]==depart)]) / total_row
        #donnees_depart['conformrefchimique'] = 100*len(donnees[(donnees["plvconformiterefchimique"]=="C")][(donnees["cddept"]==depart)]) / total_row
        donnees_departs.append(donnees_depart)
    return donnees_departs

# REnvoie le dict des pourcentage de sources d'eau des departelents de la liste list_depart
def type_eau(donnees, list_dprt, min, max):
    df=donnees[donnees['cddept'].isin(list_dprt)]
    total_row = len(df)
    ESO = 100*len(df[(df['inae']=='ESO')]) / total_row if total_row!=0 else 0
    EMI = 100*len(df[(df['inae']=='EMI')]) / total_row if total_row!=0 else 0
    ESU = 100*len(df[(df['inae']=='ESU')]) / total_row if total_row!=0 else 0
    MER = 100*len(df[(df['inae']=='MER')]) / total_row if total_row!=0 else 0
    return {"domaineparconf":str(min)+"-"+str(max),"ESO":ESO,"EMI":EMI,"ESU":ESU,"MER":MER}

# Renvoie un  couple de listes contenant chacun les codes de départements
# ayant un pourcentage de conformité entre min et max
def list_depart_conf(departs, min, max):
    list_bacterio=[]
    list_chimique=[]
    for depart in departs:
        if min < int(depart["conformbacterio"]) <= max:
            list_bacterio.append(depart["cddept"])
        if min < int(depart["conformchimique"]) <= max:
            list_chimique.append(depart["cddept"])
    
    return (list_bacterio, list_chimique)

# Renvoie 
def nature_eau(donnees, departs, mois):
    nature_eau_conf_bacterio = []
    nature_eau_conf_chimique = []
    #print(type_eau(donnees,list_depart_conf(departs,0,75)[0], 0, 75))
    nature_eau_conf_bacterio.append(type_eau(donnees,list_depart_conf(departs,0,75)[0],0, 75))
    nature_eau_conf_chimique.append(type_eau(donnees,list_depart_conf(departs,0,75)[1],0,75))
    min = 75
    max = 80
    for i in range(5):
        nature_eau_conf_bacterio.append(type_eau(donnees,list_depart_conf(departs,min,max)[0],min, max))
        nature_eau_conf_chimique.append(type_eau(donnees,list_depart_conf(departs,min,max)[1],0,75))
        min += 5
        max += 5
    return {"mois":mois, "departs": departs,"nature_eau_conf_bacterio":nature_eau_conf_bacterio, "nature_eau_conf_chimique":nature_eau_conf_chimique}
    
    
    

# Génère des fichiers json pour chaque année  des années à étudiers selon le template json
# et les mettent dans le répertoire output_data prêtes à l'utilisation 
def main():
    path_to_repo_input = str(Path(__file__).resolve().parent.parent) + "/extracted_data/"
    path_to_repo_output = str(Path(__file__).resolve().parent.parent) + "/json_data/"
    donnees_annees = []
    for annee in annees:
        donnees_annee = []
        donnees = pd.read_csv(path_to_repo_input+'UDI_PLV_{}.txt'.format(annee), low_memory=False)

        # projection sur les colonnes essentielles
        donnees = donnees[['cddept','dateprel','plvconformitebacterio', 'plvconformitechimique', 'inae']]
        # nouvelle colone contenant le mois qu'on va la prendre au lieu de dateprlev
        donnees["mois"] = donnees.dateprel.str.split('-').str[1].astype('int')
        donnees = donnees[donnees.columns.difference(['dateprel'])]
        # ajouter les résultats de prélèvement des mois de l'année
        for mois in range(1,13):
            donnees_mois = donnees[donnees["mois"]==mois]
            donnees_annee.append(nature_eau(donnees_mois, resultats_departs_mois(donnees_mois, mois), mois))
        donnees_annees.append({annee:donnees_annee})
        #transformer le dictionaire en fichier json et le mettre dans json_data
        with open(path_to_repo_output+"Result_conformité.json", "w") as outfile:
            json.dump(donnees_annees, outfile)

if __name__ == '__main__':
    main()
