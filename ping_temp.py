import getpass
import time
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
from rich import print as rprint

nr = InitNornir(config_file="config.yaml")
password = getpass.getpass()
nr.inventory.defaults.password = password

with open("iplist.txt", "r") as f:
    filelines = f.read().splitlines()

failed_ping = []

def getip(task):
    result = task.run(task=send_command, command="show ip route bgp")
    task.host["facts"] = result.scrapli_response.genie_parse_output()

["facts"]["vrf"]["default"]["address_family"]["ipv4"]["routes"]["51.51.5.0/24"]["next_hop"]["next_hop_list"][1]["updated"]
nr.run(task=getip)

import ipdb
ipdb.set_trace()
