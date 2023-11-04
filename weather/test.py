import requests
import asyncio
import json
import aiohttp
from time import time, sleep

async def wrapper():
    await asyncio.sleep(10)

async def main(count):
    print(f'start: {count}')
    await sleep(10)
    print(f'stop: {count}')

async def start():
    task = []
    for count in range(10):
        task.append(asyncio.create_task(main(count)))
    await asyncio.wait(task)

# asyncio.run(start())

from datetime import date
today = date.today()
print(today)
