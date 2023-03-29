import discord
from discord.ext import commands, tasks

from config import TOKEN

# Global const Variables
SPAM_CHANNEL_ID = 970823670702411810
PURPLE_COLOUR = 0x9678b6
MADGE_EMOTE = '<:DankMadgeThreat:854318972102770728>'
MENTION_IRENE = '<@!312204139751014400>'
TEST_GUILD_ID = 759916212842659850
ALUBOT_ID = 713124699663499274


class LalaBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='^^^',
            help_command=None,
            intents=discord.Intents(
                guilds=True,
                members=True,
                presences=True,
                message_content=True,
                messages=True
            )
        )
        self.counter = 0
        self.sent_already = 0

    async def setup_hook(self) -> None:
        # start the task to run in the background
        self.watch_loop.start()

    async def on_ready(self):
        print(f'Logged in as {self.user}')

    # TYPE HINT MOMENTS

    @property
    def test_guild(self) -> discord.Guild:
        return self.get_guild(TEST_GUILD_ID)  # type: ignore # known ID

    @property
    def alubot(self) -> discord.Member:
        return self.test_guild.get_member(ALUBOT_ID) # type: ignore # known ID

    @property
    def spam_channel(self) -> discord.TextChannel:
        return self.test_guild.get_channel(SPAM_CHANNEL_ID)  # type: ignore # known ID
    
    # THE LOOP ITSELF

    @tasks.loop(seconds=55)
    async def watch_loop(self):
        alubot = self.alubot

        if alubot.status == discord.Status.online:
            self.counter = 0
            self.sent_already = 0

        if alubot.status == discord.Status.offline:
            self.counter += 1

        if self.counter > 11 and self.sent_already == 0:
            self.sent_already = 1
            c = '{0}, {1} {1} {1}'.format(MENTION_IRENE, MADGE_EMOTE)
            e = discord.Embed(color=PURPLE_COLOUR, title=f"{alubot.display_name} is now offline")
            await self.spam_channel.send(content=c, embed=e)

    @watch_loop.before_loop
    async def before(self):
        await self.wait_until_ready()


bot = LalaBot()


@bot.command(aliases=['help', 'hello', 'allo', 'h', 'a'])
async def ping(ctx: commands.Context):
    await ctx.send(f'allo {MADGE_EMOTE}')


bot.run(TOKEN)
