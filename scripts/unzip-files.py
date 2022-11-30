#!/usr/bin/env python3

import zipfile
from pathlib import Path
from glob import glob

zip_files = glob("{}/data/*/*.zip".format(Path(__file__).resolve().parent.parent))

where = "UDI"
when = "PLV"

for zip in zip_files:
    zipname = zip.rsplit("/")[-1]
    date = zipname[7:-4]
    zipdir = zip[:-len(zipname)]
    with zipfile.ZipFile(zip,"r") as zip_ref:
        txtname = "{}_{}_{}.txt".format(where, when, date)
        print("Extracting file {} into directory {}".format(txtname, zipdir))
        zip_ref.extract(txtname, zipdir)