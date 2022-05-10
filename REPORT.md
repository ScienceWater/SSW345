# Report
## Problem Statement
In the age of COVID-19, many facets of life have been moved to an online environment. Whether it is because they are sick, or are trying to avoid sickness, people are spending an increasing amount of time communicating with others on platforms like Discord. While simple text communication is sufficient for some people, others seek more a more interesting and unique way to interact with their friends. As such, developing a game seemed an appropriate solution. BoggleBot, as the name suggests, allows users to play our unique version of Boggle remotely in a Discord server. Some creative liberties were taken with the rules to make the game more competitive, better suited for the Discord environment, and allow for more customizable user experiences.

## Features and Screenshots
### Rules
BoggleBot abides by **[standard Boggle rules](https://www.fgbradleys.com/rules/Boggle.pdf)**, except for the following differences:
* Instead of only getting points for unique words at the end of the game, players are awarded points for being the first to enter a particular word, with no other player receiving any credit.
* The game can be customized (through use of the `!bg play <seconds> <size>` command) to have a non-standard time limit and/or board size. Board dimensions are still always square, and can be anywhere between 2x2 and 20x20.

### Functionality
Here are a few screenshots exhibiting the the functionality of each of the aforementioned tasks. First, here is a user using the `!bg play` command to start a game. Several players submit words before the game ends and displays the scoreboard and superlatives.

![image](https://user-images.githubusercontent.com/54965487/167526523-4b1da5e3-9dc8-4466-aada-1859efa0fdfd.png)

Next, here are users using the `!bg words` and `!bg words <player>` commands to display the words found by all players and by an individual player, respectively.

![image](https://user-images.githubusercontent.com/54965487/167526505-fab00ecc-c1ff-414a-91dd-5865679d18e6.png)

This screenshot shows what happens when a user types an invalid command, and subsequently what happens when a user uses the `!bg help` command.

![image](https://user-images.githubusercontent.com/54965487/167526490-52f6e705-aa11-459c-8d52-39fc4e4e015d.png)

Here is an example of a user starting a game in which no user enters a word. Then, a user starts a custom game with the `!bg play <seconds> <size>` command, in which no user enters a correct word.

![image](https://user-images.githubusercontent.com/54965487/167526474-14573d48-6f27-4b53-8c07-f7b6924b5ce5.png)

Finally, this is an example of a game terminating early due to someone typing the `!bg cancel` command. Note that the command is deleted before the game ends so as to make the post-game display look consistent.

![image](https://user-images.githubusercontent.com/54965487/167528403-08f9b9d1-2175-4a9b-9c2a-a0b8c972adad.png)

## Reflection
The development process primarily occurred through regular team meetings via remote voice calls on Discord. The group members would meet to discuss the use cases that needed to be implemented and to delegate the tasks to each team member. Brief notes were taken at each meeting in the form of Discord messages, such as the example shown below:

![image](https://user-images.githubusercontent.com/54965487/167529275-b4b7c1fc-8e76-4099-807c-8cd2c779e77c.png)

Similar to GitHub issues or Kanban boards, the team took note of tasks that were to be implemented, and updated the progress of each task with the use of reactions.

Additionally, a large portion of the programming was completed as a group. One team member would share their screen and physically write the code as the other team members would contribute ideas and perform research related to the task at hand. This process of group programming explains why many of the tasks are assigned to multiple developers, and why the commits on GitHub may seem a bit unbalanced.

The team needed to first be familiarized with Discord APIs and develop a solid understanding of how to incorporate external resources. The user requirements were refined enough that the team knew how to move forward, and the design provided a structure for how to implement each new task. The team's process for meeting and collaborating on tasks through Discord worked well and allowed for smooth communication between team members. Regular meetings on Discord were preferred over GitHub issues and Kanban boards as they were more convenient and collaborative for a small project group. Each task was tested during and after its implementation to ensure that it functioned as intended and did not disrupt any other parts of the bot.

The bot was first considered to be hosted via AWS webhosting, and this deployment strategy was what the team used at first when attempting continuous deployment. However, after discovering limitations on what AWS provides with a free license (i.e. limits on how long a program can be deployed, how much data can be transferred per month, etc.), it was decided to instead host the bot with Heroku. Deployment with Heroku required very minor alterations to the source code, after which no further modifications were needed for remote hosting to function as desired.

## Limitations and Future Work
Due to the nature of how Discord bots are allowed to interact with chat, there are certain limitations that could not be overcome. For instance, it is impossible for a Discord bot to delete a message before it appears in the chat log, thereby causing the juttering effect experienced during gameplay. Additionally, a user inputting words in rapid succession may still see some of the words they inputted with them seemingly never being deleted. However, when this happens, the words still have truly been deleted, and can no longer be seen by other users, but this effect will not be seen by the user who entered the words until the page is reloaded. Lastly, a single Discord message is limited to contain no more than 2,000 characters. This informed the decision to limit the maximum allowed board size to 20x20.

There are several features yet to be implemented that would improve the quality of the bot even further. The most critical of these features is to add the ability for the bot to run a game in multiple channels simultaneously. This will require some restructuring of the source code as a whole, but is an essential improvement to be made. Another change to make would be to have the bot take slash commands (i.e. `/bg play` instead of `!bg play`), as this is a newer requirement for a Discord bot to be verified. Other features that are non-essential, but would still add to the overall experience, would be to include global and/or server-wide leaderboards and to have a built in `define` function that will let a user know the dictionary definition of a word outside of gameplay.
