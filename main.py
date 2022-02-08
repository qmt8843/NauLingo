import discord
import translator
import json

#establish the bot's token
with open("token.txt") as token_file:
    TOKEN = token_file.readline().strip()

#establish a command trigger symbol
COMMAND_SYMBOL = "&"

#establish a channel where bot will work
CHAT = "general"

#establishes word files
REQUEST_FILE = "requests.txt"

#establishes a file for stored word dictionaries
STORAGE_FILE = "data/dict_storage.json"

client = discord.Client()

#make initial connection to discord
@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

#handle message events
@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    mention = str(message.author.mention)
    user_message = str(message.content)

    #create split message variables before try, so that future if doesn't throw an error
    user_message_command = None
    user_message_arg = None
    #for better use of commands, this will try to seperate the command prompt from the arguments
    try:
        user_message_command, user_message_arg = user_message.split(" ", 1)
        user_message_command.lower()
        user_message_arg.lower()
    except:
        print(f"{username} issued a single line command")
    channel = str(message.channel.name)

    #stops bot from responding to itself
    if message.author == client.user:
        return

    if channel == CHAT: #this statement keeps the bot to a single channel
        print(f'{username}: {user_message} ({channel})')
        #translate command logic
        if user_message_command == COMMAND_SYMBOL+"translate" or user_message_command == COMMAND_SYMBOL+"t":
            converted_message = translator.take_input(user_message_arg) #hands off translation logic to translator.py
            await message.channel.send(f'{mention}, I converted {user_message_arg} to: ```{converted_message}```')
            return

        #request command logic
        #this command allows users to request words that don't have a translation
        elif user_message_command == COMMAND_SYMBOL+"request" or user_message_command == COMMAND_SYMBOL+"r":
            with open(REQUEST_FILE) as request_file: #searches through current requests (faster)
                for line in request_file:
                    if line.strip() == user_message_arg:
                        await message.channel.send(f"{mention}, someone else has already requested that word.")
                        return
            #for file in WORD_FILES: #searches through current translatable words (slower)
            current_file = json.load(open(STORAGE_FILE, "r"))
            current = list(current_file[0].keys())
            if isinstance(user_message_arg, current):
                await message.channel.send(f"{mention}, this world already has a translation.")
                return
            
            with open(REQUEST_FILE, "a") as request_file: #adds request to requests file
                request_file.write(user_message_arg+"\n")
            await message.channel.send(f"{mention}, your request has been recieved. It will be dealt with as soon as possible.")
            return

        elif user_message == COMMAND_SYMBOL+"help":
            await message.channel.send("```"+
                                        f"{COMMAND_SYMBOL}help - shows this menu\n"+
                                        f"{COMMAND_SYMBOL}translate - takes English into Naumarian\n"+
                                        f"{COMMAND_SYMBOL}request - takes a word to be added into Naumarian"+
                                        "```")

client.run(TOKEN)