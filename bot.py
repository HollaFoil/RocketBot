import discord
import logging
import logging.handlers
import os

server_id = 1268936879936508077

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logging.getLogger('discord.http').setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename='discord.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=2,  # Rotate through 5 files
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

# Add the guild ids in which the slash command will appear.
# If it should be in all, remove the argument, but note that
# it will take some time (up to an hour) to register the
# command if it's for all guilds.
@tree.command(
    name="addplayer",
    description="Add a player to your team",
    guild=discord.Object(id=server_id)
)
async def first_command(interaction, member: discord.Member):
    embed = discord.Embed(
        title="Player registered!",
        description=member.display_name + " has been successfully added to your team.",
        color=discord.Color.green()
    )

    players = ""
    players += "HollaFoil (Epic: HollaFoil)\n"
    players += member.display_name + " (Epic: botAccount)\n"

    embed.add_field(name="Current players (2/3):", value=players, inline=False)
    embed.set_footer(text="Rocket League dalykas zdz", icon_url="https://styles.redditmedia.com/t5_3l3fel/styles/communityIcon_pir9p3ppjnga1.png")
    embed.set_thumbnail(url=member.display_avatar.url)
    await interaction.response.send_message(embed=embed)

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=server_id))

client.run(os.environ['DISCORD_API_KEY'])