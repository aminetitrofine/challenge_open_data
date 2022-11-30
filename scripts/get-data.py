#!/usr/bin/env python3

import requests
import sys
from pathlib import Path

url_by_year = {
    2016 : "https://www.data.gouv.fr/fr/datasets/r/c3848a32-ab35-4d6c-b056-6511727e0a3c",
    2017 : "https://www.data.gouv.fr/fr/datasets/r/33aea374-91b8-4e7b-ad9c-dcc9f33a91d4",
    2018 : "https://www.data.gouv.fr/fr/datasets/r/782bff05-56e5-407a-beec-b80c581c799b",
    2019 : "https://www.data.gouv.fr/fr/datasets/r/c7c676c4-fce3-476e-8e94-3542e0444b73",
    2020 : "https://www.data.gouv.fr/fr/datasets/r/29a86084-4333-45e3-ab55-fae8be5ae6a5",
    2021 : "https://www.data.gouv.fr/fr/datasets/r/79cbb55b-ce30-4192-bd9f-b9002ad0ab06",
    202201 : "https://www.data.gouv.fr/fr/datasets/r/c4424700-cf7a-4c1e-8a5e-81a0c3f8f208",
    202202 : "https://www.data.gouv.fr/fr/datasets/r/810c585b-26bf-4879-86e5-f9c2d23b6a38",
    202203 : "https://www.data.gouv.fr/fr/datasets/r/0491de21-8a73-4d9b-b4ee-5bfd672f5939",
    202204 : "https://www.data.gouv.fr/fr/datasets/r/aba6a1c9-6b39-40b8-88d7-5ffe8cd9693c",
    202205 : "https://www.data.gouv.fr/fr/datasets/r/be918f38-61eb-4921-9d8b-a8e9d20e2585",
    202206 : "https://www.data.gouv.fr/fr/datasets/r/472efcf7-fda3-4304-bea3-368789402fc0",
    202207 : "https://www.data.gouv.fr/fr/datasets/r/c2a50515-d7ff-4ade-9770-02af6ee0ba37",
    202208 : "https://www.data.gouv.fr/fr/datasets/r/86c31a2c-c2bb-4a68-9158-6a6e21b076f8",
    202209 : "https://www.data.gouv.fr/fr/datasets/r/24caeff4-a56a-4230-98a6-de34bbd3d409"
}

path_to_repo = Path(__file__).resolve().parent.parent

year = 0
if len(sys.argv)== 1:
    year = input("Argument non trouvé. Entrez l'année : ")
else :
    year = sys.argv[1]

name = "eaurob-{}.zip".format(year)
URL = url_by_year[int(year)]

print("URL : ", URL)
response = requests.get(URL)

if (response.status_code == 200) :
    if len(year) == 6:
        year = year[:4]
    with open("{}/data/{}/{}".format(path_to_repo, year, name), "wb") as zipfile:
        zipfile.write(response.content)
else :
    print("Error occured. Status code is : ", response.status_code)