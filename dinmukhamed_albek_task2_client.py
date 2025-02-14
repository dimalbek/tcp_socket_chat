import socket as tcp_sock
import threading


# function for receving messages
def receive_msgs(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("Server closed connection\n")
                break
            print(data.decode())
        except Exception as e:
            print(f"Error when receiving messages: {e}")
            break


def tcp_client():
    PORT = 10503
    server_adrs = ("localhost", PORT)
    sock = tcp_sock.socket(tcp_sock.AF_INET, tcp_sock.SOCK_STREAM)

    try:
        sock.connect(server_adrs)
    
    except tcp_sock.error as e:
        print(f"Connect to server is failed: {e}")
        return


    # Starting a separate thread to listen the server and incoming messages.
    recv_thread = threading.Thread(target=receive_msgs, args=(sock,))
    recv_thread.daemon = True
    recv_thread.start()

    # prompt for login
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    login_message = f"{username} {password}"
    sock.sendall(login_message.encode())

    #  loop for sending messages to chat
    try:
        while True:
            message = input("You may type 'exit' to leave the chat\n")
            if message.lower() == "exit":
                break
            elif not message:
                print("Message cannot be empty\n")
            else:
                sock.sendall(message.encode())
    
    except KeyboardInterrupt:
        sock.sendall("exit".encode())
    
    except Exception as e:
        print(f"Error when sending message: {e}")
    
    finally:
        sock.close()


if __name__ == "__main__":
    tcp_client()
