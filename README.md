# TCP Chat Application

# **Project Overview**
This project implements a simple TCP-based chat application with user authentication. It consists of two tasks:

Task 1: Basic client-server interaction where the server responds to client messages.

Task 2: Multi-threaded chat server with user authentication, logging, and message broadcasting.

## **Technology Stack**

Python: Core language for implementation.

Socket: Handles TCP communication.

Threading: Enables concurrent client connections.

SQLAlchemy: Manages SQLite database for user authentication.

Passlib: Securely hashes and verifies passwords.

Logging: Logs chat messages and user activity.

## **User Credentials**
The application's default users:

Username | Password
dima | please
zak | give
nur | me
nusupoff | full
ansar | points

## **Installation and setup**

Unpack zip file and go inside

**Set Up a Virtual Environment (Recommended)**:
```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate
```

**Install Dependencies**:
```bash
    pip install -r requirements.txt
```

**Running the Application**

***Task 1: Basic Client-Server Communication***

Start the Server:
```bash
    python3 dinmukhamed_albek_task1_server.py
```

Start the Client:
```bash
    python3 dinmukhamed_albek_task1_client.py
```
Enter a message after prompt.
The server will respond with a greeting.

***Task 2: Multi-threaded Chat Server with Authentication***

Start the Server:
```bash
    python3 dinmukhamed_albek_task2_server.py
```
This initializes the SQLite database and starts the chat server.

Start the Client:
```bash
    python3 dinmukhamed_albek_task2_client.py
```
Enter a username and password from the predefined list.

If authentication is successful, the client joins the chat.
Type messages to send them to all connected users.
Type exit to leave the chat.

## Logs

Chat messages and user connections are logged in chat_logs.log.

## Database

The SQLite database (sql_app.db) stores user credentials securely.

## Author
Developed by Dinmukhamed Albek.