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
    raise Exception("No token!")


def get_headers() -> dict:
    return {
        "User-Agent": "Thunder Client (https://www.thunderclient.com)",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {get_token()}",
    }


def has_tests(items: list) -> bool:
    keywords = ["test", "tests"]
    for item in items:
        if item["name"] in keywords:
            return True
    return False


def has_ci_cd(items: list) -> bool:
    keywords = [
        # ".github/work/flows",  # GitHub Actions
        ".circleci",  # CircleCI
        ".gitlab-ci.yml",  # GitLab CI
        ".travis.yml",  # Travis CI
        "azure-pipelines.yml",  # Azure Pipelines
        "Jenkinsfile",  # Jenkins
        ".ci",  # Custom setups or various CI/CD tools
        ".ci-config",  # Alternative custom setups
    ]

    for item in items:
        if item["name"] in keywords:
            return True
    return False
