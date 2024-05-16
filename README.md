# Data-Engineering-2-project
### Instruction to run Github crawler
- Clone the repository
- Create a yml file name config.yml
- Paste your git token as shown below
``` YAML

token: "GITHUB_API_TOKEN"

```
- Create the virtual environment and install the necessaty packages

``` bash
python3 -m venv env
python3 -m pip install -r requirements.txt
```

- Run the file using below command.

``` bash
python3 python_crawler.py
```

### Producer

- You can start the producer by running

``` bash
sudo docker compose -f composers/producer_compose.yml up
```
- Then you can run the test consumer!
``` bash
python3 consumer.py
```