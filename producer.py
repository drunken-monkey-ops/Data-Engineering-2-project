from github_requests import *
from utils import has_ci_cd, has_tests
import pulsar
import json

client = pulsar.Client('pulsar://pulsar_domain:6650')

repo_producer = client.create_producer('repos')

repos = get_repositories()

for repo in get_repositories():
    owner, name = repo["full_name"].split('/')
    content = get_repo_content(owner, name)
    workflows = get_repo_workflows(owner, name)

    repo["owner"] = owner
    repo["has_tests"] = has_tests(content, workflows)
    repo["has_ci_cd"] = has_ci_cd(workflows)
    repo["commits"] = get_commit_count(owner, name)
    repo["languages"] = get_repo_languages(owner, name)
    repo_producer.send(json.dumps(repo).encode())

client.close()