import os
import getpass
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from rich import print
from rich.console import Console
from rich.table import Table

nr = InitNornir(config_file='config.yaml')

password = getpass.getpass()
nr.inventory.defaults.password = password
#above section is initialising nornir and using getpass to prompt the user to enter 
#their username and password. It will use the credentials to login to each host

with open('iplist.txt', 'r') as f:
    filelines = f.read().splitlines()
with open('iplist.txt', 'r') as f:
    COUNT = 0
    for line in f:
        COUNT += 1
#reading lines from iplist and doing a count
CLEAR = "clear"
os.system(CLEAR)
print("[yellow]*[/yellow]" * 5 + "[yellow]INITIALISING FULL NETWORK PING TEST[/yellow]" + "[yellow]*[/yellow]" * 25)
print("Nornir is conducting a full ping test against all targeted addresses...")
print("< [magenta]If there are no alerts: all devices are fully reachable[/magenta] >")
print("\n")
print("[cyan][u]SCOPE SUMMARY:[/u][/cyan]")
print("\n")
table1 = Table(title="Enumerating")
table2 = Table(title="Enumerating")
table1.add_column("DEVICE INVENTORY", justify="center", style="cyan")
table2.add_column("TARGETS", justify="center", style="green")
for host in nr.inventory.hosts:
    device = host
    STRING_HOST = str(device)
    ipaddr = nr.inventory.hosts[device].hostname
    STRING_IP = str(ipaddr)
    table1.add_row(STRING_HOST + " (" + STRING_IP + ")")
#printing out to screen to tell user what the script is doing and creating tables to 
#show the devices in host list and the target IP addresses. A

for targets in filelines:
    table2.add_row(targets)
#abdding the target IP addresses into table 2
console = Console()
console.print(table1, table2)
device_num = len(nr.inventory.hosts)
per_num = device_num * COUNT
print("\n")
print(f"[u]Total number of devices in inventory[/u]: [green]{device_num}[/green]")
print(f"[u]Total number of IP addresses in target list[/u]: [green]{COUNT}[/green]")
print(f"[u]Total number of ping tests[/u]: [green]{per_num}[/green]")
print("\n")
for target in filelines:
    results = nr.run(send_command, command="ping " + target)
    for dev in results:
        response = results[dev].result
        if not "!!!" in response:
            print(f"[red]ALERT[/red]: {dev} cannot ping [blue]{target}[/blue]")
print("\n")
print("*" * 5 + "[green] TESTS COMPLETE [/green]" + "*" * 46)
#printing out the results and if there is failed pings outputing to the screen
#to show which device failed to reach which IP address