from pymongo import MongoClient
import pulsar
import json

mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["repo_database"]
collection = db["repo_collection"]

pulsar_client = pulsar.Client("pulsar://localhost:6650")
repo_consumer = pulsar_client.subscribe("repos", subscription_name="repos-sub")

keys = ["name", "owner", "has_tests", "has_ci_cd", "commits", "languages", "created_at"]

while True:
    data = repo_consumer.receive()
    repo_consumer.acknowledge(data)

    data = data.value()
    repo = json.loads(data)
    repo = {key: repo[key] for key in keys}

    if collection.count_documents({"name": repo["name"], "owner": repo["owner"]}) == 0:
        insert_result = collection.insert_one(repo)

    # print(json.dumps(repo))
