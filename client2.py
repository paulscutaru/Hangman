import socket
import time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 55500
server.connect((host, port))
print('---Client 2---', end='')

while True:
    print()
    signal = input('Start a new game? Press 0 for no, 1 for yes: ')
    server.send(signal.encode())

    state = server.recv(1024)
    if state.decode() == 'close':
        print('Closing game...')
        server.close()
        break
    else:
        print('-----------Game started!-----------')

    data = server.recv(1024)
    definition = data.decode()

    print('Here is the definition of the word:', definition)

