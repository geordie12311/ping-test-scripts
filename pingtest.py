"""This script will send ping commands to all devices in the host file
and ping each ip address in a static list and print any failed pings 
to the screen"""
import getpass
import time
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
from rich import print as rprint

rprint("[bold red on yellow]********************THIS SCRIPT WILL PING THE IP ADDRESSES IN IPLIST.TXT FROM ALL HOSTS******************[/bold red on yellow]")
time.sleep(2)

nr = InitNornir(config_file="config.yaml")
password = getpass.getpass()
nr.inventory.defaults.password = password

with open("iplist.txt", "r") as f:
    filelines = f.read().splitlines()

failed_ping = []
    
def pingtest(task):
    for target in filelines:
        result = task.run(task=send_command, command="ping " + target)
        response = result.result
        if not "!!!" in response:
            failed_ping.append(f"{task.host} can't ping {target}")

results = nr.run(task=pingtest)
if failed_ping:
    sorted_list = sorted(failed_ping)
    rprint(sorted_list)
else: 
    rprint("All ping tests were successful")
