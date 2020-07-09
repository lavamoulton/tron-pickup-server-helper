#!/usr/bin/python3

import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PICKUP_BOT = os.getenv('PICKUP_BOT')
OUTPUT_WST = os.getenv('OUTPUT_WST')
OUTPUT_FORT = os.getenv('OUTPUT_FORT')
OUTPUT_TST = os.getenv('OUTPUT_TST')
CHANNEL = os.getenv('PICKUP_CHANNEL')

class myClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.channel.name != CHANNEL:
            print("I've skipped a message because it is not in the correct channel")
            return

        if message.author == self.user:
            return

        if message.author.name != PICKUP_BOT:
            print("I've skipped a message because it was not written by the Pickup Bot")
            return

        else:
            if message.content[0:9] == 'WST ready':
                self.draft_split(message.content, OUTPUT_WST)
                print("STARTING WST")
            if message.content[0:10] == 'Fort ready':
                self.draft_split(message.content, OUTPUT_FORT)
                print("STARTING FORT")
            if message.content[0:9] == 'TST ready':
                self.other_split(message.content, OUTPUT_TST)
                print("STARTING TST")

    def draft_split(self, message, output):
        split_message = message.split('\n')

        captain1 = self.get_user(int(split_message[1].lstrip('Team 1 captain: <@').rstrip('>')))
        captain2 = self.get_user(int(split_message[2].lstrip('Team 2 captain: <@').rstrip('>')))

        everyone_else = split_message[3].lstrip('Everyone else: ').split(',')

        for i in range(len(everyone_else)):
            everyone_else[i] = self.get_user(int(everyone_else[i].lstrip('<@').rstrip('>')))
        
        print("DRAFT SPLIT RESULT: " + captain1.display_name + ", " + captain2.display_name)
        print(everyone_else)
        write_draft(captain1, captain2, everyone_else, output)

    def other_split(self, message, output):
        split_message = message.split('\n')

        first = True
        teams_raw = []
        final_teams = []
        
        for i in range(len(split_message)):
            if first:
                first=False
            else:
                teams_raw.append(split_message[i].lstrip('Team ' + str(i) + ': ').split(', '))

        for team in teams_raw:
            single_team = []
            for player in team:
                single_team.append(self.get_user(int(player.lstrip('<@').rstrip('>'))))
            final_teams.append(single_team)
        
        print("OTHER SPLIT RESULT: ")
        print(final_teams)
        write_other(final_teams, output)

def write_draft(captain1, captain2, everyone_else, output_file):
    f = open(output_file, 'w')
    print("Writing to output file: " + output_file)
    f.write('Captain 1: ' + captain1.display_name + '\n')
    f.write('Captain 2: ' + captain2.display_name + '\n')

    first = True

    for player in everyone_else:
        if first:
            f.write('Players: ' + player.display_name)
            first = False
        else:
            f.write(', ' + player.display_name)

    f.close()

def write_other(teams, output_file):
    print("Writing to output file: " + output_file)
    f = open(output_file, 'w')
    
    count = 0
    for team in teams:
        count += 1
        f.write('Team ' + str(count) + ': ')
        first = True
        for player in team:
            if first:
                first = False
                f.write(player.display_name + ', ')
            else:
                f.write(player.display_name + '\n')
    
    f.close()

client = myClient()
client.run(TOKEN)
