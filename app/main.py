import socket
import threading
import re

NOT_FOUND_MSG = 'HTTP/1.1 404 Not Found\r\n'
OK_MESSAGE = 'HTTP/1.1 200 OK\r\n'

def handle_http_requests(conn : socket.socket, addr):
    while True:
        request_msg : str = conn.recv(1024).decode()
        if request_msg:
            request_parts = request_msg.split(sep='\r\n')
            
            start_line = request_parts[0]
            user_agent = request_parts[2]
            
            method = start_line.split(sep='/')[0]
            
            request_target : str = re.sub(pattern='GET |POST |HEAD |OPTIONS ', repl='', string= start_line)
            request_target = re.sub(pattern=' HTTP/1[.][0-1]', repl='' , string= request_target)
            
            
            target_parts = request_target.split(sep='/')
            while '' in target_parts:
                target_parts.remove('')
                
            if method in ['GET ', 'POST ', 'HEAD ', 'OPTIONS ']: 
                if request_msg != '/':
                    if len(target_parts) == 1:
                        path = target_parts[0]
                        print('path is', path)
                        if path == ' user-agent':
                            ua_content = re.sub(pattern='User-Agent: ', repl='', string=user_agent)
                            conn.send(f"{OK_MESSAGE}\r\nContent-Type: text/plain\r\nContent-Length: {len(ua_content)}\r\n\r\n{ua_content}".encode())
                        elif path not in []: # [] an empty db for now
                            conn.send(f'{NOT_FOUND_MSG}\r\n'.encode())
                        else:
                            pass     
                    elif target_parts[0] == 'echo':
                        echo_content = target_parts[1]
                        conn.send(f'{OK_MESSAGE}Content-Type: text/plain\r\nContent-Length: {len(echo_content)}\r\n\r\n{echo_content}'.encode())
                else:
                    conn.send(f'{OK_MESSAGE}\r\n'.encode())  
            
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
