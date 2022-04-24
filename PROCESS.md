# Process Milestone

## Iteration 1 (Thursday, Mar 3 -- Sunday, Apr 10)

### First Steps
Prior to development, the team conducted extensive research into the creation of a Discord bot. This included Discord APIs and external resources such as the Scrabble dictionary. The team also conducted user interviews to gather requirements for our bot, and how it should handle interactions with its users. Finally, the team mapped out the general design of the bot, which is detailed further in the team's DESIGN document.

### Story Creation
The story creation portion of our project was done primarily through remote voice calls on Discord. The group members would meet to discuss the use cases that needed to be implemented, assign story points to rate the complexity of each task, and delegate the tasks to each team member. Brief notes were taken at each meeting in the form of Discord messages, such as the example shown below:

![enter image description here](https://i.imgur.com/Nvvi86d.png)

Similar to GitHub issues or Kanban boards, the team took note of tasks that were to be implemented, and updated the progress of each task with the use of reactions.

Additionally, a large portion of the programming was completed as a group. One team member would share their screen and physically write the code as the other team members would contribute ideas and perform research related to the task at hand. This process of group programming explains why many of the tasks are assigned to multiple developers, and why the commits on GitHub may seem a bit unbalanced.

List of tasks for iteration 1:
- Generate a Boggle board
	- Story points: 8
	- Developers: Vinny

### Reflection
At the end of the first iteration, the team was fairly comfortable with Discord APIs and had a solid understanding of how to incorporate external resources. The user requirements were refined enough that the team knew how to move forward, and the design provided a structure for how to implement each new task. The team was also able to successfully generate a Boggle board on command. The formatting of the board still had to be adjusted for readability, but it was able to function as intended. The team's process for meeting and collaborating on tasks through Discord worked well and allowed for smooth communication between team members. Regular meetings on Discord were preferred over GitHub issues and Kanban boards as they were more convenient and collaborative for a small project group.

## Iteration 2 (Monday, Apr 11 -- Sunday, Apr 24)

### Story Creation
The same practices for story creation that were used for the first iteration were used again in the second iteration.

List of tasks for iteration 2:
- Start a new game (`!bg play`)
	- Story points: 3
	- Developers: Andrew, Ryan, Vinny
- Add play options (`!bg play <seconds> <size>`)
	- Story points: 5
	- Developers: Andrew, Ryan
- End the game
	- Story points: 3
	- Developers: Andrew, Ryan, Vinny
- Cancel the current game (`!bg cancel`)
	- Story points: 3
	- Developers: Ryan
- Submit a word
	- Story points: 5
	- Developers: Andrew, Ryan, Vinny
- Delete messages
	- Story points: 1
	- Developers: Andrew, Ryan, Vinny
- Track player scores
	- Story points: 5
	- Developers: Andrew, Ryan, Vinny
- Track player words
	- Story points: 5
	- Developers: Andrew, Ryan
- Display time warning
	- Story points: 1
	- Developers: Ryan
- Display commands (`!bg help`)
	- Story points: 1
	- Developers: Andrew
- Handle invalid commands
	- Story points: 1
	- Developers: Andrew
- Display scoreboard
	- Story points: 3
	- Developers: Ryan, Vinny
- Display superlatives
	- Story points: 3
	- Developers: Andrew, Ryan

### Demo
Here are a few screenshots exhibiting the the functionality of each of the aforementioned tasks. First, here is a user using the `!bg play` command to start a game. Several players submit words before the game ends and displays the scoreboard and superlatives.

![enter image description here](https://i.imgur.com/OLPv3nv.png)

Next, here are users using the `!bg words` and `!bg words <player>` commands to display the words found by all players and by an individual player, respectively.

![enter image description here](https://i.imgur.com/H6PImkn.png)

This screenshot shows what happens when a user types an invalid command, and subsequently what happens when a user uses the `!bg help` command.

![enter image description here](https://i.imgur.com/vu4BVSY.png)

Finally, here is an example of a user starting a game in which no user enters a word. Then, a user starts a custom game with the `!bg play <seconds> <size>` command, in which no user enters a correct word.

![enter image description here](https://i.imgur.com/gNSmeTd.png)

### AWS
To have the bot be continuously running without needing to constantly run on a team member's personal machine, the team determined that the best solution would be to remotely host it via an EC2 server provided by AWS. However, due to the fact that the team is using a free version of said services, a limitation arose in the form of timeout restrictions imposed by AWS. Namely, a script is not allowed to run on their servers for longer than 45 minutes at a time. As such, the best compromise was to have the server continuously rebuild the project every 30 minutes, effectively causing the bot to go down for approximately 20 seconds every 30 minutes. This means that the bot has an uptime of around 99%, which is admittedly less than ideal.

### Reflection
At the end of the second iteration, the team had successfully implemented each of the tasks that were listed for the iteration. Each task was tested during and after its implementation to ensure that it functioned as intended and did not disrupt any other parts of the bot. The same story creation and collaboration process that was used for the first iteration was used again for the second iteration, and the team still found success using the practices described. The next steps for the team are to add minor features and tweaks to existing features, and to clean up any loose edge cases.
