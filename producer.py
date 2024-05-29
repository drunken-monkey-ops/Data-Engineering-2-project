from pulsar import Client, ConsumerType, ProducerAccessMode
import logging
from datetime import timedelta, datetime
from utils import read_tokens

print("Starting producer!")

logging.getLogger().setLevel(logging.CRITICAL)

client = Client('pulsar://pulsar_domain:6650')

consumer_ready = client.subscribe("consumer-ready", subscription_name="consumer-ready-sub", consumer_type=ConsumerType.Shared)

print("Waiting for consumers...")
data = consumer_ready.receive()
consumer_ready.acknowledge(data)
consumer_ready.close()

token_producer = client.create_producer("tokens", access_mode=ProducerAccessMode.Shared)
for token in read_tokens():
    print(f"{token} inserted!")
    token_producer.send(token.encode())
token_producer.close()


start_date = datetime(year=2023, month=5, day=1)
end_date = datetime(year=2024, month=4, day=30)
delta = timedelta(days=1)

date_producer = client.create_producer("dates", access_mode=ProducerAccessMode.Shared)
while start_date <= end_date:
    date_producer.send(start_date.isoformat().encode())
    print(f"{start_date} inserted!")
    start_date += delta
date_producer.close()

client.close()