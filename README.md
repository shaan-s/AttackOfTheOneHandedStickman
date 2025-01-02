# Introduction
This is a pygame based ASCII-art fighting game. It was created in fall 2021 as part of my ICS3U class, which assigned a console-based game. I created a quasi-console in pygame, with custom-built text colour, scroll bar, line-breaks, backspacing, etc. It includes sound effects and a custom song created by me.

![image](https://github.com/user-attachments/assets/dab2f52a-7c11-4b2a-8ae3-0c66506fc3f8)

# Gameplay
The game is a simple fighting game with two levels. The controls are left arrow (punch), right arrow (dodge), and up arrow (double punch). THe window can be resized using F11. Since there is no health regeneration, and attacks are time-limited to prevent spamming, the game is won by good timing. The game tracks combos and awards the player for them. The game comes with an optional tutorial screen. 
![image](https://github.com/user-attachments/assets/9cf6bde5-4b55-4378-8429-ac45bd5a8fb3)
![image](https://github.com/user-attachments/assets/0102e7c1-2a31-4134-8581-01a1ffc2205a)
## Gallery
![image](https://github.com/user-attachments/assets/9cd2fa23-a424-4969-b9d1-c9b44c74488e)

The dodge mechanic in level 1, TOBOR.

![image](https://github.com/user-attachments/assets/e88736b5-399b-44d6-a76e-65226ea7d479)

The pre-amble before level 2, GunMan, showing the coloured text, line-break, and scroll bar features

![image](https://github.com/user-attachments/assets/5471ff5f-f044-4ea4-98d1-db98769101ea)

GunMan's attack

![image](https://github.com/user-attachments/assets/b862ca40-267f-4954-97ff-5fb34e88b0d2)

A double punch, which can only be used in the second level

# Installation
Make sure the latest version of Python is installed. The game uses the non-built-in package `pygame`, which must be installed first. Since the game was built in repl.it, it is also compatible with repl's audio package, however pygame is still needed for the visuals.

`pip install pygame`

`git clone https://github.com/shaan-s/AttackOfTheOneHandedStickman`

Then run `main.py`.
