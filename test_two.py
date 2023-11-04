import requests 
import json
from bs4 import BeautifulSoup
from colorama import Fore

from time import ctime, time

import asyncio
import aiohttp
from translate import Translator

ForeCast_URL = 'https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid=' + 'ae503a9e809c10ec2d6a2fdda6737a49' + '&units=metric&lang=ru'
INFO = []
TRANSLATOR = Translator(to_lang="Russian")




async def Transcript_forecast(response_json, name_sity, Slice):
    global INFO, TRANSLATOR
    print(str(response_json))


    # for value in response_json[Slice]:
    #     INFO.append({
    #         'sity': name_sity,
    #         'temp': value['main']['temp'],
    #         'image': value['weather'][0]['icon'],
    #         'wind' : value['wind']['speed'],
    #         'cloud' : value['weather'][0]['main'],
    #         'date': value['dt_txt']

    #     })

async def Start_Transcript_forecast(response_json, name_sity):
    set_task = []
    for count in range(0, 41, 10):
        # set_task.append(asyncio.create_task(Transcript_forecast(response_json['list'], name_sity, slice(count - 10, count))))
        set_task.append(Transcript_forecast(response_json['list'], name_sity, slice(count - 10, count)))
    await asyncio.gather(*set_task)

def Forecast_Parser(coordinate, namesity):
    response = requests.get(ForeCast_URL.format(*coordinate))
    if response.status_code == 200:
        response_json = json.loads(response.text)
        if namesity == None: namesity = f'lat: {coordinate[0]}, long: {coordinate[1]}'
        asyncio.run(Start_Transcript_forecast(response_json, namesity))
    
    else: 
        print(Fore.RED + str(response.status_code) + Fore.WHITE)


Forecast_Parser([1, 1], None)
print(Fore.GREEN + str(INFO) + Fore.WHITE)
print(len(INFO))
