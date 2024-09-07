import os
import csv
import lightkurve as lk
import numpy as np

FOLDER_PATH = "./Positive"
SAVE_PATH = "Planets.csv"

fits_list = os.listdir(FOLDER_PATH)

total_fits = len(fits_list)

print("Se procesaran {} archivos".format(total_fits))

counter = 0

#Este bloque s epodría encerrar en una función
for fits_file in fits_list:
    path = "{}/{}".format(FOLDER_PATH, fits_file)
    lc = lk.read(path)
    if (len(lc) >= 4100):
        counter = counter + 1
        if (counter%50==0):
            print("Processados {} correctamente de {}".format(counter, total_fits))
        flatten_lc = lc.remove_nans().flatten(window_length=401)
        flux = np.array(flatten_lc.flux.value[0:4000] - 1)
        with open(SAVE_PATH, 'a', newline='\n') as f:
            writer = csv.writer(f)
            writer.writerow(flux)

fits_corruptos = total_fits - counter

print("De los {} archivos, se han Procesado {} correctamente.\n{} no cumplian los parametros establecidos".format(total_fits, counter, fits_corruptos))

