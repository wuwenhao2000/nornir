from nornir import InitNornir
from nornir.plugins.tasks import networking,text,commands
from nornir.plugins.tasks.networking import netmiko_send_command,napalm_get
from nornir.plugins.functions.text import print_result
import json

def adapt_host_data(host):
    with open("pass.json", "r") as f:
       data = json.load(f)
       host.username = data["username"]
       host.password = data["password"]

nr = InitNornir(
    core={"num_workers": 100},
    inventory={
        "plugin": "nornir.plugins.inventory.simple.SimpleInventory",
        "transform_function": adapt_host_data,
        "options": {
            "host_file": "inventory/hosts.yaml",
            "group_file": "inventory/groups.yaml",
            "defaults_file": "inventory/defaults.yaml"}})


nr = nr.filter(platform="cisco_ios")
show_list = ["sh version","sh ip arp"] 

# # nr = nr.filter(platform="arista_eos")
# # show_list = ["sh version","sh ip arp"] 

# # nr = nr.filter(platform="juniper_junos")
# # show_list = ["sh version","sh chassis hardware"] 

# nr = nr.filter(platform="juniper_screenos")
# show_list = ["get config | in snmp","get config | in interface"] 

for each in show_list:
    result = nr.run(
        task=netmiko_send_command,
        command_string=each
        # task=netmiko_send_config_set
    )
    print_result(result)