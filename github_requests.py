import requests
from requests.models import PreparedRequest
from utils import get_headers
from datetime import datetime


def get_commit_count(owner: str, repo: str) -> int:
    uri = f"https://api.github.com/repos/{owner}/{repo}/commits"

    request_params = {"per_page": 100}

    req_url = PreparedRequest()
    req_url.prepare_url(uri, request_params)
    req_url = req_url.url

    commit_count = 0

    while True:
        response = requests.get(req_url, headers=get_headers())
        if response.status_code != 200:
            print(
                f"Failed to fetch repositories: {response.status_code}, message: {response.json().get('message')}"
            )
            break
        commit_count += len(response.json())
        if "links" in response and "next" in response.links:
            req_url = response.links["next"]["url"]
        else:
            break

    return commit_count


def get_repositories(from_date: datetime = None, to_date: datetime = None):
    from_date = from_date if from_date else datetime(year=2023, month=5, day=1)
    to_date = to_date if to_date else datetime(year=2024, month=5, day=1)
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

    repos = []

    while True:
        response = requests.get(req_url, headers=get_headers())
        if response.status_code != 200:
            print(
                f"Failed to fetch repositories: {response.status_code}, message: {response.json().get('message')}"
            )
            break
        repos.extend(response.json()["items"])
        if "links" in response and "next" in response.links:
            req_url = response.links["next"]["url"]
        else:
            break

    return repos