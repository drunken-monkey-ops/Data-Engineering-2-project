from github_requests import get_repositories
import json

with open("data.json", "w") as data:
    json.dump(get_repositories(), data)
