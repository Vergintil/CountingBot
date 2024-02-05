import discord
import os
import time
from replit import db
from KeepAlive import keep_alive

if not 'number' in db.keys():
    db['number'] = 0

print(db['number'])

connection = discord.Client()

currentNum = db['number']

dataWriteMode = None

isCounting = False

async def end_counting():
    global isCounting
    global currentNum

    isCounting = False

    currentNum = 0
    db['number'] = currentNum


async def increment():
    global currentNum
    currentNum += 1

    db['number'] = currentNum


async def start_counting(channel):
    global isCounting
    isCounting = True

    global currentNum

    while isCounting:
        await channel.send(currentNum)

        time.sleep(1)

        await increment()


async def celebrate(msg):
    await msg.channel.send(
        'Thank You For Contributing to Counting Bot. \n I never expected this to come so far. \n Honestly I would just like to give my heartfelt thanks to everyone who helped to make this possible.\n'
    )

    with open('Credits.txt') as f:
        send_msg = f.readlines()

        for line in send_msg:
            await msg.channel.send(line)


@connection.event
async def on_message(msg):
    if msg.author == connection.user:
        return
  
    if msg.content.startswith('~'):
        if msg.content.lower() == '~credits':
            await celebrate(msg)
      
        if msg.content.lower() == '~ymca_dance' and isCounting == False:
            print('work')
            await start_counting(msg.channel)
        elif msg.content.lower() == '~funny_joke':
            await end_counting()


@connection.event
async def on_ready():
    print('Connected!')


keep_alive()

connection.run(os.environ['TOKEN'])
