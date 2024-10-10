from __future__ import annotations

import re
from typing import Self, TypedDict, override

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
GLORIA_ID = 1293739303473774702
COMMAND_PREFIX = "^^^"
LALA_BOT_ID = 812763204010246174


class WatchStatus(TypedDict):
    counter: int
    sent_already: bool


class LalaBot(commands.Bot):
    def __init__(self) -> None:
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
        self.watching: dict[int, WatchStatus] = {
            bot_id: {"counter": 0, "sent_already": False}
            for bot_id in [
                ALUBOT_ID,
                GLORIA_ID,
            ]
        }  # mapping bot id -> WatchStatus

    @override
    async def setup_hook(self) -> None:
        self.watch_loop.start()

    async def on_ready(self) -> None:
        print(f"Logged in as {self.user}")

    @discord.utils.cached_property
    def test_guild(self) -> discord.Guild:
        return self.get_guild(TEST_GUILD_ID)  # pyright: ignore[reportReturnType]

    @discord.utils.cached_property
    def spam_channel(self) -> discord.TextChannel:
        return self.test_guild.get_channel(SPAM_CHANNEL_ID)  # pyright: ignore[reportReturnType]

    @tasks.loop(seconds=55)
    async def watch_loop(self) -> None:
        for bot_id, watch_status in self.watching.items():
            bot: discord.Member = self.test_guild.get_member(bot_id)  # pyright: ignore[reportAssignmentType]

            if bot.status == discord.Status.online:
                watch_status["counter"] = 0
                watch_status["sent_already"] = False

            elif bot.status == discord.Status.offline and not watch_status["sent_already"]:
                watch_status["counter"] += 1
                if watch_status["counter"] > 11:
                    content = "{0}, {1} {1} {1}".format(MENTION_OWNER, MADGE_EMOTE)
                    embed = discord.Embed(color=PURPLE_COLOUR, title=f"{bot.display_name} is now offline")
                    await self.spam_channel.send(content=content, embed=embed)
                    watch_status["sent_already"] = True

    @watch_loop.before_loop
    async def before(self) -> None:
        await self.wait_until_ready()

    @override
    async def on_message(self, message: discord.Message, /) -> None:
        mention_regex = re.compile(rf"<@!?{LALA_BOT_ID}>")

        if mention_regex.fullmatch(message.content):
            await message.channel.send(f"allo {MADGE_EMOTE}")
            return

        await self.process_commands(message)

    @override
    async def on_command_error(self, ctx: commands.Context[Self], error: commands.CommandError) -> None:
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f"allo {MADGE_EMOTE}")


bot = LalaBot()


@bot.command(aliases=["help", "hello", "allo", "h", "a"])
async def ping(ctx: commands.Context[LalaBot]) -> None:
    await ctx.send(f"allo {MADGE_EMOTE}")


bot.run(TOKEN)
