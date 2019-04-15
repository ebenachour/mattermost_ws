import pytest
from mock import MagicMock
from matterbot.mattermost_helper import MatterbotHelper
from mattermostdriver.exceptions import ResourceNotFound
@pytest.mark.parametrize(
    "message, result",
    [
        (None, None),
        ("mon message", "mon message"),
    ])
def test_format_message_str(message, result):
    output = MatterbotHelper().format_message(message)
    assert output == result

@pytest.mark.parametrize(
    "message",
    [
        ({"success":['1','2'], "errors": {('x','y'), ('z', 'u')}}),
        ({"success":['1','2'], "errors": {'x':'y', 'z':'u'}}),

    ])
def test_format_message_dict(message):
    output = MatterbotHelper().format_message(message)
    #import pdb; pdb.set_trace()
    print(output)
    assert isinstance(output, str)
    res = output.split('\n')
    assert ','.join(message['success']) in res[2]

def test_team_id_resource_not_found(monkeypatch):
    monkeypatch.setattr('mattermostdriver.driver.Teams.get_team_by_name', MagicMock(side_effect=ResourceNotFound()))
    monkeypatch.setattr('mattermostdriver.Driver.login', MagicMock(return_value=True))
    assert MatterbotHelper().get_team_id('coucou') is None

def test_channel_id_resource_not_found(monkeypatch):
    monkeypatch.setattr('mattermostdriver.driver.Channels.get_channel_by_name', MagicMock(side_effect=ResourceNotFound()))
    monkeypatch.setattr('mattermostdriver.Driver.login', MagicMock(return_value=True))
    assert MatterbotHelper().get_channel_id('222', 'coucou') is None


def test_channel_ok(monkeypatch):
    monkeypatch.setattr('mattermostdriver.Driver.login', MagicMock(return_value=True))
    monkeypatch.setattr('mattermostdriver.driver.Channels.get_channel_by_name', MagicMock(return_value={"id":'2333'}))
    assert MatterbotHelper().get_channel_id('222', 'coucou') == '2333'


def test_team_ok(monkeypatch):
    monkeypatch.setattr('mattermostdriver.Driver.login', MagicMock(return_value=True))
    monkeypatch.setattr('mattermostdriver.driver.Teams.get_team_by_name', MagicMock(return_value={"id": '2333'}))
    assert MatterbotHelper().get_team_id('coucou') == '2333'


