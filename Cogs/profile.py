from discord.ext import commands
from discord import Embed
from discord.ext.commands import Context
from discord import Client


class Profile(commands.Cog):

    def __init__(self, client: Client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Profile Cog')

    @commands.command(name="avatar")
    async def build(self, ctx: Context, user_id: str = None):
        if not user_id:
            user = await self.client.fetch_user(user_id=ctx.author.id)
        else:
            user = await self.client.fetch_user(removeExtraCharactersFromUserId(user_id=user_id))

        embed = Embed(title="{0}#{1}".format(user.name, user.discriminator))
        embed.set_image(url=user.avatar_url)

        await ctx.reply(embed=embed)


def removeExtraCharactersFromUserId(user_id: str) -> int:
    characters_to_remove = "<!@>"

    for character in characters_to_remove:
        user_id = user_id.replace(character, "")

    return user_id


def setup(client):
    client.add_cog(Profile(client))
