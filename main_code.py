import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client=discord.Client()

sad_words= ["sad","depressed", "depressing", "upset", "upsetting", "failure","die", "abnormal", "quit", "absurd", "awful"]

motivating_starters=["Hang in there", "Don’t give up", "Keep pushing", "Keep fighting!","Stay strong","Never give up","Never say ‘die’", "Come on! You can do it!"]

if "responding" not in db.keys():
        db["responding"] = True

def get_quote():
        response=requests.get("https://zenquotes.io/api/random")

        json_data= json.loads(response.text)

        quote=json_data[0]['q'] + "~" + json_data[0]['a']

        return (quote)

def update_quotes(motivating_quote):
        if "motivation" in db.keys():
                motivation=db["motivation"]
                motivation.append(motivating_quote)
                db["motivation"]=motivation
        else:
                db["motivation"]=[motivating_quote]

def delete_quotes(index):
        motivation=db["motivation"]
        if len(motivation) > index:
                del motivation[index]
                db["motivation"]=motivation

@client.event
async def on_ready():
        print('We are logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
        if message.author == client.user:
                return

        msg=message.content

        if msg.startswith('$quote'):
                quote=get_quote()
                await message.channel.send(quote)

        if db["responding"]:
                options=motivating_starters
                if "motivation" in db.keys():
                        options.extend(db["motivation"])

                if any(word in msg for word in sad_words):
                        await message.channel.send(random.choice(motivating_starters))

        if msg.startswith("$new"):
                motivating_quote=msg.split("$new ",1)[1]
                update_quotes(motivating_quote)
                await message.channel.send("New quote added")

        if msg.startswith("$del"):
                motivation=[]
                if "motivation" in db.keys():
                        index=int(msg.split("$del",1)[1])
                        delete_quotes(index)
                        motivation=db["motivation"]
                await message.channel.send(motivation)

        if msg.startswith("$list"):
                motivation=[]
                if "motivation" in db.keys():
                        motivation=db["motivation"]
                await message.channel.send(motivation)
        
        if msg.startswith("$responding"):
                value=msg.split("$responding ",1)[1]

                if value.lower()== "true":
                        db["responding"]= True
                        await message.channel.send("Responding")
                else:
                        db["responding"]= False
                        await message.channel.send(" Not Responding")

keep_alive()
client.run(os.getenv('TOKEN'))
