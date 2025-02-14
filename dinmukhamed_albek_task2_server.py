import socket as tcp_sock
import threading
import datetime
import logging as logs
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext


# logs PART

# Configuration of logs file
logs.basicConfig(
    filename="chat_logs.log",
    level=logs.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# HASHING PART

# Password hashing using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# verifying of password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# DB PART

# DB settings
Base = declarative_base()
DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# User model for login
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hashed = Column(String, nullable=False)

# Creation of users table
Base.metadata.create_all(bind=engine)


# get user from db by username
def get_user_by_username(username: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        return user
    finally:
        db.close()

# Creation of default users and populating db with
def populate_db():
    db = SessionLocal()
    # if db is not already pupulated, populate db
    if db.query(User).first() is None: 
        hashed_password1 = pwd_context.hash("please")
        hashed_password2 = pwd_context.hash("give")
        hashed_password3 = pwd_context.hash("me")
        hashed_password4 = pwd_context.hash("full")
        hashed_password5 = pwd_context.hash("points")
        
        user1 = User(username="dima", password_hashed=hashed_password1)
        user2 = User(username="zak", password_hashed=hashed_password2)
        user3 = User(username="nur", password_hashed=hashed_password3)
        user4 = User(username="nusupoff", password_hashed=hashed_password4)
        user5 = User(username="ansar", password_hashed=hashed_password5)
        
        db.add(user1)
        db.add(user2)
        db.add(user3)
        db.add(user4)
        db.add(user5)
        
        db.commit()
    
    db.close()


# GLOBAL VARIABLES
clients = {}  # Dict {client_sock: username}
locker = threading.Lock()  # ensures only one thread can access clients at the same time to avoid runtime errors


# SOCKETS AND CHAT PART

# send message to all connected clients
def send_msg(msg, sender_socket=None):
    with locker:
        for client, _ in clients.items():
            if client != sender_socket: # no need to send a message to sender himself
                try:
                    client.sendall(msg.encode())
                except Exception as e:
                    print(f"Error when senging message: {e}")


def handle_client(client_sock, client_adrs):
    print(f"Connection established with {client_adrs}")
    try:
        data = client_sock.recv(1024)
        if not data:
            client_sock.close()
            return
        login_msg = data.decode().strip() # username and password, removing leading and trailing spaces
        
        try:
            username, password = login_msg.split(" ")
        except ValueError:
            client_sock.sendall("Invalid login format. Disconnecting..\n".encode())
            client_sock.close()
            return

        # Validate username and password
        user = get_user_by_username(username)
        if not user: # user is not registered
            client_sock.sendall("User not found (404). Disconnecting..\n".encode())
            client_sock.close()
            return
        elif not verify_password(password, user.password_hashed): # wrong password
            client_sock.sendall("Incorrect password (401). Disconnecting..\n".encode())
            client_sock.close()
            return

        # Authorization message
        client_sock.sendall(
            "Authorized (200). Welcome!\n".encode()
        )
        
        with locker:
            clients[client_sock] = username # inserting user into clients dictionary
        
        send_msg(f"[{username}] joined to chat\n", client_sock)
        # logging to chat_logs file
        logs.info(f"[{username}] connected through port {client_adrs}") 

        # loop for receiving and sending messages
        while True:
            try:
                data = client_sock.recv(1024)
                if not data:
                    break
                
                msg = data.decode().strip() # getting message and removing leading and trailing spaces
                if msg.lower() == "exit": # disconnecting from chat by user prompt
                    # client_sock.close()
                    client_sock.sendall("Disconnecting..\n".encode())
                    break
                
                print(f"[{username}]: {msg}")
                logs.info(f"[{username}]: {msg}")
                send_msg(f"[{username}]: {msg}", client_sock)
            
            except Exception as e:
                print(f"Error while receiving message from {client_adrs}: {e}")
                break
    
    except Exception as e:
        print(f"Error with {client_adrs}: {e}")
    
    finally:
        # Remove user from clients dict & notify
        with locker:
            if client_sock in clients.keys():
                removed_user = clients[client_sock]
                send_msg(f"User [{removed_user}] left chat.\n", client_sock)
                logs.info(f"User [{removed_user}] disconnected.")
                del clients[client_sock]
        
        client_sock.close()
        print(f"Connection with {client_adrs} closed")


def tcp_server():
    server_sock = tcp_sock.socket(tcp_sock.AF_INET, tcp_sock.SOCK_STREAM)
    PORT = 10503
    server_adrs = ("localhost", PORT)
    server_sock.bind(server_adrs)
    server_sock.listen(5) # max of 5 users
    print(f"Server started on {server_adrs}. Waiting for connections..")

    try:
        while True:
            client_sock, client_adrs = server_sock.accept()
            client_thread = threading.Thread(
                target=handle_client, args=(client_sock, client_adrs)
            )
            client_thread.start()
            print(f"Active connections: {threading.active_count() - 1}")
    
    except KeyboardInterrupt:
        print("Server shutting down..")
    
    finally:
        server_sock.close()


if __name__ == "__main__":
    populate_db()
    tcp_server()
