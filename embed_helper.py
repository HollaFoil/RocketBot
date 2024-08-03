import discord

error_footer = {
    'text':"If you believe this is an error, message an admin on discord.",
    'icon_url':"https://styles.redditmedia.com/t5_3l3fel/styles/communityIcon_pir9p3ppjnga1.png"
}

success_footer = {
    'text':"Lietuvos Rocket League Lyga",
    'icon_url':"https://styles.redditmedia.com/t5_3l3fel/styles/communityIcon_pir9p3ppjnga1.png"
}

class EmbedHelper:
    def get_team_embed(self, interaction, team_name, users, invited_users, team_owner):
        if team_name == None:
            return get_team_embed_error(interaction)
        return get_team_embed_full(interaction, team_name, users, invited_users, team_owner)
    
    def get_team_create_embed(self, interaction, team_name):
        return get_team_created_embed(interaction, team_name)
    
    def get_cannot_create_team_embed(self, interaction):
        return get_team_create_embed_fail_in_team(interaction)
    
    def get_sent_invite_embed(self, interaction, invited_user):
        return get_sent_invite_embed(interaction, invited_user)
    
    def get_user_already_invited_embed(self, interaction, invited_user):
        return get_sent_invite_user_already_invited_embed(interaction, invited_user)
    
    def get_user_already_part_of_team_embed(self, interaction, invited_user):
        return get_sent_invite_user_has_team_embed(interaction, invited_user)
    
    def get_team_cannot_have_more_members_embed(self, interaction, invited_user):
        return get_sent_invite_cannot_invite_more_users_embed(interaction, invited_user)
    
    def get_leave_team_embed(self, interaction):
        return get_leave_embed(interaction)
    
    def get_no_team_embed(self, interaction):
        return get_not_part_of_team_embed(interaction)
    
    def get_team_disbanded_embed(self, interaction):
        return get_team_disbanded_embed(interaction)
    
    def get_no_invitation_embed(self, interaction):
        return get_no_invitation_embed(interaction)
    
    def get_joined_team_embed(self, interaction, team_name):
        return get_join_team_embed(interaction, team_name)
    
    def get_reject_team_embed(self, interaction):
        return get_reject_team_embed(interaction)
    
    def get_no_invitations_embed(self, interaction):
        return get_no_invitations_embed(interaction)
    
    def get_invitations_embed(self, interaction, invitations):
        return get_invitations_embed(interaction, invitations)
    
    def get_not_owner_embed(self, interaction):
        return get_not_owner_embed(interaction)
    
    def get_user_kicked_embed(self, interaction, user):
        return get_user_kicked_embed(interaction, user)
    
    def get_target_not_in_team(self, interaction):
        return get_target_not_in_team(interaction)
    
    def get_make_captain_embed(self, interaction, user):
        return get_make_captain_embed(interaction, user)
    
    def get_same_target_embed(self, interaction):
        return get_same_target_embed(interaction)
    
def get_team_embed_error(interaction):
    embed = discord.Embed(
        title = "You do not have a team!",
        description = "Create a new team by using `/create` or join an existing team.",
        color = discord.Color.red()
    )
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    embed.set_footer(**error_footer)
    return embed

def get_team_embed_full(interaction, team_name, users, invited_users, team_owner):
    embed = discord.Embed(
        title = team_name,
        color = discord.Color.green()
    )

    players = ""
    for user in users:
        players += user.display_name + " (" + user.name + ")\n"

    pending = ""
    for user in invited_users:
        pending += user.display_name + " (" + user.name + ")\n"

    captain = team_owner.display_name + " (" + team_owner.name + ")\n"

    embed.add_field(name="Captain:", value=captain, inline=False)
    embed.add_field(name="Members (" + str(len(users)) + "/3):", value=players, inline=False)
    if invited_users != None and len(invited_users) > 0:
        embed.add_field(name="Pending invites:", value=pending, inline=False)
    embed.set_thumbnail(url=team_owner.display_avatar.url)
    embed.set_footer(**success_footer)
    return embed

def get_team_created_embed(interaction, team_name):
    embed = discord.Embed(
        title = "Team " + team_name + " has been created!",
        description = "Invite players to this team using the command `/invite <user>`.",
        color = discord.Color.green()
    )
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    embed.set_footer(**success_footer)
    return embed

def get_team_create_embed_fail_in_team(interaction):
    embed = discord.Embed(
        title = "Failed to create a new team!",
        description = "You are already part of a team. Use `/team` to get info about your current team and `/leave` if you want to leave it.",
        color = discord.Color.red()
    )
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    embed.set_footer(**error_footer)
    return embed

def get_sent_invite_embed(interaction, invited_user):
    embed = discord.Embed(
        title = invited_user.display_name + " has been invited to your team!",
        description = "This invite will expire in 24 hours. They can see their pending invites by typing `/invites` and can accept them by typing `/accept @team_owner`.",
        color = discord.Color.green()
    )
    embed.set_thumbnail(url=invited_user.display_avatar.url)
    embed.set_footer(**success_footer)
    return embed

def get_sent_invite_user_has_team_embed(interaction, invited_user):
    embed = discord.Embed(
        title = "Cannot invite user.",
        description = "This user is already part of a team. They can check out their current team via `/team` or leave it via `/leave`",
        color = discord.Color.red()
    )
    embed.set_thumbnail(url=invited_user.display_avatar.url)
    embed.set_footer(**error_footer)
    return embed

def get_sent_invite_user_already_invited_embed(interaction, invited_user):
    embed = discord.Embed(
        title = "Cannot invite user.",
        description = "This user has already been invited. They can check out their current invitations via `/invites` or join via `/accept @" + interaction.user.name + "`.",
        color = discord.Color.red()
    )
    embed.set_thumbnail(url=invited_user.display_avatar.url)
    embed.set_footer(**error_footer)
    return embed

def get_sent_invite_cannot_invite_more_users_embed(interaction, invited_user):
    embed = discord.Embed(
        title = "Cannot invite user.",
        description = "Your team cannot have any more members.",
        color = discord.Color.red()
    )
    embed.set_thumbnail(url=invited_user.display_avatar.url)
    embed.set_footer(**error_footer)
    return embed

def get_not_part_of_team_embed(interaction) :
    embed = discord.Embed(
        title = "You are not part of a team.",
        description = "You can create a team by typing `/create <team name>`.",
        color = discord.Color.red()
    )
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    embed.set_footer(**error_footer)
    return embed

def get_leave_embed(interaction) :
    embed = discord.Embed(
        title = "You have left your team.",
        description = "You can create a new team by typing `/create <team name>`, or you can join an existing one. Good luck!",
        color = discord.Color.green()
    )
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    embed.set_footer(**success_footer)
    return embed

def get_team_disbanded_embed(interaction):
    embed = discord.Embed(
        title = "Your team has been disbanded.",
        description = "You were the last member of your team.",
        color = discord.Color.green()
    )
    embed.add_field(name="", value="You can create a new team by typing `/create <team name>`, or you can join an existing one. Good luck!")
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    embed.set_footer(**success_footer)
    return embed

def get_no_invitation_embed(interaction):
    embed = discord.Embed(
        title = "Cannot find pending invite.",
        description = "This user has not invited you to any team.",
        color = discord.Color.red()
    )
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    embed.set_footer(**error_footer)
    return embed

def get_join_team_embed(interaction, team_name):
    embed = discord.Embed(
        title = "Joined " + team_name,
        description = "You can view information about your team by typing `/team`",
        color = discord.Color.green()
    )
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    embed.set_footer(**success_footer)
    return embed

def get_reject_team_embed(interaction):
    embed = discord.Embed(
        title = "Invite rejected",
        description = "You can view information about your invites by typing `/invites`",
        color = discord.Color.green()
    )
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    embed.set_footer(**success_footer)
    return embed

def get_no_invitations_embed(interaction):
    embed = discord.Embed(
        title = "You have no invitations",
        description = "You currently have no pending invites. Other users can invite you by typing `/invite`.",
        color = discord.Color.green()
    )
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    embed.set_footer(**success_footer)
    return embed

def get_invitations_embed(interaction, invitations):
    embed = discord.Embed(
        title = "You have " + str(len(invitations)) + " invitations",
        description = "You can join their team by typing `/accept @<user>`.",
        color = discord.Color.green()
    )

    for invitation in invitations:
        embed.add_field(name=invitation['team_name'], value="You were invited by " + invitation['user_name'])

    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    embed.set_footer(**success_footer)
    return embed

def get_not_owner_embed(interaction):
    embed = discord.Embed(
        title = "Operation failed",
        description = "You must be the team captain to do this.",
        color = discord.Color.red()
    )
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    embed.set_footer(**error_footer)
    return embed

def get_target_not_in_team(interaction):
    embed = discord.Embed(
        title = "Operation failed",
        description = "This player is not in your team.",
        color = discord.Color.red()
    )
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    embed.set_footer(**error_footer)
    return embed

def get_same_target_embed(interaction):
    embed = discord.Embed(
        title = "Operation failed",
        description = "You cannot select yourself for this operation",
        color = discord.Color.red()
    )
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    embed.set_footer(**error_footer)
    return embed

def get_user_kicked_embed(interaction, user):
    embed = discord.Embed(
        title = user.display_name + " was kicked from your team",
        description = "You can view your team by typing `/team`.",
        color = discord.Color.green()
    )
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    embed.set_footer(**success_footer)
    return embed

def get_make_captain_embed(interaction, user):
    embed = discord.Embed(
        title = user.display_name + " is now captain",
        description = "You can view your team by typing `/team`.",
        color = discord.Color.green()
    )
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    embed.set_footer(**success_footer)
    return embed