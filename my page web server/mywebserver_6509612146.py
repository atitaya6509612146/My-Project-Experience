import socket
import os

port = 5146

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('0.0.0.0', port))

server_socket.listen(5)
print(f"Server is listening on port {port}...")

while True:
  
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr} has been established.")

    request = client_socket.recv(1024).decode('utf-8')
    print(f"Received request:\n{request}")

    if "GET /mypage.htm" in request:
        with open("mypage.htm", "r", encoding="utf-8") as file:
            response_body = file.read()
        
        response = "HTTP/1.1 200 OK\r\n"
        response += "Content-Type: text/html; charset=utf-8\r\n"
        response += f"Content-Length: {len(response_body.encode('utf-8'))}\r\n"
        response += "\r\n"
        response += response_body

        response = response.encode('utf-8') 

    elif "GET /myimage.gif" in request:
        if os.path.exists("myimage.gif"):
            with open("myimage.gif", "rb") as img_file:
                img_data = img_file.read()
            response = "HTTP/1.1 200 OK\r\n"
            response += "Content-Type: image/gif\r\n"
            response += f"Content-Length: {len(img_data)}\r\n"
            response += "\r\n"
            response = response.encode('utf-8') + img_data  
        else:
            response = "HTTP/1.1 404 Not Found\r\n\r\n<h1>404 Not Found</h1>"
            response = response.encode('utf-8') 

    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\n<h1>404 Not Found</h1>"
        response = response.encode('utf-8')  

    client_socket.sendall(response)

    print(f"Connection from {addr} has been closed.")

    client_socket.close()
