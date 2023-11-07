import time
import pandas as pd
from pyswip import Prolog

#creazione delle clausole
def create_kb() -> Prolog:
    prolog = Prolog()

    prolog.consult("kb/facts.pl")
    kb=prolog

    prolog.assertz("same_temperature(Temp, ID2) :- temperature(ID2, Temp)")
    prolog.assertz("num_of_day_with_same_temp(Temp, Count) :-findall(Temp, same_temperature(Temp,ID2), L), length(L, Count)")
    prolog.assertz("winter1(ID) :- id(_,M,_,_,ID),M<3")
    prolog.assertz("winter2(ID) :- id(_,M,_,_,ID),M=12")
    prolog.assertz("spring(ID) :- id(_,M,_,_,ID),M>2,M<6")
    prolog.assertz("summer(ID):- id(_,M,_,_,ID),M>5,M<9")
    prolog.assertz("autumn(ID):- id(_,M,_,_,ID),M>8,M<12")
    prolog.assertz("cool(ID) :- apparent_temperature(ID,Temp),Temp<21,Temp>10")
    prolog.assertz("mild(ID) :- apparent_temperature(ID,Temp),Temp<26,Temp>20")
    prolog.assertz("warm(ID) :- apparent_temperature(ID,Temp),Temp<31,Temp>25")
    prolog.assertz("hot(ID) :- apparent_temperature(ID,Temp),Temp>30,Temp<40")
    prolog.assertz("sweltering(ID) :- apparent_temperature(ID,Temp),Temp>40")
    prolog.assertz("cold(ID) :- apparent_temperature(ID,Temp),Temp<11,Temp>0")
    prolog.assertz("freezing(ID) :- apparent_temperature(ID,Temp),Temp<1")

    prolog.assertz("avg_windy(Year,Avg) :- findall(Speed, (windspeed(Id, Speed), id(Year, _, _, _, Id)), SpeedList),length(SpeedList, Count),sum_list(SpeedList, Sum),Avg is Sum / Count")
    prolog.assertz("avg_windm(Month,Avg) :- findall(Speed, (windspeed(Id, Speed), id(_,Month, _, _, Id)), SpeedList),length(SpeedList, Count),sum_list(SpeedList, Sum),Avg is Sum / Count")
    prolog.assertz("avg_tempy(Year,Avg) :- findall(Temp, (temperature(Id,Temp), id(Year, _, _, _, Id)), TempList),length(TempList, Count),sum_list(TempList, Sum),Avg is Sum / Count")
    prolog.assertz("avg_tempm(Month,Avg) :- findall(Temp, (temperature(Id,Temp), id(_,Month, _, _, Id)), TempList),length(TempList, Count),sum_list(TempList, Sum),Avg is Sum / Count")
    prolog.assertz("min_wind(Min) :- findall(Speed, windspeed(_, Speed), SpeedList), min_list(SpeedList,Min)")
    prolog.assertz("max_wind(Max) :- findall(Speed, windspeed(_, Speed), SpeedList), max_list(SpeedList,Max)")
    prolog.assertz("min_temp(Min) :- findall(Temp, temperature(_, Temp), TempList), min_list(TempList,Min)")
    prolog.assertz("max_temp(Max) :- findall(Temp, temperature(_,Temp), TempList), max_list(TempList,Max)")
    prolog.assertz("conta_occorrenzew(Id,Count) :- windspeed(Id,X),findall(Speed,windspeed(_,Speed),SpeedList), aggregate_all(count, member(X,SpeedList), Count)")
    prolog.assertz("conta_occorrenzet(Id,Count) :- temperature(Id,X),findall(Temp,temperature(_,Temp),TempList), aggregate_all(count, member(X,TempList), Count)")
    prolog.assertz("trova_posizione(Elemento, Lista, Posizione) :- nth1(Posizione, Lista, Elemento )")
    prolog.assertz("most_frequency_speed(Speed) :- findall(Freq, conta_occorrenzew(Id,Freq),Freqlist), max_list(Freqlist,Max), trova_posizione(Max,Freqlist,Id),windspeed(Id,Speed)")
    prolog.assertz("most_frequency_temp(Temp) :- findall(Freq, conta_occorrenzet(Id,Freq),Freqlist), max_list(Freqlist,Max), trova_posizione(Max,Freqlist,Id),temperature(Id,Temp)")
    
    with open('kb/query_numeriche.pl', 'w') as file:
        for result in prolog.query("avg_windy(2006,Avg)"):
            file.write('average wind speed in 2006= {}\n'.format(str(result["Avg"])))
        file.write('most frequency wind speed= {}\n'.format(str(list(prolog.query(f"most_frequency_speed(Speed)"))[0]["Speed"])))
        file.write('most frequency temperature= {}\n'.format(str(list(prolog.query(f"most_frequency_temp(Temp)"))[0]["Temp"])))
        for result in prolog.query("avg_windm(4,Avg)"):
            file.write('average wind speed in march={}\n'.format(str(result["Avg"])))
        for result in prolog.query("avg_tempy(2006,Avg)"):
            file.write('average temperature in 2006={}\n'.format(str(result["Avg"])))
        for result in prolog.query("avg_tempm(4,Avg)"):
            file.write('average temperature in march={}\n'.format(str(result["Avg"])))
        for result in prolog.query("min_wind(Min)"):
            file.write('minimum wind speed={}\n'.format(str(result["Min"])))
        for result in prolog.query("max_wind(Max)"):
            file.write('maximum wind speed={}\n'.format(str(result["Max"])))
        for result in prolog.query("max_temp(Max)"):
            file.write('maximum temperature={}\n'.format(str(result["Max"])))
        for result in prolog.query("min_temp(Min)"):
            file.write('minimum temperature={}\n'.format(str(result["Min"])))

    
    with open('kb/winter.pl', 'w') as file:
        for result in prolog.query("winter1(ID)"):
            file.write('{}\n'.format(str(result["ID"])))
        for result in prolog.query("winter2(ID)"):
            file.write('{}\n'.format(str(result["ID"])))
    with open('kb/spring.pl', 'w') as file:
        for result in prolog.query("spring(ID)"):
            file.write('{}\n'.format(str(result["ID"])))
    with open('kb/summer.pl', 'w') as file:
        for result in prolog.query("summer(ID)"):
            file.write('{}\n'.format(str(result["ID"])))
    with open('kb/autumn.pl', 'w') as file:
        for result in prolog.query("autumn(ID)"):
            file.write('{}\n'.format(str(result["ID"])))
    with open('kb/hot.pl', 'w') as file:
        for result in prolog.query("hot(ID)"):
            file.write('{}\n'.format(str(result["ID"])))
    with open('kb/sweltering.pl', 'w') as file:
        for result in prolog.query("sweltering(ID)"):
            file.write('{}\n'.format(str(result["ID"])))
    with open('kb/warm.pl', 'w') as file:
        for result in prolog.query("warm(ID)"):
            file.write('{}\n'.format(str(result["ID"])))
    with open('kb/mild.pl', 'w') as file:
        for result in prolog.query("mild(ID)"):
            file.write('{}\n'.format(str(result["ID"])))
    with open('kb/cool.pl', 'w') as file:
        for result in prolog.query("cool(ID)"):
            file.write('{}\n'.format(str(result["ID"])))
    with open('kb/cold.pl', 'w') as file:
        for result in prolog.query("cold(ID)"):
            file.write('{}\n'.format(str(result["ID"])))
    with open('kb/freezing.pl', 'w') as file:
        for result in prolog.query("freezing(ID)"):
            file.write('{}\n'.format(str(result["ID"])))        
            
   
def ottieni_ids(file_name):
    with open(file_name, 'r') as file:
        ids = [line.strip() for line in file]

    return ids
#creazione del dataset con la nuove feature
def produce_working_dataset(kb: Prolog, path: str, final=False):
    df=pd.read_csv("data/working_dataset/New_weather_history.csv")
    season= {}
    autumn = ottieni_ids("kb/autumn.pl")
    spring=ottieni_ids("kb/spring.pl")
    summer=ottieni_ids("kb/summer.pl")
    winter=ottieni_ids("kb/winter.pl")
    hot=ottieni_ids("kb/hot.pl")
    sweltering=ottieni_ids("kb/sweltering.pl")
    warm=ottieni_ids("kb/warm.pl")
    mild=ottieni_ids("kb/mild.pl")
    cool=ottieni_ids("kb/cool.pl")
    cold=ottieni_ids("kb/cold.pl")
    freezing=ottieni_ids("kb/freezing.pl")
    
    set_autumn = set(map(int,autumn))
    set_spring = set(map(int,spring))
    set_summer = set(map(int,summer))
    set_winter = set(map(int,winter))
    set_hot= set(map(int,hot))
    set_sweltering= set(map(int,sweltering))
    set_warm= set(map(int,warm))
    set_mild= set(map(int,mild))
    set_cold=set(map(int,cold))
    set_cool= set(map(int,cool))
    set_freezing= set(map(int,freezing))

    df['autumn'] = df['ID'].isin(set_autumn).astype(int)
    df['spring'] = df['ID'].isin(set_spring).astype(int)
    df['summer'] = df['ID'].isin(set_summer).astype(int)
    df['winter'] = df['ID'].isin(set_winter).astype(int)
    df['hot'] = df['ID'].isin(set_hot).astype(int)
    df['sweltering'] = df['ID'].isin(set_sweltering).astype(int)
    df['warm'] = df['ID'].isin(set_warm).astype(int)
    df['mild'] = df['ID'].isin(set_mild).astype(int)
    df['cold'] = df['ID'].isin(set_cold).astype(int)
    df['cool'] = df['ID'].isin(set_cool).astype(int)
    df['freezing'] = df['ID'].isin(set_freezing).astype(int)
    
    df.loc[df['winter'] == 1, 'season'] = 1
    df.loc[df['summer'] == 1, 'season'] = 3
    df.loc[df['autumn'] == 1, 'season'] = 4
    df.loc[df['spring'] == 1, 'season'] = 2
    df.loc[df['cold'] == 1, 'wind_chill'] = 'cold'
    df.loc[df['hot'] == 1, 'wind_chill'] = 'hot'
    df.loc[df['sweltering'] == 1, 'wind_chill'] = 'sweltering'
    df.loc[df['warm'] == 1, 'wind_chill'] = 'warm'
    df.loc[df['mild'] == 1, 'wind_chill'] = 'mild'
    df.loc[df['cool'] == 1, 'wind_chill'] = 'cool'
    df.loc[df['freezing'] == 1, 'wind_chill'] = 'freezing'
    del df['winter']
    del df['summer']
    del df['autumn']
    del df['spring']
    del df['cold']
    del df['hot']
    del df['sweltering']
    del df['warm']
    del df['mild']
    del df['cool']
    del df['freezing']
    df['season']=df['season'].apply(int)
    df.to_csv('data/working_dataset/dataset_operativo.csv', index = False)

def main():
    #create_prolog_kb()
    knowledge_base = create_kb()
    produce_working_dataset(knowledge_base, "kb/New_weather_history.csv")
    print("Created generated_dataset")

main()