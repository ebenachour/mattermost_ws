from flask import Blueprint, request, abort
from matterbot.mattermost_helper import MatterbotHelper
from http import HTTPStatus
from matterbot.utils import validate_channel, validate_team

bot = Blueprint("bot", __name__)


@bot.route("/post", methods=["POST"])
def index():
    if not request.json:
        abort(HTTPStatus.BAD_REQUEST)
    request_data = request.get_json()
    expected_values = ["team_name", "channel_name", "message"]
    if sorted(expected_values) != sorted(request_data.keys()):
        abort(HTTPStatus.BAD_REQUEST, "Wrong parameters")
    matbot = MatterbotHelper()
    team_id = validate_team(matbot, request_data["team_name"])
    if not team_id:
        abort(
            HTTPStatus.BAD_REQUEST,
            "Given team {} is not valid".format(request_data["team_name"]),
        )
    channel_id = validate_channel(matbot, team_id, request_data["channel_name"])
    if not channel_id:
        abort(
            HTTPStatus.BAD_REQUEST,
            "Given channel {} is not valid".format(request_data["channel_name"]),
        )
    matbot.notify_mattermost(team_id, channel_id, request_data["message"])
    return ("OK", HTTPStatus.OK)
