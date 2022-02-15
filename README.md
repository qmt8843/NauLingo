# NauLingo
This is a Discord bot that uses the disnake python library. The purpose of the bot is to translate English into Naumarian using regular expressions.
The bot makes use of a translator.py, which is the decendent of my other, poorly named, repo "translator". Along with being more complete, this bot is faster
because it makes better use of time complexitities bystoring the translations in a dictionary within a json.
<br />
<br />
Currently there is no reverse translation, but it is a top priority.

# Prerequisites
Python 3.7.0+<br />
Disnake

# Other Steps
In order for this bot to work you will need to create three seperate files within the main directory<br />
token.txt<br />
Paste your bots token onto a single line, the main script will pull it from here<br /><br />
replies.txt<br />
This is where any translation replies will be held and searched for<br /><br />
oauth2.txt<br />
This is where you will put the invite link to your bot, this will be used in creating the link buttons<br /><br />

# Sites
Disnake: https://disnake.dev/<br />
Naumarian Website: https://www.naumarian.info/
