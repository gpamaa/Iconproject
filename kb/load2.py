import csv

from numpy import nanvar
from pyswip import Prolog

# leggo il file CSV dei clienti
# newline vuoto perchè rilevato automaticamente
with open('.\data\working_dataset\New_weather_history.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    #salto la prima riga
    next(reader)
    # creo un fatto Prolog per ogni riga del dataset
    facts = []
    for row in reader:
        # forma: nome_fatto(argomento1, argomento2, ...)
        fact = f"{'weather'}({', '.join(row[0:])})."
        facts.append(fact)
        
# scrivo i fatti Prolog in un file .pl
with open('kb\regole2.pl', 'w') as plfile:
    plfile.write('\n'.join(facts))