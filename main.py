import discord
from discord.ext import commands
from os import system as sys
from youtube_dl import YoutubeDL
from discord.utils import get
from youtubesearchpython import VideosSearch


FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    # bind to ipv4 since ipv6 addresses cause issues sometimes
    'source_address': '0.0.0.0'
}

bot = commands.Bot(command_prefix='.')


@bot.event
async def on_ready():
    print('Bot is up and running!')


@bot.command(name='ping', help='Returning the current ping time the bot takes to respond')  # Ping
async def ping(ctx):
    await ctx.send(f'Current ping is {round(bot.latency * 1000)}ms')


@bot.command(name='join', help='Joining the voice channel')  # Join
async def join(ctx):
    channel = ctx.author.voice.channel
    if channel:
        await channel.connect()
    else:
        await ctx.send('You need to join a voice channel first!')


@bot.command(name='leave', help='Leaving the voice channel')  # Leave
async def leave(ctx):
    player = get(bot.voice_clients, guild=ctx.guild)
    if player.is_playing():
        player.stop()
    channel = ctx.message.guild.voice_client
    if channel:
        await channel.disconnect()
    else:
        await ctx.send('You need to be in a voice channel for this command to work')


# Play
@bot.command(name='play', help='Playing a song from YouTube', aliases=['p'])
async def play(ctx, *url):
    song = ' '.join(url)
    channel = ctx.author.voice.channel
    if channel:
        try:
            player = await channel.connect()
        except:
            player = get(bot.voice_clients, guild=ctx.guild)
        with YoutubeDL(YDL_OPTIONS) as ydl:
            videosSearch = VideosSearch(song, limit=1)
            url = 'https://www.youtube.com/watch?v=' + \
                videosSearch.result()['result'][0]['id']
            info = ydl.extract_info(url, download=False)
            URL = info['url']
            player.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
            await ctx.send(f'Now playing: {info["title"]}')
            await ctx.send(url)
    else:
        await ctx.send('You need to join a voice channel first!')


@bot.command(name='stop', help='Stopping the song')  # Stop
async def stop(ctx):
    channel = ctx.author.voice.channel
    if channel:
        player = get(bot.voice_clients, guild=ctx.guild)
        if player.is_playing():
            player.stop()
    else:
        await ctx.send('You need to be in a voice channel for this command to work')


@bot.command(name='pause', help='Pausing the song')  # Pause
async def pause(ctx):
    channel = ctx.author.voice.channel
    if channel:
        player = get(bot.voice_clients, guild=ctx.guild)
        if player.is_playing():
            player.pause()
    else:
        await ctx.send('You need to be in a voice channel for this command to work')


@bot.command(name='resume', help='Resuming the song')  # Resume
async def resume(ctx):
    channel = ctx.author.voice.channel
    if channel:
        player = get(bot.voice_clients, guild=ctx.guild)
        if player.is_paused():
            player.resume()
    else:
        await ctx.send('You need to be in a voice channel for this command to work')


def main():
    sys('cls')
    bot.run('TOKEN')


if __name__ == '__main__':
    main()
