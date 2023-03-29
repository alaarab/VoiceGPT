import os
import discord
import asyncio
import random
from dotenv import load_dotenv
from discord.ext import commands
import openai
from gtts import gTTS

try:
    # Load environment variables from the .env file
    load_dotenv()
except Exception as e:
    print(f"Error loading environment variables: {e}")
    exit(1)

try:
    openai_api_key = os.getenv("OPENAI_API_KEY")
    discord_bot_key = os.getenv("DISCORD_BOT_KEY")
except Exception as e:
    print(f"Error getting API keys from environment variables: {e}")
    exit(1)

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.guilds = True
intents.reactions = True
intents.emojis = True
intents.voice_states = True
intents.typing = False
intents.presences = False
intents.invites = True
intents.integrations = True
intents.webhooks = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

try:
    openai.api_key = openai_api_key
except Exception as e:
    print(f"Error setting OpenAI API key: {e}")
    exit(1)

async def get_gpt_response(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"{prompt}",
            temperature=0.5,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
    except Exception as e:
        print(f"Error getting GPT response: {e}")
        return "Sorry, I couldn't process your request. Please try again later."
    return response.choices[0].text.strip()

async def save_tts_async(tts, filename):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, tts.save, filename)

async def read_aloud(text, ctx):
    if ctx.author.voice and ctx.author.voice.channel:
        voice_channel = ctx.author.voice.channel
        try:
            tts = gTTS(text, lang="en")
            await save_tts_async(tts, "response.mp3")
            voice_client = await voice_channel.connect()
            voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg", source="response.mp3"))
            while voice_client.is_playing():
                await asyncio.sleep(1)
            await voice_client.disconnect()
        except Exception as e:
            print(f"Error reading aloud: {e}")
            await ctx.send("Sorry, I couldn't read the response aloud. Please try again later.")
    else:
        await ctx.send("You must be in a voice channel for the bot to read the response aloud.")

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='ask')
async def ask(ctx, *, question):
    response = await get_gpt_response(question)
    formatted_response = f"```\nUser: {ctx.author}\nQuestion: {question}\n\nResponse: {response}\n```"
    await ctx.send(formatted_response)
    await read_aloud(response, ctx)

async def main():
    try:
        await bot.start(discord_bot_key)
    except KeyboardInterrupt:
        await bot.close()
    except Exception as e:
        print(f"An error occurred: {e}")
        await bot.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"An error occurred while running the main loop: {e}")
        exit(1)