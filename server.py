# Proiect "Spanzuratoarea"
# Scutaru Paul-Alexandru
# Grupa A7

import socket
import time

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 55500
serversocket.bind((host, port))
serversocket.listen(2)
print('---Server---')
print('Listening for connections...')

# Client 1
clientsocket1, addr1 = serversocket.accept()
print('Connected by client 1 (provider):', addr1)

# Client 2
clientsocket2, addr2 = serversocket.accept()
print('Connected by client 2 (guesser):', addr2)


def shutdownGame():
    clientsocket1.send(str('close').encode())
    clientsocket2.send(str('close').encode())
    clientsocket1.close()
    clientsocket2.close()
    serversocket.close()


def notifyClients():
    clientsocket1.send(str('start').encode())
    clientsocket2.send(str('start').encode())


while True:
    # Waiting for clients to send signal to start
    signal1 = clientsocket1.recv(1024)
    print('Received from client1:', signal1.decode())
    signal2 = clientsocket2.recv(1024)
    print('Received from client2:', signal2.decode())
    if signal1.decode() != '1' or signal2.decode() != '1':
        print("Server is closing...")
        shutdownGame()
        break
    else:
        notifyClients()

    # Get the word choosen by client 1
    data = clientsocket1.recv(1024)
    word = data.decode()
    print('Received word:', word)

    # Get the definition of the word
    data2 = clientsocket1.recv(1024)
    definition = data2.decode()
    print('Received definition:', definition)

    # Send the definition to client 2
    clientsocket2.send(data2)


