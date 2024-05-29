from pymongo import MongoClient
from pulsar import Client, ConsumerType
from datetime import datetime, timedelta
from github_requests import get_repositories, get_commit_count, get_repo_workflows, get_repo_languages
from utils import has_ci_cd, has_tests, TOKENS
from os import environ as env
from sys import exit

client_ip = env["IP_CLIENT"] if "IP_CLIENT" in env else "localhost"
pulsar_ip = env["IP"] if "IP" in env else "localhost"

print(f"Client IP: {client_ip}")
print(f"Pulsar IP: {pulsar_ip}")

mongo_client = MongoClient(f"mongodb://{client_ip}:27017/")
db = mongo_client["repo_database"]
collection = db["repo_collection"]

pulsar_client = Client(f"pulsar://{pulsar_ip}:6650")
token_consumer = pulsar_client.subscribe("tokens", subscription_name="tokens-sub", consumer_type=ConsumerType.Shared)
date_consumer = pulsar_client.subscribe("dates", subscription_name="dates-sub", consumer_type=ConsumerType.Shared)

start_producer = pulsar_client.create_producer("consumer-ready")
start_producer.send("start!".encode())

for _ in range(2):
    try:
        data = token_consumer.receive(30000)
        token_consumer.acknowledge(data)
        token = data.value().decode()
        print(f"Token {token} adquired!")
        TOKENS.append(token)
    except Exception as e:
        print(f"Error retrieving token: {str(e)}")
token_consumer.close()

if not TOKENS:
    print("No token...")
    exit(1)

keys = ["name", "owner", "has_tests", "has_ci_cd", "commits", "languages", "created_at"]
delta = timedelta(days=1)
count = 1

while True:
    data = date_consumer.receive()
    date_consumer.acknowledge(data)
    date = datetime.fromisoformat(data.value().decode())

    for repo in get_repositories(date, date + delta):
        owner, name = repo["full_name"].split(
                "/"
            )  # Iterate over each repository in the list
        try:
            workflows = get_repo_workflows(
                owner, name
            )  # Get the workflows of the repository

            repo["owner"] = owner
            repo["has_tests"] = has_tests(workflows)
            repo["has_ci_cd"] = has_ci_cd(workflows)
            repo["commits"] = get_commit_count(owner, name)
            repo["languages"] = get_repo_languages(owner, name)

            # repo_producer.send(json.dumps(repo).encode())
            repo = {
                key: repo[key] for key in keys
            }  # Filter the dictionary to include only the keys we are interested in//dictionary comprehension.

            print(f"{count}) Done with {owner}/{name}...")
            insert_result = collection.insert_one(repo)
            count += 1
        except Exception as e:
            print(f"Failed on {owner}/{name}: {str(e)}")
    count = 1