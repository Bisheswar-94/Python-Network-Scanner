import socket
import ipaddress
import threading
import subprocess
import platform
from queue import Queue
from colorama import Fore, init

init(autoreset=True)

print(Fore.CYAN + r"""
 _   _      _                      _    
| \ | | ___| |___      _____  _ __| | __
|  \| |/ _ \ __\ \ /\ / / _ \| '__| |/ /
| |\  |  __/ |_ \ V  V / (_) | |  |   < 
|_| \_|\___|\__| \_/\_/ \___/|_|  |_|\_\

      Python Network Scanner
""")

network = input("Enter Network Range: ").strip()

try:
    ip_net = ipaddress.ip_network(network, strict=False)
except ValueError:
    print(Fore.RED + "Invalid Network Range")
    exit()

queue = Queue()
print_lock = threading.Lock()

system = platform.system().lower()

def ping_host(ip):
    if system == "windows":
        command = ["ping", "-n", "1", "-w", "100", str(ip)]
    else:
        command = ["ping", "-c", "1", "-W", "1", str(ip)]

    result = subprocess.run(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    if result.returncode == 0:
        try:
            hostname = socket.gethostbyaddr(str(ip))[0]
        except:
            hostname = "Unknown"

        with print_lock:
            print(Fore.GREEN + f"[+] Active Host: {ip} | Hostname: {hostname}")

def worker():
    while not queue.empty():
        ip = queue.get()
        ping_host(ip)
        queue.task_done()

for ip in ip_net.hosts():
    queue.put(ip)

thread_count = 100

for _ in range(thread_count):
    thread = threading.Thread(target=worker)
    thread.daemon = True
    thread.start()

queue.join()

print(Fore.CYAN + "\nScan Completed.")