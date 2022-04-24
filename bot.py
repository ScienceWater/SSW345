from operator import indexOf
import discord
from game import *
import time
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")

DEFAULT_TIME = 35
DEFAULT_SIZE = 4

class MyClient(discord.Client):
    def __init__(self):
        discord.Client.__init__(self)
        self.playing = False
        self.words = set()

    async def start_game(self, message, sec=DEFAULT_TIME, size = DEFAULT_SIZE):
        self.playing = True
        self.b = Board(size)
        self.players = {}
        await message.channel.send(self.b.__str__())
        if sec > 30:
            await asyncio.sleep(sec-30)
            await message.channel.send("30 seconds remain!")
            await asyncio.sleep(20)
            await message.channel.send("10 seconds remain!")
            await asyncio.sleep(10)
        elif 30 > sec > 10:
            await asyncio.sleep(sec-10)
            await message.channel.send("10 seconds remain!")
            await asyncio.sleep(10)
        else:
            await asyncio.sleep(sec)
        
        if self.playing:
            await self.end_game(message)

    async def end_game(self, message):
        self.playing = False
        if self.players == {}:
             await message.channel.send("Why did no one play :(")
        else:
            await self.scoreboard(self.sort_dict(), message)
            await self.superlatives(message)

    async def scoreboard(self, scores, message):
        scoreboard = "Congratulations " + scores[0][1] + "!```"
        #maxX values to help with formatting of the scoreboard
        maxplacelen = len(str(max(scores ,key=lambda x: len(str(x[0])))[0]))
        maxnamelen = len(max(scores ,key=lambda x: len(x[1]))[1])   
        maxscorelen = len(str(max(scores ,key=lambda x: len(str(x[2])))[2])) 
        #scoreboard formatting
        for i in scores:
            scoreboard += "\n" +" "*(maxplacelen - len(str(i[0]))) + str(i[0]) + ". " + i[1] + " "*(maxnamelen - len(i[1])) + " |" + " "*(maxscorelen - len(str(i[2]))+ 1) + str(i[2]) + " points"
        scoreboard += "```"
        await message.channel.send(scoreboard)
    
    def sort_dict(self):
        playerscores = []

        for player in self.players:
            playerscores += [(player, self.players[player][0])]
        playerscores.sort(key=lambda f: f[1], reverse=True)
        for i in range(len(playerscores)):
            playerscores[i] = (i+1, playerscores[i][0], playerscores[i][1]) 

        return playerscores
    
    async def superlatives(self,message):
        longwordinfo = self.find_longest_word()
        mostwordsinfo = self.find_most_words()
        await message.channel.send("```The player with the longest word was: " + longwordinfo[1] + " with " + longwordinfo[0] + 
        "\nThe player with the most words was: " + mostwordsinfo[1] + " with " + str(mostwordsinfo[0])+ " words```")

        
    def find_longest_word(self):
        longword = ''
        longwordplayer = ''
        for player in self.players:
            for word in self.players[player][1]:
                if len(word) > len(longword):
                    longword = word
                    longwordplayer = player
        return [longword, longwordplayer]
    
    def find_most_words(self):
        mostwords = 0
        mostwordsplayer = ''
        for player in self.players:
            if len(self.players[player][1]) > mostwords:
                mostwords = len(self.players[player][1])
                mostwordsplayer = player
        return [mostwords, mostwordsplayer]

    async def list_words(self, message):
        wordlist = ''
        for player in self.players:
            wordlist += ("\n"+ player + ": " )
            for word in self.players[player][1]:
                if self.players[player][1].index(word) == len(self.players[player][1])-1:
                    wordlist += word
                else:
                    wordlist += word + ", "
        await message.channel.send("```" + wordlist + "```")
    
    async def list_words_player(self, message, player):
        if player not in self.players:
            await message.channel.send("Username not found")
        else:
            wordlist = player + ": "
            for word in self.players[player][1]:
                if self.players[player][1].index(word) == len(self.players[player][1])-1:
                    wordlist += word
                else:
                    wordlist += word + ", "
            await message.channel.send("```" + wordlist + "```")
    
    async def add_points(self, message):
        length = len(message.content)

        if length <= 4:
            points = 1
        elif length == 5:
            points = 2
        elif length == 6:
            points = 3
        elif length == 7:
            points = 5
        else:
            points = 11
    
        self.players[message.author.display_name][0] += points


    async def on_message(self, message):
        user_message = str(message.content).lower()


        if message.author == client.user:
            return

        if not self.playing:
            if user_message[0:3] == '!bg':
                if user_message[0:8] == '!bg play':
                    if user_message == '!bg play':
                        await self.start_game(message)
                    else:
                        rules = user_message[8:].split()
                        if len(rules) != 2:
                            await message.channel.send("Please enter '!bg play' or '!bg play <seconds> <size>")
                        elif not rules[0].isnumeric() or not rules[1].isnumeric():
                            await message.channel.send("Parameters must be valid integers")
                        elif int(rules[1]) > 20:
                            await message.channel.send("Due to discord character limits, size must be 20 or less")
                        else:
                            await self.start_game(message, int(rules[0]), int(rules[1]))
                if user_message[0:9] == '!bg words':
                    if user_message == '!bg words':
                        await self.list_words(message)
                    else:
                        await self.list_words_player(message, str(message.content)[10:])
        elif self.playing:
            if user_message[0:3] == '!bg':
                if user_message == '!bg cancel':
                    await self.end_game(message)
            if not message.author.display_name in self.players:
                self.players[message.author.display_name] = [0,[]]
            if self.b.contains(user_message):
                if user_message in self.words:
                    pass
                else:
                    self.words.add(user_message)
                    await self.add_points(message)
                    self.players[message.author.display_name][1].append(user_message)
            await message.delete()
    


client = MyClient()

client.run(TOKEN)
