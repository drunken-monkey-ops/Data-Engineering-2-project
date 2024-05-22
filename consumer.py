from pymongo import MongoClient
import pulsar
import json
from os import environ as env

client_ip = env["IP_CLIENT"] if "IP_CLIENT" in env else "localhost"
pulsar_ip = env["IP"] if "IP" in env else "localhost"

print(f"Client IP: {client_ip}")
print(f"Pulsar IP: {pulsar_ip}")

mongo_client = MongoClient(f"mongodb://{client_ip}:27017/")
db = mongo_client["repo_database"]
collection = db["repo_collection"]

print(f"pulsar://{pulsar_ip}:6650")

pulsar_client = pulsar.Client(f"pulsar://{pulsar_ip}:6650")
repo_consumer = pulsar_client.subscribe("repos", subscription_name="repos-sub")

# Define the keys we are interested in from the incoming Pulsar messages
keys = ["name", "owner", "has_tests", "has_ci_cd", "commits", "languages", "created_at"]

while True:
    data = repo_consumer.receive()
    repo_consumer.acknowledge(data)

    data = data.value() # Get the actual content of the message
    repo = json.loads(data)  # Parse the JSON content of the message into a Python dictionary
    repo = {key: repo[key] for key in keys} # Filter the dictionary to include only the keys we are interested in//dictionary comprehension.

    if collection.count_documents({"name": repo["name"], "owner": repo["owner"]}) == 0:
        insert_result = collection.insert_one(repo)

    print(json.dumps(repo))
