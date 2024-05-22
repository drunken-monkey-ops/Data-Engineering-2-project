import requests
import re
from requests.models import PreparedRequest
from utils import get_headers
from datetime import datetime

def get_repo_workflows(owner: str, repo: str) -> list:
    uri = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows"

    request_params = {"per_page": 100}

    req_url = PreparedRequest()  # Prepare the full URL with query parameters
    req_url.prepare_url(uri, request_params)
    req_url = req_url.url

    elements = []

    while True:
        response = requests.get(req_url, headers=get_headers())
        if response.status_code != 200:    #Print an error message if the request fails
            print(   
                f"Failed to fetch repositories: {response.status_code}, message: {response.json().get('message')}"
            )
            break
        
        data = response.json()
        if data["total_count"] > 0:
            elements.extend(data["workflows"]) # If workflows are found, add them to the list
        
        if "next" in response.links:    # Check if there's a next page
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
    return int(re.findall(r'\d+', response.links["last"]["url"])[-1])
    

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

    while True:
        response = requests.get(req_url, headers=get_headers())
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
