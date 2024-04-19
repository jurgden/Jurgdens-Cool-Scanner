import sys
import socket
import pyfiglet
import threading
from queue import Queue
import time 

# Constants
IP = input("Please enter your IP address: ")
PORTS = range(1, 65500)
THREAD_LIMIT = 100  # Adjust this based on your system and network capacity

# Thread-safe queue to manage open ports
open_ports = Queue()

# Print banner
ascii_banner = pyfiglet.figlet_format("Jurgdens \nc00l Python \nPort Scanner")
print(ascii_banner)

def probe_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((ip, port))
        if result == 0:
            open_ports.put(port)
        sock.close()
    except Exception:
        pass

def threader():
    while True:
        # Get the port number from the queue
        port = port_queue.get()
        # Scan the port
        probe_port(IP, port)
        # Signal to the queue that the task is done
        port_queue.task_done()



start_time = time.time()

# Create the queue and spawn a pool of threads
port_queue = Queue()
for _ in range(THREAD_LIMIT):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()



# Place ports into the queue
for port in PORTS:
    port_queue.put(port)
    print(f"Scanning port number: {port}")

# Wait for the queue to be empty
port_queue.join()

# Gather and print results
results = []
while not open_ports.empty():
    results.append(open_ports.get())

if results:
    print("Open Ports are:")
    print(sorted(results))
else:
    print("Looks like no ports are open :(")

print(f"Total scanning time: {total_time:.2f} seconds")