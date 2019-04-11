def validate_team(matbot, team_name):
    return matbot.get_team_id(team_name)

def validate_channel(matbot, team_id, channel_name):
    return matbot.get_channel_id(team_id, channel_name)

