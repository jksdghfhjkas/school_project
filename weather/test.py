import requests
import asyncio
import json
import aiohttp
from time import time

URL = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + 'ae503a9e809c10ec2d6a2fdda6737a49'
USER_SITY = []

async def Request_Get_Weather(city, session):
    async with session.get(URL.format(city), proxy=None) as response:
        response_json = json.loads(await response.text())
        
        if response_json['cod'] != '404':
            print(response_json)
            # USER_SITY.append({
            #     'city': city,
            #     'temp': response_json['main']['temp'],
            #     'image': response_json['weather'][0]['icon']
            # })

async def Request_User_Weather(cityes):
    city_tasks = []
    async with aiohttp.ClientSession() as session:
        for city in cityes:
            city_tasks.append(asyncio.create_task(Request_Get_Weather(city, session)))
        await asyncio.gather(*city_tasks)


sities = ['london', 'london']

for i in range(10):
    time_st = time()
    asyncio.run(Request_User_Weather(sities))
    print(time_st - time())