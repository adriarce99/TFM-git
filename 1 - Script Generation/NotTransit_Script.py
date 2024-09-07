import csv
import os
import stat
import sys

_WGET_CMD = ("wget -q -nH --cut-dirs=6 -r -l0 -c -N -np -erobots=off -R 'index*' -A _llc.fits")
_BASE_URL = "http://archive.stsci.edu/pub/kepler/lightcurves"

def main():

    kepler_csv_file = "Not_Transit.csv"
    download_dir = "./Not_Transit"
    output_file = "get_Not_Transit.sh"

    #Lectura de los Objetivos
    kepids = set()
    with open(kepler_csv_file) as f:
        reader = csv.DictReader(row for row in f if not row.startswith("#"))
        for row in reader:
            kepids.add(row["kepid"])
    
    num_kepids = len(kepids)

    #Creación scritps de descarga
    with open(output_file, "w") as f:
        f.write("#!/bin/sh\n")
        f.write("echo 'Dowloading {} Kepler targets to {}'\n".format(
            num_kepids, download_dir))

        for i, kepid in enumerate(kepids):
            print (str(i) + " " + kepid)
            if i and not i%10:
                f.write("echo 'Downloaded {}/{}'\n".format(i, num_kepids))
            
            kepid = "{0:09d}".format(int(kepid))
            subdir = "{}/{}".format(kepid[0:4], kepid)
            download_dir_kepid = download_dir
            url = "{}/{}/".format(_BASE_URL, subdir)
            f.write("{} -P {} {}\n".format(_WGET_CMD, download_dir_kepid, url))

        f.write("echo 'Finished downloading {} Kepler targets to {}'\n".format(
            num_kepids, download_dir))
    
    #Haciendo ejecutable el script
    os.chmod(output_file, stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)

    print("{} Kepler targets will be downloaded to {}".format(
      num_kepids, output_file))
    print("To start download, run:\n  {}".format("./" + output_file
                                               if "/" not in output_file
                                               else output_file))


if __name__ == "__main__":
  main()
