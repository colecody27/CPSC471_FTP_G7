# Server code
from socket import ∗

 # The port on which to listen
 serverPort = 12000

 # Create a TCP's socket
 serverSocket = socket( AF INET, SOCK STREAM)

 # Bind the socket to the port
 serverSocket.bind((’’, serverPort))

 # Start listening for incoming connections
 serverSocket.listen(1) 
 print ”The server is ready to receive ” 

 # Forever accept incoming connections
 while 1 :
 # Accept a connection ; get client ’ socket
 connectionSocket, addr = serverSocket.accept()

 # The temporary buffer
 tmpBuff= ”” 

 while len(data) != 40 :
 # Receive whatever the newly connected client has to send
tmpBuff = connectionSocket.recv(40)

 # The other side unexpectedly closed it’s socket
if not tmpBuff :
break

# Save the data
data += tmpBuff
print data 

# Close the socket
connectionSocket.close()