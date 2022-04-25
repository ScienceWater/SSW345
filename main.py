from operator import indexOf
import discord
from game import *
import time
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")

DEFAULT_TIME = 180
DEFAULT_SIZE = 4

class MyClient(discord.Client):
    def __init__(self):
        discord.Client.__init__(self)
        self.playing = False
        self.words = set()

    # Starts a new game of Boggle
    async def start_game(self, message, sec=DEFAULT_TIME, size = DEFAULT_SIZE):
        self.playing = True
        self.b = Board(size)
        self.players = {}
        await message.channel.send(self.b.__str__())

        # Sends warning messages at certain amounts of time remaining
        if sec > 30:
            await asyncio.sleep(sec-30)
            if self.playing:
                await message.channel.send("30 seconds remain!")
                await asyncio.sleep(20)
                if self.playing:
                    await message.channel.send("10 seconds remain!")
                    await asyncio.sleep(10)
        elif 30 > sec > 10:
            await asyncio.sleep(sec-10)
            if self.playing:
                await message.channel.send("10 seconds remain!")
                await asyncio.sleep(10)
        else:
            await asyncio.sleep(sec)
        
        # Ends the game
        if self.playing:
            await self.end_game(message)

    # Ends the current game of Boggle (and displays scoreboard and superlatives)
    async def end_game(self, message):
        self.playing = False
        if self.players == {}:
             await message.channel.send("Why did no one play :(")
        else:
            await self.scoreboard(self.sort_dict(), message)
            await self.superlatives(message)

    # Displays a scoreboard (after a game ends)
    async def scoreboard(self, scores, message):
        scoreboard = "Congratulations " + scores[0][1] + "!```"
        # maxX values to help with formatting of the scoreboard
        maxplacelen = len(str(max(scores ,key=lambda x: len(str(x[0])))[0]))
        maxnamelen = len(max(scores ,key=lambda x: len(x[1]))[1])   
        maxscorelen = len(str(max(scores ,key=lambda x: len(str(x[2])))[2])) 
        # scoreboard formatting
        for i in scores:
            scoreboard += "\n" +" "*(maxplacelen - len(str(i[0]))) + str(i[0]) + ". " + i[1] + " "*(maxnamelen - len(i[1])) + " |" + " "*(maxscorelen - len(str(i[2]))+ 1) + str(i[2]) + " points"
        scoreboard += "```"
        await message.channel.send(scoreboard)
    
    # Sorts the players in order of their score (after a game ends)
    def sort_dict(self):
        playerscores = []

        for player in self.players:
            playerscores += [(player, self.players[player][0])]
        playerscores.sort(key=lambda f: f[1], reverse=True)
        for i in range(len(playerscores)):
            playerscores[i] = (i+1, playerscores[i][0], playerscores[i][1]) 

        return playerscores
    
    # Displays superlatives (longest word, most words, etc.) after a game of Boggle has ended
    async def superlatives(self, message):
        longwordinfo = self.find_longest_word()
        mostwordsinfo = self.find_most_words()
        await message.channel.send("```The player with the longest word was: " + longwordinfo[1] + " with " + longwordinfo[0] + 
        "\nThe player with the most words was: " + mostwordsinfo[1] + " with " + str(mostwordsinfo[0])+ " words```")

    # Helper function for finding the longest word found in a game and the player who found that word
    def find_longest_word(self):
        longword = ''
        longwordplayer = ''
        for player in self.players:
            for word in self.players[player][1]:
                if len(word) > len(longword):
                    longword = word
                    longwordplayer = player
        if longword != '':
            return [longword, longwordplayer]
        else:
            return ['N/A', 'no one']
    
    # Helper function for finding the player who found the most words in a game and how many words they found
    def find_most_words(self):
        mostwords = 0
        mostwordsplayer = ''
        for player in self.players:
            if len(self.players[player][1]) > mostwords:
                mostwords = len(self.players[player][1])
                mostwordsplayer = player
        if mostwords != 0:
            return [mostwords, mostwordsplayer]
        else:
            return [0, 'no one']

    # `!bg words` Displays the scoring words of each player from the last game of Boggle
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
    
    # `!bg words <player>` Displays the scoring words of the given player from the last game of Boggle
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
    
    # Awards points to a player for a submitted word
    async def add_points(self, message, word):
        length = len(word)

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

    # Reads all messages sent in the Discord server
    async def on_message(self, message):
        user_message = str(message.content).lower()

        # Ensures that BoggleBot does not delete or respond to its own messages
        if message.author == client.user:
            return

        # Responds to these commands if there is no game in progress
        if not self.playing:
            # Reads `!bg` commands
            if user_message[0:3] == '!bg':
                # Reads `!bg play` commands
                if user_message[0:8] == '!bg play':
                    # `!bg play` Starts a new game of Boggle with the default settings of 3 minutes and a 4x4 board
                    if user_message == '!bg play':
                        await self.start_game(message)
                    # `!bg play <seconds> <size>` Starts a new game of Boggle with the given parameters
                    else:
                        rules = user_message[8:].split()
                        # Checks that the user input the proper number of parameters (2)
                        if len(rules) != 2:
                            await message.channel.send("Please enter '!bg play' or '!bg play <seconds> <size>")
                        # Checks that the user input the proper type of parameters (integers)
                        elif not rules[0].isnumeric() or not rules[1].isnumeric():
                            await message.channel.send("Parameters must be valid integers")
                        # Checks that the user input a board size less than or equal to 20 (larger sizes display improperly, especially on mobile)
                        elif int(rules[1]) > 20:
                            await message.channel.send("Due to discord character limits, size must be 20 or less")
                        else:
                            await self.start_game(message, int(rules[0]), int(rules[1]))
                # Reads `!bg words` commands
                elif user_message[0:9] == '!bg words':
                    # `!bg words` Displays the scoring words of each player from the last game of Boggle
                    if user_message == '!bg words':
                        await self.list_words(message)
                    # `!bg words <player>` Displays the scoring words of the given player from the last game of Boggle
                    else:
                        await self.list_words_player(message, str(message.content)[10:])
                # `!bg help` Displays a list of commands
                elif user_message == '!bg help':
                    await message.channel.send("```Commands:\n\
- !bg help : Displays a list of commands\n\
- !bg play : Starts a new game of Boggle with the default settings of 3 minutes and a 4x4 board\n\
- !bg play <seconds> <size> : Starts a new game of Boggle with the given parameters\n\
- !bg cancel : Cancels the current game of Boggle\n\
- !bg words : Displays the scoring words of each player from the last game of Boggle\n\
- !bg words <player> : Displays the scoring words of the given player from the last game of Boggle```")
                # Directs message author to `!bg help` if command is not recognized
                else:
                    await message.channel.send(user_message + " is not a recognized command. Type `!bg help` for a list of commands.")

        # Responds to these commands if there is a game in progress
        elif self.playing:
            # Reads `!bg` commands
            if user_message[0:3] == '!bg':
                # `!bg cancel` Cancels the current game of Boggle
                if user_message == '!bg cancel':
                    await self.end_game(message)
            # Adds message author to list of players (if they are not already added)
            if not message.author.display_name in self.players:
                self.players[message.author.display_name] = [0,[]]
            # Checks if word has already been found by a player in the current game
            word = self.b.contains(user_message)
            #   If so, ignore the duplicate word
            if not word or word in self.words:
                pass
            #   If not, add word to lists of words found for game and player, and award points to player
            else:
                self.words.add(word)
                await self.add_points(message, word)
                self.players[message.author.display_name][1].append(word)
            # Deletes the message (to maintain the board at the bottom of the screen)
            await message.delete()
    


client = MyClient()

client.run(TOKEN)
