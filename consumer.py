import pulsar

client = pulsar.Client("pulsar://<your-ip>:6650")

repo_consumer = client.subscribe("repos", subscription_name="repos-sub")

while(True):
    print(repo_consumer.receive().value())