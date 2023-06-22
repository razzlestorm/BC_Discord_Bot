
This is a Discord Bot for the Final Fantasy: Beyond Chaos randomizer!

## About the Bot

This is a basic look-up bot that is currently set to load in excel files and look up information when a user makes a request.
The bot's functionality is located within the Cogs folder. Each Cog would ideally have somewhat separate functionality, and it is designed so that it will load each cog separately.

The majority of the bot's functionality is a port of [GreenKnight's Desktop CecilBot](https://github.com/greenknight5/CecilBotDesktopApp). His excel files were also used to create the database that this will eventually run on.

## Deployment

To deploy, you will need to have this hosted either on your own machine, or on a free service like Heroku. 

## Built With

* [Discord.py](https://discordpy.readthedocs.io/en/latest/)

## TODO
* Rework bot to use new Discord API with slash commands
* Have slash commands prepopulate as user types so there are fewer mispellings (if possible with API).
* Turn spreadsheets into database
* Allow mods to add data via slash commands