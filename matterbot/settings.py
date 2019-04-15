import os

MATTERMOST_SETTTINGS = {
    "url": os.environ.get("MAT_URL"),
    "login_id": os.environ.get("MAT_LOGIN"),
    "password": os.environ.get("MAT_PWD"),
    "port": int(os.environ.get("MAT_PORT")),
}
