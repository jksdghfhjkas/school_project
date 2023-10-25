import requests
import asyncio


app_id = 'ae503a9e809c10ec2d6a2fdda6737a49'
url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + app_id

cities = ["London",
"London"]

user_sity = []

async def RequestGetOne(url, cities, user_sity):                                                                   
    user_sity.append(requests.get(url.format(cities[0])).json())
    

async def RequestGetTwo(url, cities, user_sity):
    user_sity.append(requests.get(url.format(cities[1])).json())


async def main():
    task1 = asyncio.create_task(RequestGetOne(url, cities, user_sity))
    task2 = asyncio.create_task(RequestGetOne(url, cities, user_sity))
    await task1, task2

asyncio.run(main())

for i in user_sity:
    print(i)


