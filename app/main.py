import socket
import threading
import re

FORMAT = 'utf-8'

    
def main():
    with socket.create_server(("localhost", 4221)) as server_socket:
        while True:
            client_request = server_socket.accept() # wait for client
            conn, addr = client_request

            # each machine has its HTTP request handled by a thread
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()    

if __name__ == "__main__":
    main()  



def handle_client(conn : socket.socket, addr):
    request_msg : str = conn.recv(1024).decode(FORMAT)
    if request_msg:
        
        parsed_request = parse_req(request_msg)
        response: dict = get_response(parsed_request)
        
        status: int = response['status_code']
        content = response['response_body']
        context : tuple[int, str] = (len(content), response['content-type'])
        
        match status:
            case 501:
                message = "HTTP/1.1 501 Not Implemented\r\n\r\n"
            case 404:
                message = "HTTP/1.1 404 Not Found\r\n\r\n"
            case 400:
                message = "HTTP/1.1 400 Bad Request\r\n\r\n"
            case 201:
                message = "HTTP/1.1 201 Created\r\n\r\n"
            case 200:
                if not content:
                    message = "HTTP/1.1 200 OK\r\n\r\n"
                else:
                    message = f"HTTP/1.1 200 OK\r\nContent-Type: {context[1]}\r\nContent-Length: {context[0]}\r\n\r\n{content}"            
        try:
            conn.send(message.encode(FORMAT))
        except:
            print("Something went wrong when a response was being sent, might be a connection error")        
        

def get_response(req : dict) -> dict[str, str, str]:
    
    res_GET = {
        'status-code': 404,
        'content-type': "",
        'response-body': None,
    }
    
    if not req:
        res_GET['status-code'] = 400 # Bad request
        return res_GET
    
    if req['method'] not in ['GET', 'POST', 'PUT' , 'HEAD', 'OPTIONS']:
        res_GET['status-code'] = 501 # unsupported method 
        return res_GET

    headers = [str(key) for key in dict['headers'].keys()] 
    url_paths = ['/']
    if req['method'] == 'GET':
        
        if str(req['target']) in url_paths:
            res_GET['status-code'] = 200
        
        if str(req['target']).lower() in headers:
            res_GET['status-code'] = 200
            res_GET['response-body'] = req['headers'][req['target'].lower()]
            res_GET['content-type'] = 'text/plain'
        
        if str(req['target']).startswith('/echo'):
            res_GET['status-code'] = 200
            res_GET['response-body'] = req['target'].split('/')[2]
            res_GET['content-type'] = 'text/plain'
            
        
        if str(req['target']).startswith('/files'):
            res_GET['status-code'] = 200
            res_GET['content-type'] = 'application/octet-stream'
        
        return res_GET     
        

# Breaks down http request and verifies syntax
def parse_req(msg : str)-> dict[str, str, str, str]:
    output_dict = {
        'method': "",
        'target': "",
        'headers': {},
        'body': ""
    }
    req_parts = msg.split('\r\n')
    
    # The simplest case of a req is GET(method) / HTTP/1.1\r\n\r\n meaning at least GET / HTTP/1.1|""|""
    if len(req_parts) < 3:
        return
    
    output_dict['method'] = req_parts[0].split(' ')[0]
    output_dict['target'] = req_parts[0].split(' ')[1]
    
    count = 0
    
    for header in req_parts[1:]:        
        if header == '' and count != 0: # if no header is present
                                        # an additional blank line is found so we skip it.
            output_dict["body"] = req_parts[count + 1]
            return output_dict            
        if len(req_parts) > 3: # 4 is the minimum size for a header-filled request
            output_dict['headers'][header.split(': ')[0].lower()] = header.split(': ')[1]
        count += 1
    

                  
    
         

