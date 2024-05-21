# http://docs.openstack.org/developer/python-novaclient/ref/v2/servers.html
import time, os, sys, random
import inspect
from os import environ as env
import re
from  novaclient import client
import keystoneclient.v3.client as ksclient
from keystoneauth1 import loading
from keystoneauth1 import session

flavor = "ssc.large"
private_net = "UPPMAX 2024/1-4 Internal IPv4 Network"
floating_ip_pool_name = "Public External IPv4 Network"
floating_ip = "130.238.29.215"
image_name = "Ubuntu 20.04 - 2023.12.07"

identifier = random.randint(1000,9999)

loader = loading.get_plugin_loader('password')

auth = loader.load_from_options(auth_url=env['OS_AUTH_URL'],
                                username=env['OS_USERNAME'],
                                password=env['OS_PASSWORD'],
                                project_name=env['OS_PROJECT_NAME'],
                                project_domain_id=env['OS_PROJECT_DOMAIN_ID'],
                                #project_id=env['OS_PROJECT_ID'],
                                user_domain_name=env['OS_USER_DOMAIN_NAME'])

sess = session.Session(auth=auth)
nova = client.Client('2.1', session=sess)
print ("user authorization completed.")

image = nova.glance.find_image(image_name)

flavor = nova.flavors.find(name=flavor)

if private_net != None:
    net = nova.neutron.find_network(private_net)
    nics = [{'net-id': net.id}]
else:
    sys.exit("private-net not defined.")

#print("Path at terminal when executing this file")
print(os.getcwd() + "\n")
producer_cfg_file_path = os.getcwd()+'/producer-cloud-config.txt'


if os.path.isfile(producer_cfg_file_path):
    userdata_producer = open(producer_cfg_file_path)

else:
    sys.exit("cloud-cfg.txt is not in current working directory")



secgroups = ['default']

# print(userdata_producer , userdata_consumer)

print ("Creating instance .. ")

instance = nova.servers.create(name="prod_server_with_docker", image=image, flavor=flavor,userdata=userdata_producer, nics=nics,security_groups=secgroups)

# In case you want to login to the production server
instance_producer = nova.servers.create(name="producer_group_9", image=image, flavor=flavor, key_name='DE_2_key',userdata=userdata_producer, nics=nics,security_groups=secgroups)


inst_status_prod = instance_producer.status

print ("waiting for 10 seconds.. ")
time.sleep(10)

while inst_status_prod == 'BUILD' :
    print ("Instance: "+instance_producer.name+" is in "+inst_status_prod+" state, sleeping for 5 seconds more...")

    time.sleep(5)
    instance_producer = nova.servers.get(instance_producer.id)
    inst_status_prod = instance_producer.status


ip_address_prod = None
for network in instance_producer.networks[private_net]:
    if re.match('\d+\.\d+\.\d+\.\d+', network):
        ip_address_prod = network
        break
if ip_address_prod is None:
    raise RuntimeError('No IP address assigned!')



print ("Instance: "+ instance_producer.name +" is in " + inst_status_prod + " state" + " ip address: "+ ip_address_prod)

consumer_cfg_file_path = os.getcwd()+'/consumer-cloud-config.txt'
if os.path.isfile(consumer_cfg_file_path):
    lines = ''
    with open(consumer_cfg_file_path) as file:
        lines = ''.join(file.readlines())
    lines = lines.replace("{var_1}", f"'{ip_address_prod}'")
    with open(consumer_cfg_file_path, 'w') as file:
        file.write(lines)
    userdata_consumer = open(consumer_cfg_file_path)

print("Rest for sometime.......")

time.sleep(30)
instance_consumer = nova.servers.create(name="consumer_group_9", image=image, flavor=flavor, key_name='DE_2_key',userdata=userdata_consumer, nics=nics,security_groups=secgroups)
inst_status_cons = instance_consumer.status

print ("waiting for 10 seconds.. ")
time.sleep(10)
while inst_status_cons == 'BUILD' :
    print ("Instance: "+instance_consumer.name+" is in "+inst_status_cons+" state, sleeping for 5 seconds more...")
    time.sleep(5)
    instance_consumer = nova.servers.get(instance_consumer.id)
    inst_status_cons = instance_consumer.status

ip_address_cons = None
for network in instance_consumer.networks[private_net]:
    if re.match('\d+\.\d+\.\d+\.\d+', network):
        ip_address_cons = network
        break
if ip_address_cons is None:
    raise RuntimeError('No IP address assigned!')

print ("Instance: "+ instance_consumer.name +" is in " + inst_status_cons + " state" + " ip address: "+ ip_address_cons)