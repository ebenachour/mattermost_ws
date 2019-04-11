from datetime import datetime

from tabulate import tabulate

from mattermostdriver import Driver
from mattermostdriver.exceptions import ResourceNotFound
from matterbot.settings import MATTERMOST_SETTTINGS

class MatterbotHelper(object):
    def __init__(self):
        self.session = None

    def connect(self, port=443):
        try:
            print(MATTERMOST_SETTTINGS)
            self.session = Driver(MATTERMOST_SETTTINGS)
            self.session.login()
        except Exception:
            raise

    def get_team_id(self, team_name):
        try:
            self.connect()
            team = self.session.teams.get_team_by_name(team_name)
            return team["id"]
        except ResourceNotFound:
            return None

    def get_channel_id(self, team_id, channel_name):
        try:
            self.connect()
            channel = self.session.channels.get_channel_by_name(team_id=team_id,channel_name=channel_name)
            return channel["id"]
        except ResourceNotFound:
            return None

    def notify_mattermost(self, team_id, channel_id, success, errors):
        time_start = datetime.now().strftime("%Y-%m-%d %H:%M")
        try:
            self.connect()
            table = tabulate(errors, headers=["test", "errors"], tablefmt="pipe")

            message = """**{} nighty test result**
{} tests succeded.
Succeeded tests are : {}

**FAILS**


{}
""".format(time_start, len(success), ','.join(success), table)

            self.session.posts.create_post(options={
                                           'channel_id': channel_id,
                                           'message': message})
        except Exception:
            raise
