import pulsar

client = pulsar.Client("pulsar://localhost:6650")

repo_consumer = client.subscribe("repos", subscription_name="repos-sub")


while(True):
    print(repo_consumer.receive().value())