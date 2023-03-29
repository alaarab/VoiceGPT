import os
import discord
import asyncio
import random
from dotenv import load_dotenv
from discord.ext import commands
import openai
from gtts import gTTS

# Load environment variables from the .env file
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
discord_bot_key = os.getenv("DISCORD_BOT_KEY")

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

openai.api_key = openai_api_key

async def get_gpt_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"{prompt}",
        temperature=0.5,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].text.strip()

async def save_tts_async(tts, filename):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, tts.save, filename)

audio_queue = asyncio.Queue()

async def read_aloud(text, ctx):
    voice_channel = ctx.author.voice.channel
    if voice_channel:
        tts = gTTS(text, lang="en")
        await save_tts_async(tts, "response.mp3")
        voice_client = await voice_channel.connect()
        voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg", source="response.mp3"))
        while voice_client.is_playing():
            await asyncio.sleep(1)
        await voice_client.disconnect()

async def process_audio_queue():
    while True:
        source, voice_channel, ctx = await audio_queue.get()
        if not (voice_channel.guild.voice_client and voice_channel.guild.voice_client.is_connected()):
            voice_client = await voice_channel.connect()
        else:
            voice_client = voice_channel.guild.voice_client
        voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=source))
        while voice_client.is_playing():
            await asyncio.sleep(1)
        voice_client.stop()
        if audio_queue.empty():
            await voice_client.disconnect()

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

message_queue = asyncio.PriorityQueue()

async def process_message_queue():
    while True:
        _, ctx, question = await message_queue.get()
        response = await get_gpt_response(question)
        formatted_response = f"```\nUser: {ctx.author}\nQuestion: {question}\n\nResponse: {response}\n```"
        await ctx.send(formatted_response)
        await read_aloud(response, ctx)

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
    asyncio.run(main())