import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

user_sessions = {}


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.event
async def on_message(message):

    if message.author.bot:
        return

    channel_name = "create-event-here"

    if message.channel.name != channel_name:
        return

    user_id = message.author.id

    if user_id not in user_sessions:

        user_sessions[user_id] = {
            "step": "name"
        }

        await message.reply(
            "What's the name of your event?"
        )
        return

    session = user_sessions[user_id]

    if session["step"] == "name":

        session["name"] = message.content
        session["step"] = "time"

        await message.reply(
            "What date and time is the event?"
        )

        return

    if session["step"] == "time":

        session["time"] = message.content
        session["step"] = "location"

        await message.reply(
            "What's the address or location?"
        )

        return

    if session["step"] == "location":

        session["location"] = message.content

        output = f"""
✅ EVENT READY

WHAT:
{session['name']}

WHEN:
{session['time']}

WHERE:
{session['location']}

Now type:

/create

Then copy these values into the boxes.
"""

        await message.reply(output)

        del user_sessions[user_id]

bot.run(TOKEN)