import disnake
import translator
import json
from disnake.ext import commands
from disnake import ApplicationCommandInteraction
import logging

#establish the bot's token
with open("data/token.txt") as token_file:
    TOKEN = token_file.readline().strip()
    
#establish a command trigger symbol
COMMAND_SYMBOL = "&"

#establish the bot's token
with open("data/oauth2.txt") as token_file:
    INVITE_LINK = token_file.readline().strip()

#establishes request file
REQUEST_FILE = "data/requests.txt"

#establishes logging file
LOG_FILE = "data/bot.log"

#logging setup
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', encoding='utf-8', level=logging.DEBUG, handlers=[
        logging.FileHandler("data/bot.log"),
        logging.StreamHandler()
        ])

#establishes a file for stored word dictionaries
STORAGE_FILE = "data/dict_storage.json"

#establish a command trigger symbol
bot = commands.Bot(command_prefix=commands.when_mentioned_or(f"{COMMAND_SYMBOL}"), intents=disnake.Intents.all())

######################
###    BUTTONS     ###
######################

#This class is responsible for holding all link buttons
class LinkButtons(disnake.ui.View):
    def __init__(self):
        super().__init__()

        self.view = disnake.ui.View()
        self.view.add_item(
            disnake.ui.Button(
                style=disnake.ButtonStyle.url,
                label="🌐 Website",
                url="https://www.naumarian.info/",
            )
        )
        self.view.add_item(
            disnake.ui.Button(
                style=disnake.ButtonStyle.url,
                label="➕ Invite",
                url=f"{INVITE_LINK}",
            )
        )

######################
### SLASH COMMANDS ###
######################

# @bot.slash_command(name='ping', description="Sends back bot latency")
# async def ping(inter: ApplicationCommandInteraction):
    
#     embed = disnake.Embed(
#         title="Pong:",
#         description=f"Latency: {round(bot.latency*1000)}ms"
        
#     )

#     website = Buttons().view
#     return await inter.send(embed=embed, ephemeral=True, view = website)

#translate command logic
@bot.slash_command(name='translate', description="Translates English into Naumarian")
async def translate(inter: ApplicationCommandInteraction, sentence: str):
    logging.info(f"[TRANSLATE] Author:{str(inter.author).encode('unicode-escape').decode('ASCII')}  Channel:{inter.channel}  Server:{inter.guild}  Note:{sentence.strip()}")
    translated, time = translator.take_input(sentence)
    embed = disnake.Embed(
        title="Naumarian translation:",
        description=f"**Old:** {sentence}\n\n**New:** {translated}\n\nSomething didn't translate? Use /request to get it added!\n`Time taken: {time} seconds`"
    )
    website = LinkButtons().view
    return await inter.send(embed=embed, ephemeral=True, view = website)

#public translate command logic
#just isn't ephemeral
@bot.slash_command(name='publictranslate', description="Translates English into Naumarian for the whole server to see")
async def translate(inter: ApplicationCommandInteraction, sentence: str):
    logging.info(f"[PUBLIC TRANSLATE] Author:{str(inter.author).encode('unicode-escape').decode('ASCII')}  Channel:{inter.channel}  Server:{inter.guild}  Note:{sentence.strip()}")
    translated, time = translator.take_input(sentence)
    embed = disnake.Embed(
        title="Naumarian translation:",
        description=f"**Old:** {sentence}\n\n**New:** {translated}\n\nSomething didn't translate? Use /request to get it added!\n`Time taken: {time} seconds`"
    )
    website = LinkButtons().view
    return await inter.send(embed=embed, ephemeral=False, view = website)

#request command logic
#this command allows users to request words that don't have a translation
@bot.slash_command(name='request', description="Makes a translation request")
async def request(inter: ApplicationCommandInteraction, word: str):
    if len(word.split(" ")) != 1:
        logging.warning(f"[REQUEST] Issue:Not Individual  Author:{str(inter.author).encode('unicode-escape').decode('ASCII')}  Channel:{inter.channel}  Server:{inter.guild}  Note:{word.strip()}")
        embed = disnake.Embed(
            title="Translation request:",
            description="You man only request individual words."
        )
        website = LinkButtons().view
        return await inter.send(embed=embed, ephemeral=True, view = website)

    count = 0
    with open(REQUEST_FILE) as request_file: #searches through current requests (faster)
                if count < 1000:
                    for line in request_file:
                        count+=1
                        if line.strip() == word:
                            logging.warning(f"[REQUEST] Issue:Already Requested  Author:{str(inter.author).encode('unicode-escape').decode('ASCII')}  Channel:{inter.channel}  Server:{inter.guild}  Note:{word.strip()}")
                            embed = disnake.Embed(
                                title="Translation request:",
                                description=f"Request: {word}\n\nThat word has already been requested."
                            )
                            website = LinkButtons().view
                            return await inter.send(embed=embed, ephemeral=True, view = website)
                else:
                    logging.warning(f"[REQUEST] Issue:Too Many Requests  Author:{str(inter.author).encode('unicode-escape').decode('ASCII')}  Channel:{inter.channel}  Server:{inter.guild}  Note:{word.strip()}")
                    embed = disnake.Embed(
                            title="Translation request:",
                            description=f"Request: {word}\n\nThere are currently too many requests. Try again later."
                        )
                    website = LinkButtons().view
                    return await inter.send(embed=embed, ephemeral=True, view = website)

    #for file in WORD_FILES: #searches through current translatable words (slower)
    current_file = json.load(open(STORAGE_FILE, "r"))
    current = list(current_file[0].keys())
    if word[0] in current:
        logging.warning(f"[REQUEST] Issue:Already Exists  Author:{str(inter.author).encode('unicode-escape').decode('ASCII')}  Channel:{inter.channel}  Server:{inter.guild}  Note:{word.strip()}")
        embed = disnake.Embed(
            title="Translation request:",
            description=f"Request: {word}\n\nThat word already has a translation."
        )
        website = LinkButtons().view
        return await inter.send(embed=embed, ephemeral=True, view = website)

    with open(REQUEST_FILE, "a") as request_file: #adds request to requests file
        request_file.write(word+"\n")
        logging.info(f"[REQUEST] Author:{str(inter.author).encode('unicode-escape').decode('ASCII')}  Channel:{inter.channel}  Server:{inter.guild}  Note:{word.strip()}")
        embed = disnake.Embed(
                    title="Translation request:",
                    description=f"Request: {word}\n\nYour request has been recieved. It will be dealt with as soon as possible."
                )
        website = LinkButtons().view
        return await inter.send(embed=embed, ephemeral=True, view = website)

#help command logic
@bot.slash_command(name='help', description="Shows command list")
async def help(inter: ApplicationCommandInteraction):
    logging.warning(f"[HELP] Author:{str(inter.author).encode('unicode-escape').decode('ASCII')}  Channel:{inter.channel}  Server:{inter.guild}")
    embed = disnake.Embed(
        description=f"This bot uses the 3.0 version of the Naumarian Translator, so expect differences from the website\n"+
                    f"\nCommands:\b"+
                    f"/help - Shows this menu\n"+
                    f"/translate - Takes English into Naumarian\n"+
                    f"/publictranslate - Same as translate, but allows the whole server to see\n"+
                    f"/request - Takes a word to be added into Naumarian"
    )
    website = LinkButtons().view
    return await inter.send(embed=embed, ephemeral=True, view = website) 

#Runs the bot
try:
    logging.info(f"NauLingo is starting!")
    bot.run(TOKEN)  
except Exception as error:
    logging.critical("FAILED TO START BOT:  {error}")