import os
import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")

# Replace with your event channel ID
EVENT_CHANNEL_ID = 1544412516719927306

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

user_sessions = {}


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.event
async def on_message(message):

    # Ignore bots
    if message.author.bot:
        return

    # Ignore messages outside event channel
    if message.channel.id != EVENT_CHANNEL_ID:
        return

    user_id = message.author.id

    # Start a new event creation
    if user_id not in user_sessions:

        user_sessions[user_id] = {
            "step": "name"
        }

        await message.reply(
            "📅 Let's create an event!\n\nWhat is the name of your event?"
        )
        return

    session = user_sessions[user_id]

    # Event Name
    if session["step"] == "name":

        session["name"] = message.content.strip()
        session["step"] = "time"

        await message.reply(
            "🕒 What date and time is the event?"
        )
        return

    # Event Time
    if session["step"] == "time":

        session["time"] = message.content.strip()
        session["step"] = "location"

        await message.reply(
            "📍 What is the address or location?"
        )
        return

    # Event Location
    if session["step"] == "location":

        session["location"] = message.content.strip()

        await message.reply(
            f"""✅ **EVENT READY**

**WHAT**
{session['name']}

**WHEN**
{session['time']}

**WHERE**
{session['location']}

Now type `/create`.

Then copy the information above into the GroupFlows boxes.

You're done! 🎉"""
        )

        del user_sessions[user_id]


bot.run(TOKEN)
