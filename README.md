# NauLingo
This is a Discord bot that uses the disnake python library. The purpose of the bot is to translate English into Naumarian using regular expressions.
The bot makes use of a translator.py, which is the decendent of my other, poorly named, repo "translator". Along with being more complete, this bot is faster
because it makes better use of time complexitities bystoring the translations in a dictionary within a json.
<br />
<br />
Currently there is no reverse translation, but it is a top priority.

# Prerequisites
Building and running this in docker should handle these
Python 3.7.0+<br />
Disnake<br />
flask<br />
flask-restful<br />
flask-cors<br />
gunicorn<br />


# Other Steps
In order for this bot to work you will need to create three seperate files within the main directory<br />
token.txt<br />
Paste your bots token onto a single line, the main script will pull it from here<br /><br />
replies.txt<br />
This is where any translation replies will be held and searched for<br /><br />
oauth2.txt<br />
This is where you will put the invite link to your bot, this will be used in creating the link buttons<br /><br />

# Time Complexity
![Time Graph](https://github.com/qmt8843/NauLingo/blob/main/TimeGraph.png?raw=true)<br />
Above you can see a linear increase in time with the increase in the number of words provided to the translator. The sentences were generated from the current list of translatable words and endings, this way it could get a worst case scenario. Unfortunatly, this linear function is also the best case, as the re library (more specifically re.sub) has a time complexity of o(n). Future optimizations could only expect to either decrease the slope of the graph, or decrease the overall time.

# Web Server
In order get the same translation (and logic) on my website, I have created a simple https server to return any needed translations. It makes use of a Flask-Restful API with CORS support and runs over HTTPS.

# Sites
Disnake: https://disnake.dev/ <br />
Flask: https://flask.palletsprojects.com/en/2.0.x/ <br />
Flask-Restful: https://flask-restful.readthedocs.io/en/latest/ <br />
Flask-Cors: https://flask-cors.readthedocs.io/en/latest/ <br />
Let's Encrypt (used to get SSL): https://letsencrypt.org/ <br />
Naumarian Website: https://www.naumarian.info/
