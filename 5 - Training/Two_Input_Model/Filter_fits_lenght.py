import lightkurve as lk
import numpy as np
import json
import os

def escribeJson(data_folder, is_planet):

    period = np.linspace(1, 30, 5000)
    json_folder = "./Data_json/"

    fits_list = os.listdir(data_folder)
    counter = 0
    total_files = len(fits_list)

    #Escritura de los documentos
    for fits_file in fits_list:
        counter += 1
        if (counter % 100 == 0):
            print("{} de {} procesados".format(counter, total_files))
        #Comprueba primero si el fichero cumple los requesitos
        lc = lk.read(data_folder + fits_file)
        lc_lenght = len(lc)

        if (lc_lenght >= 4100):

            #Array de flujo normalizado
            flatten_lc = lc.remove_nans().flatten(window_length=401)
            lc_flux = np.array((flatten_lc.flux.value[0:4000] - 1)*100)
            flux = []
            for value in lc_flux:
                flux.append(value.item())

            #Array de periodos
            bls = lc.to_periodogram(method='bls', period=period, frequency_factor=500)
            lc_power = np.array(bls.power / bls.max_power)
            power = []
            for value in lc_power:
                power.append(value.item())

            #Creación del documento
            documento = {
                "name" : lc.label,
                "is_planet" : is_planet,
                "flux" : flux,
                "power" : power
            }

            writing_file = json_folder + fits_file.strip(".fits") + ".json"
            with open(writing_file , "w") as outfile:
                json.dump(documento, outfile)
    
    print('Escritura y filtrado finalizados')


planet_path = "../Data/Positive/"
false_positive_path = "../Data/Negative/"
not_transit_path = "../Data/Not_Transit/"

filtered_data_folder = "./Train_Data/"

escribeJson(data_folder=planet_path, is_planet=1)
escribeJson(data_folder=false_positive_path, is_planet=0)
escribeJson(data_folder=not_transit_path, is_planet=0)
