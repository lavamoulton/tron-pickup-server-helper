import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PICKUP_BOT = os.getenv('PICKUP_BOT')
OUTPUT_FILE = os.getenv('OUTPUT')

class myClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.author.name != PICKUP_BOT:
            return
        else:
            if message.content[0:9] == 'WST ready':
                split_message = message.content.split('\n')

                print(split_message)

                captain1 = self.get_user(int(split_message[1].lstrip('Team 1 captain: <@').rstrip('>')))
                captain2 = self.get_user(int(split_message[2].lstrip('Team 2 captain: <@').rstrip('>')))

                print(captain1)
                print(captain2)

                everyone_else = split_message[3].lstrip('Everyone else: ').split(',')

                for i in range(len(everyone_else)):
                    everyone_else[i] = self.get_user(int(everyone_else[i].lstrip('<@').rstrip('>')))

                print(everyone_else)

                write_WST(captain1, captain2, everyone_else)


def write_WST(captain1, captain2, everyone_else):
    f = open(OUTPUT_FILE, 'w')
    f.write('Captain 1: ' + captain1.display_name + '\n')
    f.write('Captain 2: ' + captain2.display_name + '\n')
    for player in everyone_else:
        f.write('Players: ' + player.display_name + ', ')
    f.close()


client = myClient()
client.run(TOKEN)