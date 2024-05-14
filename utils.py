import yaml
from os import environ
from pathlib import Path

TOKEN = ""

"""
You can either:
    * set the TOKEN variable with the token
    * set an environment variable called "github_token" in your OS with the token
    * create a yaml file called "config.yml" in this same directory, with an attribute called "token"
"""


def get_token() -> str:
    if TOKEN:
        return TOKEN
    print(Path.cwd())
    if (Path.cwd() / "config.yml").exists():
        with open("config.yml", "r") as config:
            return yaml.safe_load(config)["token"]
    if "github_token" in environ:
        return environ["github_token"]


def get_headers() -> dict:
    return {
        "User-Agent": "Thunder Client (https://www.thunderclient.com)",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {get_token()}",
    }
