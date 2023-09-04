import datetime
import pandas as pd
import csv

#creazione del file contenente i fatti
def load_data_in_kb(weather:pd.DataFrame,kb=None,):
    prolog_file = None
    map={'Partly Cloudy':1, 'Mostly Cloudy':2, 'Overcast':3, 'Foggy':4,
 'Breezy and Mostly Cloudy':5, 'Clear':6, 'Breezy and Partly Cloudy':7,
 'Breezy and Overcast':8, 'Humid and Mostly Cloudy':9, 'Humid and Partly Cloudy':10,
 'Windy and Foggy':11, 'Windy and Overcast':12, 'Breezy and Foggy':13,
 'Windy and Partly Cloudy':14, 'Breezy':15, 'Dry and Partly Cloudy':16,
 'Windy and Mostly Cloudy':17, 'Dangerously Windy and Partly Cloudy':18, 'Dry':19,
 'Windy':20, 'Humid and Overcast':21, 'Light Rain':22, 'Drizzle':23, 'Windy and Dry':24,
 'Dry and Mostly Cloudy':25, 'Breezy and Dry':26, 'Rain':27}
    if kb is None:
            prolog_file = open("kb/facts.pl", "w")
            action = lambda fact_list: assert_all_in_file(fact_list, prolog_file)
    else:
            action = lambda fact_list: assert_all(fact_list, kb)
    action([":-style_check(-discontiguous)"])
    weather['Summary']=weather['Summary'].replace(map)
    
    weather['Daily Summary']=weather['Daily Summary'].str.replace(' ','',regex=True)
    weather['Daily Summary']=weather['Daily Summary'].str.slice(0,-1)
    #Inserimento dati per il Meteo
    for index, row in weather.iterrows():
        data = f"{int(row['Y'])},{int(row['M'])},{int(row['D'])},{int(row['HH'])},0,0"
        info = [f"id({datetime_to_prolog_fact(data)},{row['ID']})",
                    f"summary({row['ID']},{row['Summary']})",
                    f"precipitation_type({row['ID']},'{row['Precip Type']}')",
                    f"temperature({row['ID']},{row['Temperature (C)']})",
                    f"apparent_temperature({row['ID']},{row['Apparent Temperature (C)']})",
                    f"humidity({row['ID']},{row['Humidity']})",
                    f"windspeed({row['ID']},{row['Wind Speed (km/h)']})",
                    f"wind_bearing({row['ID']},{row['Wind Bearing (degrees)']})",
                    f"visibility({row['ID']},{row['Visibility (km)']})",
                    f"pressure({row['ID']},{row['Pressure (millibars)']})",
                    f"daily_summary({row['ID']},'{row['Daily Summary']}')"]
        action(info)
    if kb is not None:
        prolog_file.close()


def assert_all(info, kb):
    for fact in info:
        kb.asserta(fact)


def assert_all_in_file(info, kb_file):
    kb_file.writelines(".\n".join(info) + ".\n")




#formattazione della data
def datetime_to_prolog_fact(datetime_str: str) -> str:
    dt = date_time_from_dataset(datetime_str)
    datetime_str = "date({},{},{},{},{},{})".format(dt.year, dt.month, dt.day,dt.hour,0,0)
    return f"{datetime_str}"


def date_time_from_dataset(datetime_str: str) -> datetime:
    return datetime.datetime.strptime(datetime_str, '%Y,%m,%d,%H,%M,%S')
def create_prolog_kb():
    weather = pd.read_csv("data/working_dataset/New_Weather_history.csv")
    load_data_in_kb(weather)
def main():
    create_prolog_kb()
main()
  
                
'''  f"apparent_temperature({datetime_to_prolog_fact(data)},{row['Apparent Temperature (C)']})",
                f"humidity({datetime_to_prolog_fact(data)},{row['Humidity']})",
                f"windspeed({datetime_to_prolog_fact(data)},{row['Wind Speed (km/h)']})",
                f"windbearing({datetime_to_prolog_fact(data)},{row['Wind Bearing (degrees)']})",
                f"visibility({datetime_to_prolog_fact(data)},{row['Visibility (km)']})",
                f"pressure({datetime_to_prolog_fact(data)},{row['Pressure (millibars)']})",
                f"dailysummary({datetime_to_prolog_fact(data)},'{row['Daily Summary']}')" 
                Summary,Precip Type,Temperature (C),Apparent Temperature (C),Humidity,Wind Speed (km/h),Wind Bearing (degrees),Visibility (km),Loud Cover,Pressure (millibars),Daily Summary
                '''