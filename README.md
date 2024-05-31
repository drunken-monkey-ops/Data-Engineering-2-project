# Github Analytics using Apache pulsar

Folder struct and description.
``` bash
├── CloudInit 
│   ├── cloud-init.yaml
│   └── config.sh
├── DATA ANALYSES.ipynb
├── README.md
├── composers ----------------> required docker files
│   ├── consumer_compose.yml
│   ├── db_compose.yml
│   ├── producer_compose.yml
│   └── pulsar_standalone_compose.yml
├── config.yml --------------------> github tokens
├── consumer.py ----------------------> consumer python 
├── db_dump.tar.gz
├── deploy -----------> cloud configuration and start instance script
│   ├── consumer-cloud-config.txt
│   ├── producer-cloud-config.txt
│   └── start_instance.py
├── github_requests.py 
├── images --------------> Docker images
│   ├── consumer
│   └── producer
├── producer.py ------------> producer script
├── requirements.txt ------------> python requirements file
├── test.py -------------> test file 
└── utils.py ------------------> all the utility functio to transform JSON response into a meaningful JSON and token ingestion.
```


## Description
Our project aims to address limitations by creating an analytic system that uses Apache Pulsar, a streaming framework, to collect and analyze GitHub repository metadata in real-time. The system will investigate key questions about the top ten programming languages, project activity, and development methodologies such as test-driven development and DevOps practices in the last year. To overcome the restrictions of the GitHub API for data collection and to answer these questions, we have designed a specific system architecture using Apache Pulsar and Docker. We selected Apache Pulsar for its capability to handle high-throughput, low-latency data streams and its support for scalable, distributed systems. Furthermore, in the final part of our project, we aim to assess the scalability of our architecture to ensure that it can handle varying workloads and maintain performance. 

![Untitled-2024-05-29-1639 (1)](https://github.com/drunken-monkey-ops/Data-Engineering-2-project/assets/66768769/080eaf8a-fe2e-45bf-be42-884a330e8182)

## Prerequistes
- Python 3
- Pulsar client python library
- Docker
- openstack clients
- novaclient
- keystone python library

Don't worry, everything is specified in the requirements.txt and cloud configuration text files, so all components will be installed in the cloud during initialization. 😃
## How to run the files 😜
+ Download the RC file from SNIC cloud
+ source the RC file
  ``` shell
    source project_name.rc
  ```
+ Clone the repo
+ Change directory to cloned gihub repo
  ``` shell
  cd Data-Engineering-2-project
  ```
+ create a config.yml file adding all the github token
  ``` yaml
    token:
     - "GITHUN TOKEN"
  ```
+ move inside deploy folder
   ```shell
  cd deploy
   ```
+ Open the consumer cloud config.txt file with your favourite text editor and add the client VM's ip address near the client VM variable
+ Open the start_instance.py file and enter your key pair name in the create instance function. Then run the start instance by running the start instance script
+ wait some time till to apply all the configurations inside the newly created VM's
+ start the mongodb docker compose file
``` shell
docker compose -f composers/db_compose.yml up -d
```
+ Once everything up and running you could ssh into the producer and consumer VM using your pem key and run the docker ps file to see the container's running.
+ After the data has been accumulated, you can use Jupyter Notebook to access the accumulated data and perform further analysis on the GitHub repository data.
## Results 
We gathered  200,000 GitHub repositories and conducted an analysis on programming languages, CI/CD usage, and the frequency of updates based on commits. We also identified the top 10 programming languages for test-driven development and CI/CD. One challenge we encountered was the varying rate limits provided by GitHub for retrieving data and searching for metadata. Additionally, we faced difficulties with message loss between the producer and consumer. To address this issue, we ensured that each piece of data was transferred, and in case of data loss, the resent message would be sent to Apache Pulsar to retrieve the lost message for the consumer. 

![image](https://github.com/drunken-monkey-ops/Data-Engineering-2-project/assets/66768769/fc080914-7746-4032-b472-332522b83724)
![image](https://github.com/drunken-monkey-ops/Data-Engineering-2-project/assets/66768769/86d27217-61b3-48cc-b662-8e55d2872510)
![image](https://github.com/drunken-monkey-ops/Data-Engineering-2-project/assets/66768769/d4d67e1f-bb76-4803-8568-d4b83cf13fd1)
![image](https://github.com/drunken-monkey-ops/Data-Engineering-2-project/assets/66768769/fed2ce32-e5b7-45e1-a0dd-e0c8703f2c24)

Scalability Result:

![Speedup_Strong_Scaling_111](https://github.com/drunken-monkey-ops/Data-Engineering-2-project/assets/57313821/64cd676f-86fd-4c0b-a872-e65ccc0ecdee)
![Efficiency_Strong_Scaling_1111](https://github.com/drunken-monkey-ops/Data-Engineering-2-project/assets/57313821/cf79f6ea-0f32-4f23-9bf9-6b24dc83cb6d)
