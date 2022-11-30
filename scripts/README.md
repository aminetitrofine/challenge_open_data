## Scripts

# get-data.py :
Ce script permet de récupérer le zipfile des résultats de l'analyse de l'eau de robinet concernant l'année passée en argument ou en input. 

En effet, si l'année est passée en argument le script est lancé pour s'exécuter sur l'argument. Sinon, il demande à l'utilisateur de passer l'année en input. 

Ceci permet de lancer le script avec run dans l'éditeur ainsi que de le lancer en ligne de commande comme indiqué ci-dessous : 
    $ python3 <path_to_script>/get-data.py 2021

Pour lancer le script sur plusieurs années en même temps, lancez le script get-all-data.sh :
    $ ./get-all-data.sh

N'bouliez pas d'ajouter les droits d'exécution au script avec la commande :
    $ chmod u+x get-all-data.sh


# unzip-files.py 
Ceci est un script qui permet d'extraire un type de fichier texte donné à partir du fichier zip qui le contient. L'extraction se fait sur tout les fichier zip contenus dans le répertoire data (récursivement). Le fichier extrait est mis dans le même répertoire que le fichier zip qui le contenait.