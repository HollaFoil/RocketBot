import discord
import logging
import logging.handlers
import os
from sql_helper import SQLConnection
from embed_helper import EmbedHelper

connection = SQLConnection()
embeds = EmbedHelper()

max_team_size = 3

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
async def get_team_command(interaction, ):
    user_id = interaction.user.id
    team_id = connection.get_user_team_id(user_id)
    team_members = connection.get_team_members(team_id)
    team_invitations = connection.get_team_invitations(team_id)
    team_name = connection.get_team_name(team_id)
    team_owner = connection.get_team_owner(team_id)

    users = get_users(team_members, interaction.guild)
    invited_users = get_users(team_invitations, interaction.guild)
    team_owner = None if team_owner == None else interaction.guild.get_member(team_owner)

    embed = embeds.get_team_embed(interaction, team_name, users, invited_users, team_owner)
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
        connection.delete_invites(user_id)
        embed = embeds.get_team_create_embed(interaction, name)

    await interaction.response.send_message(embed=embed)
    connection.commit()

@tree.command(
    name="invite",
    description="Invite a user to your team",
    guild=discord.Object(id=server_id)
)
async def invite_player_command(interaction, user: discord.Member):
    user_id = interaction.user.id
    team_id = connection.get_user_team_id(user_id)

    embed = None
    if not connection.check_player_has_team(user_id):
        embed = embeds.get_no_team_embed(interaction)
    elif connection.get_total_team_size(team_id) >= max_team_size:
        embed=embeds.get_team_cannot_have_more_members_embed(interaction, user)
    elif connection.check_player_has_team(user.id):
        embed = embeds.get_user_already_part_of_team_embed(interaction, user)
    elif connection.check_player_invited(user.id, team_id):
        embed = embeds.get_user_already_invited_embed(interaction, user)
    else:
        connection.add_player_invitation(user.id, team_id, user_id)
        embed = embeds.get_sent_invite_embed(interaction, user)

    await interaction.response.send_message(embed=embed)
    connection.commit()

@tree.command(
    name="leave",
    description="Leave your current team",
    guild=discord.Object(id=server_id)
)
async def leave_team_command(interaction):
    user_id = interaction.user.id
    team_id = connection.get_user_team_id(user_id)
    owner_id = connection.get_team_owner(team_id)
    player_count = connection.count_team_players(team_id)

    embed = None
    if team_id == None:
        embed = embeds.get_no_team_embed(interaction)
    elif player_count == 1:
        embed = embeds.get_team_disbanded_embed(interaction)
        connection.delete_team(team_id)
    else:
        connection.delete_player_from_team(team_id, user_id)
        if user_id == owner_id:
            connection.change_team_owner(team_id)
        embed = embeds.get_leave_team_embed(interaction)

    await interaction.response.send_message(embed=embed)
    connection.commit()

@tree.command(
    name="accept",
    description="Accept an invitation from a user",
    guild=discord.Object(id=server_id)
)
async def accept_invite_command(interaction, user: discord.Member):
    user_id = interaction.user.id
    team_id = connection.get_user_team_id(user.id)
    team_name = connection.get_team_name(team_id)

    embed = None
    if not connection.check_player_invited(user_id, team_id):
        embed = embeds.get_no_invitation_embed(interaction)
    else:
        embed = embeds.get_joined_team_embed(interaction, team_name)
        connection.add_player_to_team(user_id, team_id)
        connection.delete_invites(user_id)

    await interaction.response.send_message(embed=embed)
    connection.commit()
    
@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=server_id))

def get_users(user_id_rows, guild):
    if user_id_rows == None:
        return []
    users = [guild.get_member(member[0]) for member in user_id_rows]
    return users
    

client.run(os.environ['DISCORD_API_KEY'])