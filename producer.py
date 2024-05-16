from github_requests import get_repositories, get_commit_count, get_repo_content
from utils import has_ci_cd, has_tests
import pulsar
import json

client = pulsar.Client('pulsar://pulsar_domain:6650')

repo_producer = client.create_producer('repos')

repos = get_repositories()

for i in range(5):
    repo = repos[i]
    owner, name = repo["full_name"].split('/')
    content = get_repo_content(owner, name)
    repo["has_tests"] = has_tests(content)
    repo["has_ci_cd"] = has_ci_cd(content)
    repo["commits"] = get_commit_count(owner, name)
    repo_producer.send(json.dumps(repo).encode())
    print("done!")

client.close()