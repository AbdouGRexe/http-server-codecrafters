import socket


def main():
    with socket.create_server(("localhost", 4221)) as server_socket:
        client_request = server_socket.accept() # wait for client
        conn, addr = client_request
        conn.send('HTTP/1.1 200 OK\r\n\r\n'.encode())
    
    


if __name__ == "__main__":
    main()
