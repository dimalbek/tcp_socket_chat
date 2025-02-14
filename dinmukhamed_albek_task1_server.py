import socket as tcp_sock

def tcp_server():
    # Creation of a TCP / IP socket 
    server_sock = tcp_sock.socket(tcp_sock.AF_INET, tcp_sock.SOCK_STREAM)
    
    # Define socket port and adress
    PORT = 10502
    server_adrs = ('localhost', PORT)
    print(f"Starting server on {server_adrs}")
    
    # Bind socket to port and adress
    server_sock.bind(server_adrs)
    
    # Listen for incoming connection, max of 1
    server_sock.listen(1)
    print("Server listens for incoming connection..\n")
    
    while True:
        # Accept connection from client
        connection, client_address = server_sock.accept()
        try:
            print(f"Connection established with {client_address}")
            
            while True:
                # Receive data, max of 1024 bytes
                data = connection.recv(1024)
                if data:
                    # Decode received message from bytes to string
                    message = data.decode()
                    print(f"Received message from client: {message}")
                    
                    # Response message
                    response = "Greetings from server! Your message received!"
                    # Send response to client
                    connection.sendall(response.encode())
                    print("Response sent to client.\n")
                else:
                    print("No data received\n")
                    break
        
        except Exception as e:
            print(f"Error: {e}")
        
        finally:
            # Close connection
            connection.close()
            print("Connection closed. Server shutting down.")

if __name__ == "__main__":
    tcp_server()

