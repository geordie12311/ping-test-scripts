"""This script is designed to identify the loopback address on each host in the host file
create a target list using that data and get each host to then ping each loopback IP addres"""
import getpass
import time
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
from rich import print as rprint

rprint("[bold red on yellow]******************THIS SCRIPT WILL PING THE LOOPBACK ADDRESSES ON ALL HOSTS FROM ALL HOSTS****************[/bold red on yellow]")
time.sleep(2)

nr = InitNornir(config_file="config.yaml")
user = input("Please enter your username: ")
password = getpass.getpass()
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password

with open("iplist.txt", "r") as f:
    filelines = f.read().splitlines()

target_list = []
failed_ping = []

def getip(task):
    result = task.run(task=send_command, command="show ip int brief")
    task.host["facts"] = result.scrapli_response.genie_parse_output()
    interfaces = task.host["facts"]["interface"]
    for intf in interfaces:
        if intf.startswith("Loop"):
            ip_addr = interfaces[intf]["ip_address"]
            if ip_addr != "unassigned":
                target_list.append(ip_addr)

def pingtest(task):
    for ip_address in sorted_list:
        result = task.run(task=send_command, command="ping " + ip_address)
        response = result.result
        if not "!!!" in response:
            failed_ping.append(f"{task.host} can't ping {ip_address}")


nr.run(task=getip)
sorted_list = sorted(target_list)
nr.run(task=pingtest)
if failed_ping:
    sorted_failed = sorted(failed_ping)
    rprint(sorted_failed)
else:
    rprint("[green]All ping tests were successful[/green]")


