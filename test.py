from pymongo import MongoClient
from datetime import datetime, timedelta
from calendar import monthrange
from github_requests import get_repositories_count
import json

mongo_client = MongoClient(f"mongodb://130.238.28.90:27017/")
db = mongo_client["repo_database"]
collection = db["repo_collection"]

# data = []
# for i in collection.find({}):
#     i["_id"] = str(i["_id"])
#     data.append(i)
# print(data[0])
# with open("out.json", "w") as file:
#     json.dump(data, file, indent=4) 

# search = {
#     "created_at": {
#         "$gt": datetime(year=2023, month=6, day=1).isoformat(),
#         "$lt": datetime(year=2023, month=6, day=30).isoformat(),
#     }
# }

start = datetime(year=2023, month=5, day=1)
end = datetime(year=2024, month=5, day=1)

while start <= end:
    delta = timedelta(days=monthrange(2024, start.month)[1] - 1)
    search = {
        "created_at": {
            "$gt": start.isoformat(),
            "$lt": (start + delta).isoformat(),
        }
    }
    print(f"{start.isoformat()}) {collection.count_documents(search)}")
    start += timedelta(days=monthrange(2024, start.month)[1])

# safing/mmdbmeld.
for i in collection.find({"owner": "safing", "name": "mmdbmeld"}):
    print(i)
print(collection.count_documents({}))


# start = datetime(year=2023, month=5, day=1)
# end = datetime(year=2023, month=5, day=31)
# delta = timedelta(days=1)
# count = 0
# repo_count = {}
# while start <= end:
#     repo_count[count] = get_repositories_count(start, start + delta)
#     print(f"{count}) {repo_count[count]}")
#     count += 1
#     start += delta
