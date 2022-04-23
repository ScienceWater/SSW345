import discord
from game import *
import time
import asyncio


token='OTU4NDYzMjU1ODA4OTk5NDcx.YkNsdw.hHPkvXsoXQ-mbFZpkJa1L9ckQvo'

DEFAULT_TIME = 30

class MyClient(discord.Client):
    def __init__(self):
        discord.Client.__init__(self)
        self.playing = False
        self.words = set()

    async def start_game(self, message, sec=DEFAULT_TIME):
        self.playing = True
        self.b = Board(4)
        self.players = {}
        await message.channel.send(self.b.__str__())
        await asyncio.sleep(sec)
        await self.end_game(message)

    async def end_game(self, message):
        self.playing = False
        await self.scoreboard(self.sort_dict(), message)

    async def scoreboard(self, scores, message):
        scoreboard = "Congratulations " + scores[0][1] + "!```"
        maxplacelen = len(str(max(scores ,key=lambda x: len(str(x[0])))[0]))
        maxnamelen = len(max(scores ,key=lambda x: len(x[1]))[1])   
        maxscorelen = len(str(max(scores ,key=lambda x: len(str(x[2])))[2])) 
        for i in scores:
            scoreboard += "\n" +" "*(maxplacelen - len(str(i[0]))) + str(i[0]) + ". " + i[1] + " "*(maxnamelen - len(i[1])) + " |" + " "*(maxscorelen - len(str(i[2]))+ 1) + str(i[2]) + " points"
        scoreboard += "```"
        await message.channel.send(scoreboard)
    
    def sort_dict(self):
        playerscores = []

        for player in self.players:
            playerscores += [(player, self.players[player])]
        playerscores.sort(key=lambda f: f[1], reverse=True)
        for i in range(len(playerscores)):
            playerscores[i] = (i+1, playerscores[i][0], playerscores[i][1]) 

        return playerscores

    
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
    
        self.players[message.author.display_name] += points


    async def on_message(self, message):
        user_message = str(message.content).lower()


        if message.author == client.user:
            return

        if not self.playing:
            if user_message[0:3] == '!bg':
                if user_message == '!bg play':
                    await self.start_game(message)
        else:
            if not message.author.display_name in self.players:
                self.players[message.author.display_name] = 0
            if self.b.contains(user_message):
                if user_message in self.words:
                    await message.channel.send('word already used')
                else:
                    self.words.add(user_message)
                    await self.add_points(message)
            else:
                await message.channel.send('bad word')



        

                
        

        
        



client = MyClient()

client.run(token)