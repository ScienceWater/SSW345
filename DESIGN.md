# Design Proposal

## Problem Statement

In the age of COVID-19, many facets of life have been moved to an online environment. Whether it is because they are sick, or are trying to avoid sickness, people are spending an increasing amount of time communicating with others on platforms like Discord. While simple text communication is sufficient for some people, others seek more a more interesting and unique way to interact with their friends.

## Bot Description

BoggleBot is an interactive Discord bot that can be added to any Discord server so that people can play Boggle with their friends. Boggle is a word game that was first published about 50 years ago. The game can be played with at least 2 players, and only requires a 4x4 grid of letters and a timer. While Boggle's popularity has died down over the years, word games are still in style. Games like Scrabble, Words with Friends, and Wordle are dominating today's top charts in the game market. So, why not return to one of the classics for some friendly, thought-provoking competition with your friends?

The original version of Boggle would have players create words using letters from the grid and write them down privately. Each player's words would be revealed at the end of the timer, and only unique words would score points for the player. However, BoggleBot's takes its own twist on Boggle in order to better accommodate the Discord environment. Once the grid is generated, players are able to type words in real time, with the first player to type a valid word receiving points for that word. This will encourage more fast-paced, interactive rounds that users can easily pick up and play with their friends.

A tagline for the bot's publication will be as follows: "A Discord Bot that breathes new, fast-paced life into the classic word game!"

## Use Cases

### Use Case 1: Creating a Game

#### Preconditions
A game is not currently ongoing.

#### Main Flow
A user issues a command to the chatbot to start the game [S1]. Bot will return a randomly generated Boggle board based on the specified parameter(s) [S2]. Bot begins an internal timer [S3] and starts tracking word submission(s) [S4].

#### Subflows
[S1] There will be several valid commands for starting a new game. For example, `!bg play` will start a game with standard board dimensions and time limit. `!bg play 7` will start a game with a 7x7 board and the standard time limit. `!bg play 4:00` will start a game with standard board dimensions and a four minute time limit. `!bg play 7 4:00` will start a game with a 7x7 board and a four minute time limit.

[S2, S3] A board will be generated and a timer will be started per the requirements in [S1]. The board will be rendered in the chat in a text format with clear grid alignment.

[S4] The bot will initialize each player with an empty list of words. Starting here, words will begin being tracked as described in **Use Case 2**.

#### Alternative Flows
[E1] A game is already ongoing. Games should be possible to cancel early via the creator of the game entering a command such as `!bg cancel`.

[E2] Invalid inputs for creating a game. This should result in an error message to the effect of: "Sorry, I don't understand that. If you want to play a new game of Boggle, typey tig `!bg play <size> <time>`. For example, try `!bg play` or `!bg play 7 4:00`"

### Use Case 2: Playing a Game

#### Preconditions
A game is currently ongoing.

#### Main Flow
The bot will monitor the chat the game was created in for words and block words submitted by other users from displaying on a given user's screen [S1]. If a word is valid, then it will be added to the list of words assigned to the player whom submitted it [S2]. There are several conditions a word must fulfill in order to be considered valid [S3].

#### Subflows
[S1] A player will be able to submit a single word at a time, exclusively with alphabetic characters. They will be able to see all words they have submitted, but none of the words that other players submit during the time limit.

[S2] If valid, a word will be added to that player's list of words. Additionally, that word's point value (determined by its length) will be added to a running total number of points that player has earned in the round.

[S3] A word is considered valid if it (1) is in the standard English dictionary, (2) is possible to make with adjacent, non-repeating letters in the board, (3) is three letters or longer, and (4) has not previously been submitted by any player engaged with this game.

#### Alternative Flows
[E1] The player enters a message with non-alphabetic characters. The bot will attempt to check the validity of the word by stripping all non-alphabetic characters from the word. For instance, `hen-house` and `.     school bus _  ;` will be evaluated as `henhouse` and `schoolbus`.

[E2] The word entered by the player is not valid as determined by [S3]. The word will be added to the player's list with an indication that it had already been used if and only if the word satisfies [S3.1], [S3.2], and [S3.3] but not [S3.4]. Otherwise, the word will not be added to the list and the player will be notified upon entering that the word was invalid. In either case, no points will be awarded for the word.

## Design Sketches

### Sequence Flow Diagram
![enter image description here](https://i.imgur.com/ERS77PO.jpeg)
___
### Primary Flow Storyboard
![](https://imgur.com/PGRoUDu.pnga/nm4LqGK)

## Architecture Design

The bot, being hosted on Discord, will make use of Discord APIs for the purposes of reading, sending, and managing messages within a Discord server. As mentioned earlier, it will need to be able to parse commands sent through chat as well as interpret words in general that are sent during the games running time. It will also need to send its own messages to ensure a cohesive user experience, as well as managing messages sent by other users so that the rules of the game continue to hold.

Another external resource this bot will use will be a dictionary of common English words. A straightforward solution would be to use the official [Scrabble dictionary](https://raw.githubusercontent.com/redbo/scrabble/master/dictionary.txt).

In terms of class structure, several classes will be necessary to ensure that file structure is clean and comprehensible.

One necessary class will be a Board class, which will hold a 2D array of characters to represent the board. It will also need a function capable of determining whether or not a specific word can be found within the board.

Another class that would be helpful would be a static Dictionary class that can be referenced to determine whether or not a specific word is within the English language.

Yet another class will be a Player class, which will be necessary to track which users have found which words, as well as tracking how many points players have accrued.

Lastly, there will need to be a master Game class, which will contain the board and player information for a specific game. The Game class will also track which words have been played already, and will award points to a player who submits a word that has not been found yet. Additionally, the Game class will need to contain a timer, which after its expiration no further words will be parsed.

### Interactions between users, APIs, and classes
![](https://i.imgur.com/AxQW9e5.png)
<!--stackedit_data:
eyJoaXN0b3J5IjpbMTkyOTQzNTU5MSwxMTYwMDM3ODExLC0xND
c3MDc1NDEzLDE1OTI3NTExNjQsMTI3NjMzNzcxMSwtMzI4Mzcy
NTg2LDE1NzA3MDQ1MTUsMzk2NDAxOTcyLC04MjY4MjE3MTcsLT
kxNDYxMjU0MCwtMTUyNjA0NTMwNywzNTk3OTE1OSwzMDY2NDMz
MjAsLTEwNjYwODI3NzgsLTE1NDQ5NDkwNzksMjkyNzkxNTgsNT
gyNjU4ODExLC00MjI4MjYzNjYsLTE2ODk4MTczMzQsNjgzMTg1
MTJdfQ==
-->