import asyncio
import os
import json
from discord.ext import commands
from discord import Embed
from Games.LostArk.build import Build
from Games.LostArk.skill import Skill
from main import bot


class LostArk(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Lost_Ark Cog')

    @commands.group(name="lost_ark", invoke_without_command=True)
    async def lost_ark(self, ctx):
        pass

    @lost_ark.command(name="build")
    async def build(self, ctx):
        classes = json.load(open(f'{os.getcwd()}/Games/LostArk/classes.json'))
        message = "Elige la clase:\n"

        for idx, class_ in enumerate(classes):
            message += "{0}: {1}\n".format(idx+1, class_["name"].capitalize())

        reply = await ctx.reply(message)

        def classExists(i, classes):
            return i >= 0 and i <= len(classes)

        def checkClass(m):
            if m.content.isdigit() != True:
                return False
            if classExists(i=int(m.content), classes=classes) != True:
                return False
            return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

        try:
            class_idx = await bot.wait_for("message", check=checkClass, timeout=10)
        except asyncio.TimeoutError:
            await reply.edit(content="Operacion cancelada, timeout")
            return

        class_idx = int(class_idx.content)

        if class_idx == 0:
            await reply.edit(content="Cancelado")
            return

        message = "Elige una clase avanzada:\n"

        for idx, advanced_class in enumerate(classes[class_idx-1]["advanced_classes"]):
            message += "{0}: {1}\n".format(idx+1, advanced_class.capitalize())

        await reply.edit(content=message)

        def advancedClassCheck(m):
            if m.content.isdigit() != True:
                return False
            if classExists(i=int(m.content), classes=classes[class_idx-1]["advanced_classes"]) != True:
                return False
            return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

        try:
            advanced_class_idx = await bot.wait_for("message", check=advancedClassCheck, timeout=10)
            await reply.edit(content="Awantame tantillo...")
        except asyncio.TimeoutError:
            await reply.edit(content="Operacion cancelada, timeout")
            return

        advanced_class_idx = int(advanced_class_idx.content)

        class_name = classes[class_idx-1]['name']
        advanced_class_name = classes[class_idx -
                                      1]['advanced_classes'][advanced_class_idx-1]

        builds = Build(class_name, advanced_class_name).search_builds()

        message = "Elige una build:\n"

        for idx, build in enumerate(builds):
            message += "{0}: {1} <{2}>\n".format(idx+1,
                                                 build.get_name(), build.get_url())

        await reply.edit(content=message)

        def buildClassCheck(m):
            if m.content.isdigit() != True:
                return False
            return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id and int(m.content) > 0 and int(m.content) <= len(builds)

        try:
            build_idx = await bot.wait_for("message", check=buildClassCheck, timeout=10)
            await reply.edit(content="Awantame tantillo...")
        except asyncio.TimeoutError:
            await reply.edit(content="Operacion cancelada, timeout")
            return

        build_idx = int(build_idx.content)

        build = builds[build_idx-1]

        description = ""

        build.set_skills(Skill().search_skills(build.get_url()))

        for skill in build.get_skills():
            description += "{0}: {1}\n".format(skill.get_name(),
                                               skill.get_level())

        description += "Original: {0}".format(build.get_url())

        embed = Embed(title=build.get_name(),
                      url=build.get_url(), description=description)

        embed.set_image(url=build.get_image_url())

        await ctx.reply(embed=embed)


def setup(client):
    client.add_cog(LostArk(client))
