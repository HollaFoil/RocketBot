import discord

class EmbedHelper:
    def get_team_id_embed(self, interaction, team_name, users):
        if team_name == None:
            return get_team_id_embed_error(interaction)
        return get_team_id_embed_full(interaction, team_name, users)
    
    def get_team_create_embed(self, interaction, team_name):
        return get_team_created_embed(interaction, team_name)
    
    def get_cannot_create_team_embed(self, interaction):
        return get_team_create_embed_fail_in_team(interaction)
    
def get_team_id_embed_error(interaction):
    embed = discord.Embed(
        title = "You do not have a team!",
        description = "Create a new team by using `/create` or join an existing team.",
        color = discord.Color.red()
    )
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    embed.set_footer(text="Rocket League dalykas zdz", icon_url="https://styles.redditmedia.com/t5_3l3fel/styles/communityIcon_pir9p3ppjnga1.png")
    return embed

def get_team_id_embed_full(interaction, team_name, users):
    embed = discord.Embed(
        title = team_name,
        color = discord.Color.green()
    )

    players = ""
    for user in users:
        players += user.display_name + " (" + user.name + ")\n"

    embed.add_field(name="Members (" + str(len(users)) + "/3):", value=players, inline=False)
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    embed.set_footer(text="Rocket League dalykas zdz", icon_url="https://styles.redditmedia.com/t5_3l3fel/styles/communityIcon_pir9p3ppjnga1.png")
    return embed

def get_team_created_embed(interaction, team_name):
    embed = discord.Embed(
        title = "Team " + team_name + " has been created!",
        description = "Invite players to this team using the command `/invite <user>`.",
        color = discord.Color.green()
    )
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    embed.set_footer(text="Rocket League dalykas zdz", icon_url="https://styles.redditmedia.com/t5_3l3fel/styles/communityIcon_pir9p3ppjnga1.png")
    return embed

def get_team_create_embed_fail_in_team(interaction):
    embed = discord.Embed(
        title = "Failed to create a new team!",
        description = "You are already part of a team. Use `/team` to get info about your current team and `/leave` if you want to leave it.",
        color = discord.Color.red()
    )
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    embed.set_footer(text="Rocket League dalykas zdz", icon_url="https://styles.redditmedia.com/t5_3l3fel/styles/communityIcon_pir9p3ppjnga1.png")
    return embed