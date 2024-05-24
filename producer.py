from github_requests import *
from utils import has_ci_cd, has_tests
import pulsar
import json
import logging
from datetime import timedelta, datetime

logging.getLogger().setLevel(logging.CRITICAL)

print("Sleeping for 20 seconds until pulsar is up")
sleep(20)

client = pulsar.Client('pulsar://pulsar_domain:6650')
repo_producer = client.create_producer('repos')

start_date = datetime(year=2024, month=5, day=1)
end_date = datetime(year=2024, month=5, day=4)
delta = timedelta(days=1)
count = 1

while start_date < end_date:
    for repo in get_repositories(start_date, start_date + delta):
        owner, name = repo["full_name"].split('/') # Iterate over each repository in the list
        workflows = get_repo_workflows(owner, name)  # Get the workflows of the repository

        repo["owner"] = owner
        repo["has_tests"] = has_tests(workflows)
        repo["has_ci_cd"] = has_ci_cd(workflows)
        repo["commits"] = get_commit_count(owner, name)
        repo["languages"] = get_repo_languages(owner, name)
        repo_producer.send(json.dumps(repo).encode())
        print(f"{count}) Done!")
        count += 1
    start_date += delta

client.close()