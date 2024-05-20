import pulsar
import json

client = pulsar.Client("pulsar://localhost:6650")
repo_consumer = client.subscribe("repos", subscription_name="repos-sub")

keys = ["name", "owner", "has_tests", "has_ci_cd", "commits", "languages"]

while(True):
    data = repo_consumer.receive()
    repo_consumer.acknowledge(data)
    data = data.value()
    repo = json.loads(data)
    repo = {key: repo[key] for key in keys}
    print(json.dumps(repo))