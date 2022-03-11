import ipaddress
import getpass
import time
import itertools
from subprocess import Popen, DEVNULL
from rich import print as rprint
from rich.console import Console
from rich.table import Table
"""Popen class is a child process that can be used to check the child process has finished"""

ping = {}
active_list = []
inactive_list = []

localtime = time.asctime(time.localtime(time.time()))
rprint("[bold green] Welcome to Subnet_Pinger![/bold green]")
rprint("[cyan]Please enter the network you want to test: ")
rprint("Example: <192.168.1.0/24>")

subnet = input("Enter the network: ")
network = ipaddress.ip_network(subnet)

hosts = network.hosts()
for n in hosts:
    IP = str(n)
    ping[IP] = Popen(["ping", "-c", "4", "-i", "0.2", IP], stdout=DEVNULL)
    
while ping:
    for IP, process in ping.items():
        if process.poll() is not None:
            del ping[IP]
            if process.returncode == 0:
                active_list.append(IP)
            elif process.returncode == 1:
                inactive_list.append(IP)
            else: 
                print(f"{IP} ERROR")
            break

table = Table(title="Ping Report \n" + localtime)
table.add_column("Active Hosts", justify="centre", style="green")
table.add_column("Inactive Hosts", justify="centre", style="red")
for (a, i) in itertools.zip_longest(active_list, inactive_list):
    table.add_row(a, i)
console = Console()
console.print(table)
