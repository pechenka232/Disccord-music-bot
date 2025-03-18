import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import asyncio

TOKEN = "ТВОЙ_ТОКЕН"

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Подключение к голосовому каналу
@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send("🔊 Бот подключился к голосовому каналу!")
    else:
        await ctx.send("❌ Ты должен находиться в голосовом канале!")

# Отключение от голосового канала
@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("🔌 Бот отключился от голосового канала.")
    else:
        await ctx.send("❌ Бот не подключен к голосовому каналу.")

# Воспроизведение музыки (YouTube, Spotify, SoundCloud)
@bot.command()
async def play(ctx, url):
    if not ctx.voice_client:
        await ctx.invoke(join)  # Подключается, если не подключен

    ctx.voice_client.stop()
    
    # Поддержка YouTube, Spotify, SoundCloud
    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192"
        }]
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info["url"]
        source = await discord.FFmpegOpusAudio.from_probe(url2, method="fallback")
        ctx.voice_client.play(source)
        await ctx.send(f"🎶 Сейчас играет: **{info['title']}**")

# Остановка музыки
@bot.command()
async def stop(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("⏹ Музыка остановлена.")
    else:
        await ctx.send("❌ Нечего останавливать!")

# Пауза
@bot.command()
async def pause(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("⏸ Музыка на паузе.")
    else:
        await ctx.send("❌ Нечего ставить на паузу!")

# Продолжить воспроизведение
@bot.command()
async def resume(ctx):
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("▶ Музыка продолжается!")
    else:
        await ctx.send("❌ Музыка не на паузе.")

bot.run(TOKEN)
