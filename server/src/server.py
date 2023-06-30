import socket
import http.server
import socketserver
import threading
import sys
import time
import urllib.request

WEB_PORT = 8000
SOCKET_PORT = 3031

running = True
server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
local_ip = str(server.getsockname()[0])
IP_PORT = (local_ip, SOCKET_PORT)
server.bind(IP_PORT)
server.listen()
print("Socket server running port " + str(IP_PORT[1]))

def socketServer():
    while running:
        conn, addr = server.accept()
        conn.send(f"Connection successful {addr[0]}".encode())
        data = conn.recv(1024)
        if data.decode()[0] == "1":
            fileName = f"{data.decode()[1:len(data.decode())]}"
            conn.send(f"http://{urllib.request.urlopen('https://ident.me').read().decode('utf8')}:{WEB_PORT}/{fileName}".encode())
            copie = open(f"{data.decode()[1:len(data.decode())]}", "wb") 
            data = conn.recv(1024)
            while data:
                copie.write(data)
                data = conn.recv(1024)
                print("receiving ")
            copie.close()
            history = open("history.txt","a")
            currentTime = time.strftime("%H:%M:%S", time.localtime())
            history.write(f"\n[{addr[0]} {currentTime}]: http://{urllib.request.urlopen('https://ident.me').read().decode('utf8')}:{WEB_PORT}/{fileName}")
            history.close()

def main():
    threading.Thread(target=socketServer).start()
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", WEB_PORT), Handler) as httpd:
        print("Web server running port", WEB_PORT)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()
        server.close()

main()