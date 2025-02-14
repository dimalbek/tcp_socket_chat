import socket as tcp_sock

def tcp_client():
    # Creation of a TCP / IP socket 
    client_sock = tcp_sock.socket(tcp_sock.AF_INET, tcp_sock.SOCK_STREAM)
    
    # Define socket port and adress
    PORT = 10502
    server_adrs = ('localhost', PORT)
    print(f"Connecting to server at adress: {server_adrs}")
    
    client_sock.connect(server_adrs)
    # Connection of socket to the server's address
    
    try:
        # Prompt user for input
        message = input("Enter a message: ")
        # Send message to server and encode string to bytes
        client_sock.sendall(message.encode())
        print(f"Sent: {message}")
        
        # Wait until receive message from server, message <= 1024 bytes
        response = client_sock.recv(1024)
        print(f"Received response from server: {response.decode()}")
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # Close socket connection
        client_sock.close()
        print("Client connection closed.")

if __name__ == "__main__":
    tcp_client()
