import pulsar
import logging
from datetime import timedelta, datetime
from utils import read_tokens

print("Starting producer!")

logging.getLogger().setLevel(logging.CRITICAL)

client = pulsar.Client('pulsar://pulsar_domain:6650')
date_producer = client.create_producer("dates")
token_producer = client.create_producer("tokens")

start_date = datetime(year=2023, month=5, day=1)
end_date = datetime(year=2024, month=4, day=30)
delta = timedelta(days=1)

while start_date <= end_date:
    date_producer.send(start_date.isoformat().encode())
    start_date += delta

for token in read_tokens():
    token_producer.send(token.encode())

client.close()