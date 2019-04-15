import pytest
from matterbot import create_app
from http import HTTPStatus
from mock import MagicMock

app = pytest.fixture(scope="session")(create_app)


@pytest.mark.parametrize(
    "json, team_id, channel_id, message",
    [
        (None, None, None, ""),
        ({"ove": "ove"}, None, None, "Wrong parameters"),
        ({"channel_id": "ove", "team_name": "tata"}, None, None, "Wrong parameters"),
        (
            {"channel_name": "ove", "team_name": "tata", "message": "coucou"},
            None,
            None,
            "Given team tata is not valid",
        ),
        (
            {"channel_name": "ove", "team_name": "tata", "message": "coucou"},
            22,
            None,
            "Given channel ove is not valid",
        ),
    ],
)
def test_post_error(monkeypatch, app, json, team_id, channel_id, message):
    monkeypatch.setattr(
        "matterbot.views.validate_team", MagicMock(return_value=team_id)
    )
    monkeypatch.setattr(
        "matterbot.views.validate_channel", MagicMock(return_value=channel_id)
    )
    with app.test_client() as cli:
        res = cli.post("/post", json=json)
        assert res._status_code == int(HTTPStatus.BAD_REQUEST)


def test_post_success(monkeypatch, app):
    monkeypatch.setattr("matterbot.views.validate_team", MagicMock(return_value=21))
    monkeypatch.setattr("matterbot.views.validate_channel", MagicMock(return_value=33))
    monkeypatch.setattr(
        "matterbot.mattermost_helper.MatterbotHelper.notify_mattermost", MagicMock(True)
    )
    with app.test_client() as cli:
        res = cli.post(
            "/post", json={"channel_name": "ove", "team_name": "ove", "message": "ove"}
        )
        assert res._status_code == int(HTTPStatus.OK)


def test_not_found(app):
    with app.test_client() as cli:
        res = cli.get("/coucou")
        assert res._status_code == int(HTTPStatus.NOT_FOUND)
