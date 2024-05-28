import requests
import re
from requests.models import PreparedRequest
from utils import read_tokens, TOKENS
from datetime import datetime
from time import sleep

current_token = {
    "core": {"token": "", "remaining": -1, "sleep_time": 60 * 60, "limit": 5000},
    "search": {
        "token": "",
        "remaining": -1,
        "sleep_time": 60,
        "limit": 30,
    },
}

def get_token(type: str):
    global TOKENS
    if not TOKENS:
        TOKENS = read_tokens()

    if current_token[type]["remaining"] <= 0:
        token_found = False
        for token in TOKENS:
            if token != current_token[type]["token"]:
                data = get_rate_limit(token)
                if data[type]["remaining"] > 0:
                    current_token[type]["token"] = token
                    current_token[type]["remaining"] = data[type]["remaining"]
                    token_found = True
                    break
        if not token_found:
            print("Sleeping...")
            sleep(current_token[type]["sleep_time"])
            current_token[type]["remaining"] = current_token[type]["limit"]

    current_token[type]["remaining"] -= 1
    return current_token[type]["token"]


def get_headers(type: str = "core", token: str = None) -> dict:
    headers = {
        "User-Agent": "Thunder Client (https://www.thunderclient.com)",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token != "":
        headers["Authorization"] = f"Bearer {token if token else get_token(type)}"
    return headers


def get_rate_limit(token: str):
    req_url = f"https://api.github.com/rate_limit"

    response = requests.get(req_url, headers=get_headers(token=token))
    if response.status_code != 200:
        print(
            f"Failed to fetch repositories: {response.status_code}, message: {response.json().get('message')}"
        )
    return response.json()["resources"]


def get_repo_workflows(owner: str, repo: str) -> list:
    uri = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows"

    request_params = {"per_page": 100}

    req_url = PreparedRequest()  # Prepare the full URL with query parameters
    req_url.prepare_url(uri, request_params)
    req_url = req_url.url

    elements = []

    while True:
        response = requests.get(req_url, headers=get_headers())
        if response.status_code != 200:  # Print an error message if the request fails
            print(
                f"Failed to fetch repositories: {response.status_code}, message: {response.json().get('message')}"
            )
            break

        data = response.json()
        if data["total_count"] > 0:
            elements.extend(
                data["workflows"]
            )  # If workflows are found, add them to the list

        if "next" in response.links:  # Check if there's a next page
            req_url = response.links["next"]["url"]
        else:
            break

    return elements


def get_repo_languages(owner: str, repo: str) -> list:
    uri = f"https://api.github.com/repos/{owner}/{repo}/languages"

    request_params = {"per_page": 100}

    req_url = PreparedRequest()
    req_url.prepare_url(uri, request_params)
    req_url = req_url.url

    elements = []

    while True:
        response = requests.get(req_url, headers=get_headers())
        if response.status_code != 200:
            print(
                f"Failed to fetch repositories: {response.status_code}, message: {response.json().get('message')}"
            )
            break
        elements.extend(response.json().keys())
        if "next" in response.links:
            req_url = response.links["next"]["url"]
        else:
            break

    return elements


def get_repo_content(owner: str, repo: str) -> list:
    uri = f"https://api.github.com/repos/{owner}/{repo}/contents"

    request_params = {"per_page": 100}

    req_url = PreparedRequest()
    req_url.prepare_url(uri, request_params)
    req_url = req_url.url

    elements = []

    while True:
        response = requests.get(req_url, headers=get_headers())
        if response.status_code != 200:
            print(
                f"Failed to fetch repositories: {response.status_code}, message: {response.json().get('message')}"
            )
            break
        elements.extend(response.json())
        if "next" in response.links:
            req_url = response.links["next"]["url"]
        else:
            break

    return elements


def get_commit_count(owner: str, repo: str) -> int:
    uri = f"https://api.github.com/repos/{owner}/{repo}/commits"

    # https://stackoverflow.com/a/70610670
    request_params = {"per_page": 1}

    req_url = PreparedRequest()
    req_url.prepare_url(uri, request_params)
    req_url = req_url.url

    response = requests.get(req_url, headers=get_headers())
    if response.status_code != 200:
        print(
            f"Failed to fetch repositories: {response.status_code}, message: {response.json().get('message')}"
        )
    return int(re.findall(r"\d+", response.links["last"]["url"])[-1])


def get_repositories_count(from_date: datetime, to_date: datetime) -> int:
    search_params = [
        "license:mit",
        "license:apache-2.0",
        "license:gpl-3.0",
        "license:mpl-2.0",
        f"created:{from_date.strftime('%Y-%m-%d')}..{to_date.strftime('%Y-%m-%d')}",
    ]

    uri = f"https://api.github.com/search/repositories"
    request_params = {"q": " ".join(search_params), "order": "desc", "per_page": 1}

    req_url = PreparedRequest()
    req_url.prepare_url(uri, request_params)
    req_url = req_url.url

    response = requests.get(req_url, headers=get_headers())
    if response.status_code != 200:
        print(
            f"Failed to fetch repositories: {response.status_code}, message: {response.json().get('message')}"
        )
    return int(re.findall(r"\d+", response.links["last"]["url"])[-1])

    

def get_repositories(from_date: datetime, to_date: datetime):
    search_params = [
        "license:mit",
        "license:apache-2.0",
        "license:gpl-3.0",
        "license:mpl-2.0",
        f"created:{from_date.strftime('%Y-%m-%d')}..{to_date.strftime('%Y-%m-%d')}",
    ]

    uri = f"https://api.github.com/search/repositories"
    request_params = {"q": " ".join(search_params), "order": "desc", "per_page": 100}

    req_url = PreparedRequest()
    req_url.prepare_url(uri, request_params)
    req_url = req_url.url

    while True:
        response = requests.get(req_url, headers=get_headers("search"))
        if response.status_code != 200:
            print(
                f"Failed to fetch repositories: {response.status_code}, message: {response.json().get('message')}"
            )
            break

        for repo in response.json()["items"]:
            yield repo

        if "next" in response.links:
            req_url = response.links["next"]["url"]
        else:
            break
