import discord
import logging
import logging.handlers
import os
from sql_helper import SQLConnection
from embed_helper import EmbedHelper

connection = SQLConnection()
embeds = EmbedHelper()
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

@tree.command(
    name="team",
    description="Get information about your current team",
    guild=discord.Object(id=server_id)
)
async def get_team_command(interaction):
    user_id = interaction.user.id
    team_id = connection.get_user_team_id(user_id)
    team_members = connection.get_team_members(team_id)
    team_name = connection.get_team_name(team_id)

    users = get_users(team_members, interaction.guild)

    embed = embeds.get_team_id_embed(interaction, team_name, users)
    await interaction.response.send_message(embed=embed)

@tree.command(
    name="create",
    description="Create a new team",
    guild=discord.Object(id=server_id)
)
async def create_team_command(interaction, name: str):
    user_id = interaction.user.id

    embed = embeds.get_cannot_create_team_embed(interaction)
    if connection.get_user_team_id(user_id) == None:
        team_id = connection.create_team(name, user_id)
        connection.add_player_to_team(user_id, team_id)
        embed = embeds.get_team_create_embed(interaction, name)
        connection.commit()

    await interaction.response.send_message(embed=embed)
    


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=server_id))

def get_users(user_id_rows, guild):
    if user_id_rows == None:
        return []
    users = [guild.get_member(member[0]) for member in user_id_rows]
    return users
    

client.run(os.environ['DISCORD_API_KEY'])