import yaml
import re
from os import environ
from pathlib import Path

TOKENS = []

"""
You can either:
    * set the TOKEN variable with the token
    * set an environment variable called "github_token" in your OS with the token
    * create a yaml file called "config.yml" in this same directory, with an attribute called "token"
"""
def read_tokens() -> list:
    if (Path.cwd() / "config.yml").exists():
        with open("config.yml", "r") as config:
            return yaml.safe_load(config)["tokens"]
    elif "github_token" in environ:
        return environ["github_token"].split(',')
    raise Exception("No token!")

def keyword_in_text(text: str, keyword: str) -> bool:
    re_match = re.search(r"\b{keyword}\b".format(keyword=keyword), text)
    return True if re_match else False

def has_tests(workflows: list) -> bool:
    keywords = ["test", "tests", "testing"]
    
    for workflow in workflows:
        if any(map(lambda x: keyword_in_text(workflow["name"], x), keywords)):
            return True

    return False

def has_ci_cd(workflows: list) -> bool:
    return True if workflows else False
