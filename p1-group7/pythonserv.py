# Server code
import socket
import os.path

# ************************************************
# Downloads file from client
# ************************************************
def get():
    # Create data channel 
    dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to port 0
    dataSocket.bind(('',59116))

    # Receive data channel connection from client
    dataSocket.listen(1) 
    connectionSocket, addr = dataSocket.accept()

    # Receive filename from client
    filename = connectionSocket.recv(40).decode()

    # Validate filename
    dirContents = os.listdir()

    i = 0
    if(filename in dirContents):
        while filename in dirContents:
            i += 1
            filename = str(i) + filename 

    # Open file in append mode
    file = open(filename, "a")

    # Print this is the right function
    print("Receiving file from client...")
    # Get the data from the client and decode it
    while True:
        # Receive data
        data = connectionSocket.recv(40).decode()

        # If there is no data then close file 
        if not data:
            file.close()
            break
        else:
            file.write(data)

    # Success output
    print("SUCCESS")
    print(filename + " has been downloaded successfully")
    print("Number of bytes downloaded: " + str(os.stat(filename).st_size) + "\n")

    # Close data channel 
    file.close()
    connectionSocket.close()

# ************************************************
# Uploads file to client
# @param filename - Name of file to be uploaded to client
# ************************************************
def put():
    # Create data channel 
    dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to port 
    dataSocket.bind(('',59116))

    # Receive data channel connection from client
    dataSocket.listen(1) 
    connectionSocket, addr = dataSocket.accept()
    
    # Receive filename from client
    filename = connectionSocket.recv(40).decode()

    # Verify file is in directory
    dirContents = os.listdir()
    if(filename not in dirContents):
        connectionSocket.close()
        
        
    # Upload file to server 
    print("Uploading file to client...")
    file = open(filename, "r")
    try:
        connectionSocket.sendall(file.read().encode())
    except IOError:
        print("Unable to upload contents to client")
        file.close()
        connectionSocket.close()

    # Success output
    print("SUCCESS")
    print(filename + " has been uploaded successfully")
    print("Number of bytes uploaded: " + str(os.stat(filename).st_size) + "\n")

    file.close()
    connectionSocket.close()

# ************************************************
# List files found on server
# ************************************************
def list():
    # Create data channel 
    dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to port 0
    dataSocket.bind(('',59116))

    # Receive data channel connection from client
    dataSocket.listen(1)
    connectionSocket, addr = dataSocket.accept()

    #Get list of files in directory 
    dirContents = os.listdir()
    dirList = ""
    for filename in dirContents:
        dirList = dirList + filename + "\n"

    print("Sending directory contents to client...")
    try:
        connectionSocket.sendall(dirList.encode())
    except IOError:
        print("Error sending directory contents to client")
        connectionSocket.close()

    # Success output
    print("SUCCESS")
    print("Directory contents been uploaded successfully\n")

    # Close connection
    dataSocket.close()
    connectionSocket.close()

 # The port on which to listen
serverPort = 12000

 # Create a TCP's socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

 # Bind the socket to the port
serverSocket.bind(('', serverPort))

 # Start listening for incoming connections
serverSocket.listen(1) 
print ("The server is ready")

# Accept a connection ; get client's socket
connectionSocket, addr = serverSocket.accept()
print("Connection established")
while True :
    # Receive command from user
    try:
        command = connectionSocket.recv(40).decode()
    except IOError:
        print("Command has not been received properly. Connection has been closed. ")
        serverSocket.close()
        connectionSocket.close()
        break
    
    match command:
        case "get":
            put()
        case "put":
            get()
        case "ls":
            list()
        case "quit":
            serverSocket.close()
            connectionSocket.close()
            break 