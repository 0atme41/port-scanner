import socket
import threading
from queue import Queue

# defined target is localhsot by default
target = "127.0.0.1"

# number of threads used to scan
THREAD_COUNT = 500

queue = Queue()
open_ports = []

# scans a port, returning true if responsive, false if not
def portscan(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target, port))
        return True
    except:
        return False

# populates the queue data structure with the list of ports to be scanned 
def fill_queue(port_list):
    for port in port_list:
        queue.put(port)

# selects the next port in the queue and called the scan method
def worker():
    while not queue.empty():
        port = queue.get()
        if portscan(port):
            print(f"Port {port} is open.")
            open_ports.append(port)

# specifies a list of ports
port_list = range(1, 1024)

fill_queue(port_list)

thread_list = []

# assigns each thread to the worker method and adds it to the thread list
for t in range(THREAD_COUNT):
    thread = threading.Thread(target=worker)
    thread_list.append(thread)

# starts all threads
for thread in thread_list:
    thread.start()

# joins all threads to ensure they all end brefore moving on
for thread in thread_list:
    thread.join()

# prints the list of open ports
print("Open ports are: ", open_ports)