from __future__ import annotations

import re

import discord
from discord.ext import commands, tasks

from config import TOKEN

# Global const Variables
SPAM_CHANNEL_ID = 970823670702411810
PURPLE_COLOUR = 0x9678B6
MADGE_EMOTE = "<:DankMadgeThreat:1125591898241892482>"
MENTION_OWNER = "<@!312204139751014400>"
TEST_GUILD_ID = 759916212842659850
ALUBOT_ID = 713124699663499274
COMMAND_PREFIX = "^^^"
LALA_BOT_ID = 812763204010246174


class LalaBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents(
            guilds=True,
            members=True,
            presences=True,
            message_content=True,
            messages=True,
        )
        super().__init__(
            command_prefix=commands.when_mentioned_or(COMMAND_PREFIX),
            help_command=None,
            intents=intents,
        )
        self.counter: int = 0
        self.sent_already: bool = False

    async def setup_hook(self) -> None:
        self.watch_loop.start()

    async def on_ready(self):
        print(f"Logged in as {self.user}")

    @discord.utils.cached_property
    def test_guild(self) -> discord.Guild:
        return self.get_guild(TEST_GUILD_ID)  # type: ignore # known ID

    @tasks.loop(seconds=55)
    async def watch_loop(self):
        alubot: discord.Member = self.test_guild.get_member(ALUBOT_ID)  # type: ignore # known ID

        if alubot.status == discord.Status.online:
            self.counter = 0
            self.sent_already = False

        elif alubot.status == discord.Status.offline and not self.sent_already:
            self.counter += 1
            if self.counter > 11:
                content = "{0}, {1} {1} {1}".format(MENTION_OWNER, MADGE_EMOTE)
                embed = discord.Embed(color=PURPLE_COLOUR, title=f"{alubot.display_name} is now offline")
                spam_channel = self.test_guild.get_channel(SPAM_CHANNEL_ID)
                await spam_channel.send(content=content, embed=embed)  # type: ignore # known ID
                self.sent_already = True

    @watch_loop.before_loop
    async def before(self):
        await self.wait_until_ready()

    async def on_message(self, message: discord.Message, /) -> None:
        mention_regex = re.compile(rf"<@!?{LALA_BOT_ID}>")

        if mention_regex.fullmatch(message.content):
            await message.channel.send(f"allo {MADGE_EMOTE}")
            return

        await self.process_commands(message)

    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f"allo {MADGE_EMOTE}")


bot = LalaBot()


@bot.command(aliases=["help", "hello", "allo", "h", "a"])
async def ping(ctx: commands.Context):
    await ctx.send(f"allo {MADGE_EMOTE}")


bot.run(TOKEN)
bot.run(TOKEN)
bot.run(TOKEN)
bot.run(TOKEN)
