import os
import time
import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")

# Replace with your actual channel ID
EVENT_CHANNEL_ID = 123456789012345678

# 5 minutes
SESSION_TIMEOUT = 300

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

    if message.channel.id != EVENT_CHANNEL_ID:
        return

    user_id = message.author.id
    content = message.content.strip()

    # Cancel current event creation
    if content.lower() in ["cancel", "stop", "quit", "exit"]:

        if user_id in user_sessions:
            del user_sessions[user_id]

        await message.reply(
            "❌ Event creation cancelled.\n\nType anything to start a new event."
        )

        return

    # Check timeout
    if user_id in user_sessions:

        elapsed = time.time() - user_sessions[user_id]["last_activity"]

        if elapsed > SESSION_TIMEOUT:

            del user_sessions[user_id]

            await message.reply(
                "⏰ Your previous event request timed out after 5 minutes.\n\nLet's start over.\n\nWhat is the name of your event?"
            )

            user_sessions[user_id] = {
                "step": "name",
                "last_activity": time.time()
            }

            return

    # Start new session
    if user_id not in user_sessions:

        user_sessions[user_id] = {
            "step": "name",
            "last_activity": time.time()
        }

        await message.reply(
            "📅 Let's create an event!\n\nWhat is the name of your event?\n\n(Type 'cancel' anytime to stop.)"
        )

        return

    session = user_sessions[user_id]
    session["last_activity"] = time.time()

    # Step 1 - Event Name
    if session["step"] == "name":

        session["name"] = content
        session["step"] = "time"

        await message.reply(
            "🕒 What date and time is the event?\n\n(Type 'cancel' anytime to stop.)"
        )

        return

    # Step 2 - Event Time
    if session["step"] == "time":

        session["time"] = content
        session["step"] = "location"

        await message.reply(
            "📍 What is the address or location?\n\n(Type 'cancel' anytime to stop.)"
        )

        return

    # Step 3 - Event Location
    if session["step"] == "location":

        session["location"] = content
        session["step"] = "description"

        await message.reply(
            "📝 Optional: What is the event description?\n\nType 'skip' to leave this blank.\n\n(Type 'cancel' anytime to stop.)"
        )

        return

    # Step 4 - Event Description
    if session["step"] == "description":

        description_text = ""

        if content.lower() != "skip":
            description_text = f" description: {content}"

        await message.reply(
            f"""✅ EVENT READY

Copy and paste this into Discord:

`/create what: {session['name']} when: {session['time']} where: {session['location']}{description_text}`

📱 On mobile? If it doesn't work the first time, delete it and paste again.

👥 Want RSVP limits? Open the Activity Page after creating the event.

Type anything below to start another event.
"""
        )

        del user_sessions[user_id]


bot.run(TOKEN)
