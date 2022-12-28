from discord import Embed, Intents, Status
from discord.ext import commands, tasks

from config import TOKEN

# Global const Variables
Cid_spam_me = 970823670702411810
Clr_prpl = 0x9678b6
Ems_MadgeThreat = '<:DankMadgeThreat:854318972102770728>'
Mntn_Irene = '<@!312204139751014400>'
Sid_christ = 759916212842659850
Uid_bot = 713124699663499274


class MandaraBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='^^^',
            help_command=None,
            intents=Intents(
                guilds=True,
                members=True,
                presences=True,
                message_content=True
            )
        )
        self.counter = 0
        self.sent_already = 0

    async def setup_hook(self) -> None:
        # start the task to run in the background
        self.checkmain.start()

    async def on_ready(self):
        print(f'Logged in as {self.user}')

    @tasks.loop(seconds=55)
    async def checkmain(self):
        alubot = self.get_guild(Sid_christ).get_member(Uid_bot)

        if alubot.status == Status.online:
            self.counter = 0
            self.sent_already = 0

        if alubot.status == Status.offline:
            self.counter += 1

        if self.counter > 11 and self.sent_already == 0:
            self.sent_already = 1
            content = '{0}, {1} {1} {1}'.format(Mntn_Irene, Ems_MadgeThreat)
            em = Embed(
                color=Clr_prpl,
                title=f"{alubot.display_name} is now offline"
            )
            await self.get_channel(Cid_spam_me).send(content=content, embed=em)

    @checkmain.before_loop
    async def before(self):
        await self.wait_until_ready()


bot = MandaraBot()


@bot.command(aliases=['help', 'hello', 'allo', 'h', 'a'])
async def ping(ctx: commands.Context):
    await ctx.send(f'allo {Ems_MadgeThreat}')


bot.run(TOKEN)
