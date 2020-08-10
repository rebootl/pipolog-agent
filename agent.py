#!/usr/bin/env python3
#
#
import os
import asyncio
import aiofiles
import aiohttp
import socket
import datetime
import binascii

import config

### output (to server)

headers = {
    'Content-type': 'application/json',
    'Authorization': 'Basic ' + config.API_KEY
}

if config.SSL_FINGERPRINT:
    ssl = aiohttp.Fingerprint(binascii.unhexlify(config.SSL_FINGERPRINT))
else:
    ssl = False

async def post_data(api_url, data):
    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            await session.post(api_url, json=data, ssl=ssl)
            #async with session.post(api_url, json=data, ssl=ssl) as response:
            #    print(response)
        except OSError as e:
            print("OSERROR: ", e)

async def prepare_logdata(type, name, text):
    await post_data(config.API_URL_LOG, {
        'name': name,
        'text': text,
        'agent_timestamp': str(datetime.datetime.now()),
        'host': socket.gethostname(),
    })

### input (local)

async def read_pipe(pipe_def):
    print('Start reader: ' + pipe_def['name'])
    while True:
        async with aiofiles.open(pipe_def['path'], 'r') as afp:
            while True:
                data = await afp.readline()
                if len(data) == 0:
                    break
                print(data, end = '')
                await prepare_logdata(
                    'logline',
                    pipe_def['name'],
                    data
                )

async def main():
    await asyncio.gather(*[ read_pipe(p) for p in config.IN_PIPES_DEF])

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

loop.run_until_complete(main())
loop.close()
#try:
#    loop.run_until_complete(main())
#finally:
#    # Shutting down and closing file descriptors after interrupt
#    loop.run_until_complete(loop.shutdown_asyncgens())
#    loop.close()
#    print('Exited')
