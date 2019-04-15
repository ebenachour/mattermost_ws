from datetime import datetime

from tabulate import tabulate

from mattermostdriver import Driver
from mattermostdriver.exceptions import ResourceNotFound
from matterbot.settings import MATTERMOST_SETTTINGS


class MatterbotHelper(object):
    def __init__(self):
        self.session = None

    def connect(self, port=443):
        self.session = Driver(MATTERMOST_SETTTINGS)
        self.session.login()

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
            channel = self.session.channels.get_channel_by_name(
                team_id=team_id, channel_name=channel_name
            )
            return channel["id"]
        except ResourceNotFound:
            return None

    def notify_mattermost(self, team_id, channel_id, message):
        try:
            self.connect()
            msg_to_send = self.format_message(message)
            self.session.posts.create_post(
                options={"channel_id": channel_id, "message": message}
            )
        except:
            raise

    def format_message(self, message):
        # it is very bad, but for the moment, i dont have another idea. Sorry PythonGod
        if isinstance(message, dict) and sorted(["success", "errors"]) == sorted(
            message.keys()
        ):
            # take all the possiblities
            try:
                errors = message["errors"].items()
            except AttributeError:
                errors = message.get("errors", None)
            time_start = datetime.now().strftime("%Y-%m-%d %H:%M")

            table = tabulate(
                errors, headers=["test", "errors"], tablefmt="pipe"
            )
            nb_success = len(message["success"])
            succes = ",".join(message["success"])

            message = """**{} nighty test result**
    {} tests succeded.
    Succeeded tests are : {}

    **FAILS**


    {}
    """.format(
                time_start, nb_success, succes, table
            )
        return message
