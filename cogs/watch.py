from discord import Embed, Status
from discord.ext import commands, tasks


class Sid:
    alu = 702561315478044804


class Clr:
    prpl = 0x9678b6


class Cid:
    logs = 731615128050598009


class Uid:
    irene = 312204139751014400
    bot = 713124699663499274


def umntn(id_):
    return f'<@!{id_}>'


class Ems:
    MadgeThreat = '<:DankMadgeThreat:854318972102770728>'


class CheckMainBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.checkmain.start()
        self.counter = 0
        self.sent_already = 0

    @commands.command(
        aliases=['help', 'hello', 'allo', 'h', 'a']
    )
    async def ping(self, ctx: commands.Context):
        await ctx.send(f'allo {Ems.MadgeThreat}')

    @tasks.loop(seconds=55)  # minutes=5)
    async def checkmain(self):
        server = self.bot.get_guild(Sid.alu)
        send_channel = server.get_channel(Cid.logs)
        member = server.get_member(Uid.bot)

        if member.status == Status.online:
            self.counter = 0
            self.sent_already = 0

        if member.status == Status.offline:
            self.counter += 1

        if self.counter > 11 and self.sent_already == 0:
            self.sent_already = 1
            content = '{0}, {1} {1} {1}'.format(umntn(Uid.irene), Ems.MadgeThreat)
            em = Embed(
                color=Clr.prpl,
                title=f"{member.display_name} is now offline"
            )
            await send_channel.send(content=content, embed=em)

    @checkmain.before_loop
    async def before(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(CheckMainBot(bot))

