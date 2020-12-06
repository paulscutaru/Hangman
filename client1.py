import socket
import time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 55500
server.connect((host, port))
print('---Client 1---', end='')

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

    word = input('Enter word to be sent to server: ')
    server.send(word.encode())

    definition = input('Enter a short definition of the word: ')
    server.send(definition.encode())

    while True:
        data1 = server.recv(1024)
        print(data1.decode(), end=' ')

        data2 = server.recv(1024)
        print(data2.decode())

        if data1.decode() == 'The other player guessed the word' or data1.decode() == 'The other player did not guess the word':
            break
