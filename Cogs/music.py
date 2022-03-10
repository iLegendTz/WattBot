import discord
from discord.ext import commands
from discord import Client
from discord.ext.commands import Context
from discord import VoiceClient
from discord import Embed

import youtube_dl


class Music(commands.Cog):
    def __init__(self, client: Client) -> None:
        self.client = client
        self.title = None
        self.url = None

    def set_url(self, url: str):
        self.url = url

    def set_title(self, title: str):
        self.title = title

    def set_thumbnail(self, thumbnail: str):
        self.thumbnail = thumbnail

    def clear_info(self):
        self.title = None
        self.url = None
        self.thumbnail = None

    @commands.Cog.listener()
    async def on_ready(self):
        print("Music Cog")

    @commands.command(name="leave")
    async def leave(self, ctx: Context):
        if ctx.author.voice is None:
            await ctx.reply('No estas en ningun canal de voz')
            return

        await ctx.guild.voice_client.disconnect()

    @commands.group(name="msc", invoke_without_command=True)
    async def msc(self, ctx: Context):
        pass

    @msc.command(name="play")
    async def play(self, ctx: Context, url):

        if ctx.author.voice is None:
            await ctx.reply('No estas en ningun canal de voz')
            return

        await ctx.author.voice.channel.connect()

        vc: VoiceClient = ctx.voice_client

        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'
        }
        YDL_OPTIONS = {'format': 'bestaudio'}

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url=url, download=False)
            url2 = info['formats'][0]['url']
            self.set_title(info.get('title', None))
            self.set_url(url)
            self.set_thumbnail(info['thumbnails'][-1]['url'])

            source = await discord.FFmpegOpusAudio.from_probe(
                url2, **FFMPEG_OPTIONS)
            vc.play(source, after=lambda e: self.clear_info())

    @msc.command(name="pause")
    async def pause(self, ctx: Context):
        if ctx.author.voice is None:
            await ctx.reply('No estas en ningun canal de voz')
            return

        vc: VoiceClient = ctx.voice_client

        if vc is None:
            await ctx.reply('Nada reproduciendo')
        else:
            vc.pause()

    @msc.command(name="resume")
    async def resume(self, ctx: Context):
        if ctx.author.voice is None:
            await ctx.reply('No estas en ningun canal de voz')
            return

        vc: VoiceClient = ctx.voice_client

        if vc is None:
            return

        if vc.is_paused():
            vc.resume()

    @msc.command(name="info")
    async def info(self, ctx: Context):
        if not self.title and not self.url:
            await ctx.reply('Nada reproduciendo')
            return

        embed = Embed()
        embed.title = self.title
        embed.url = self.url
        embed.description = self.url
        embed.set_image(url=self.thumbnail)

        await ctx.reply(embed=embed)


def setup(client):
    client.add_cog(Music(client))
