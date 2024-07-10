import socket
import threading

def handle_http_requests(conn, addr):
    while True:
        request_msg = str(conn.recv(1024).decode())
        request_parts = request_msg.split(sep='\r\n')
        
        start_line = request_parts[0]
        start_line = start_line.split(sep='/')
        
        if start_line[0] in ['GET', 'POST', 'HEAD', 'OPTIONS']:
            path = start_line[1].split(sep=' ')[0]
            if path != '':
                conn.send('HTTP/1.1 404 Not Found\r\n\r\n')
            else:
                conn.send('HTTP/1.1 200 OK\r\n\r\n')  
            
def main():
    with socket.create_server(("localhost", 4221)) as server_socket:
        while True:
            client_request = server_socket.accept() # wait for client
            conn, addr = client_request
            
            # each machine has its HTTP requests handled by a thread
            thread = threading.Thread(target=handle_http_requests, args=(conn, addr))
            thread.start()    
    


if __name__ == "__main__":
    main()
