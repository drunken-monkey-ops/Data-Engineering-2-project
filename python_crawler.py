import requests
import yaml
import time
import json


with open('config.yml' , 'r') as config:
    api_token = yaml.safe_load(config)['token']

url = "https://api.github.com/search/repositories?q=license:mit+license:apache-2.0+license:gpl-3.0+license:mpl-2.0&order=desc"


headers = {'Authorization': f'api_token' , 'X-GitHub-Api-Version': '2022-11-28'}

response = requests.request("GET", url, headers=headers)

repos_all = []
page = 1
while True:
    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch repositories: {response.status_code}, message: {response.json().get('message')}")
        break
    print(f'fetching....{page}')
    data = response.json()
    repos_all.extend(data['items'])

    if 'next' in response.links:
        url = response.links['next']['url']
    else:
        url = None
        break
    time.sleep(10)
    page+=1

with open('data.json' , 'w') as data:
    json.dump(repos_all , data)
