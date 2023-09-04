import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV, train_test_split, validation_curve

#Estrazione delle informazioni necessarie del file 'NYC weather'
def extract_weather():
    # Caricamento del dataset
    weather = pd.read_csv("data/old_dataset/weatherHistory.csv")
    # crea le nuove colonne vuote
   # crea le nuove colonne vuote
    weather['Y'] = ''
    weather['M'] = ''
    weather['D'] = ''
    weather['TIME'] = ''
    # rimuovi la colonna "time" originale
    for index, row in weather.iterrows():
        time = row['Formatted Date'].split(' ')
        date = time[0]
        time = time[1]
        year, month, day = date.split('-')
        weather.at[index, 'Y'] = year
        weather.at[index, 'M'] = month
        weather.at[index, 'D'] = day
        weather.at[index, 'TIME'] = time
    weather = weather.drop('Formatted Date', axis=1)
    weather['HH'] = ''

    # itera su ogni riga del dataframe e separa il tempo
    for index, row in weather.iterrows():
        hour,minutes,second = row['TIME'].split(':')
        
        # aggiorna le nuove colonne con i valori corretti
        weather.at[index, 'HH'] = hour

    # rimuovi la colonna "time" originale
    weather = weather.drop('TIME', axis=1)

    weather['Y'] = weather['Y'].astype(int)
    weather['M'] = weather['M'].astype(int)
    weather['D'] = weather['D'].astype(int)
    weather['HH']=weather['HH'].astype(int)


    # riordina le colonne in base all'ordine desiderato
    weather = weather.reindex(columns=['Y', 'M', 'D', 'HH'] + list(weather.columns[:-4]))

    

    # visualizza il dataframe risultante
    #
    '''f,ax = plt.subplots(figsize=(18, 18))
    data= weather.drop('Precip Type', axis=1)
    data= data.drop('Summary',axis=1)
    data= data.drop('Daily Summary',axis=1)
    sns.heatmap(data.corr(), annot=True, linewidths=.5, fmt= '.1f',ax=ax)
    plt.show()'''
    weather=weather.drop('Loud Cover',axis=1)
    weather.insert(0, 'ID', range(1, len(weather)+1))
   # weather.fillna(method='ffill', inplace=True)
    weather.to_csv("data/working_dataset/New_weather_history.csv", index=False, mode='w')

#Estrazione delle informazioni necessarie del file 'NYC Accidents'






def main():
    extract_weather()
    

main()