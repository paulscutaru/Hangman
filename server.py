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

    # Loop of guesses
    guessed_word = '_' * len(word)
    nr_chances = len(word)
    while True:

        # Get the guess from client 2
        data3 = clientsocket2.recv(1024)
        letter = data3.decode()

        print('Received guess:', letter)

        nr_occurences = word.count(letter)

        # If letter appears once or appears multiple times but wasn't guessed yet
        if nr_occurences == 1 or (nr_occurences > 1 and letter not in guessed_word):

            # If it appears once and was already guessed
            if letter in guessed_word:
                nr_chances -= 1

            index = word.find(letter)
            guessed_word = guessed_word[:index] + letter + guessed_word[index + 1:]

        elif nr_occurences > 1:

            index_aux = guessed_word.rfind(letter)
            index = word.find(letter, index_aux + 1)

            # The case when the letter has already been guessed entirely for all its occurences
            if index == -1:
                nr_chances -= 1
            else:
                guessed_word = guessed_word[:index] + letter + guessed_word[index + 1:]

        elif nr_occurences == 0:
            nr_chances -= 1

        if nr_chances == 0:
            clientsocket1.send(str('The other player did not guess the word').encode())
            clientsocket1.send(word.encode())
            clientsocket2.send(str('You did not guess the word').encode())
            clientsocket2.send(word.encode())
            print('End game (lose)')
            break

        # If all the letters are guessed
        if '_' not in guessed_word:
            clientsocket1.send(str('The other player guessed the word').encode())
            clientsocket1.send(word.encode())
            clientsocket2.send(str('You guessed the word').encode())
            clientsocket2.send(word.encode())
            print('End game (win)')
            break

        # Send result of guess to clients
        clientsocket1.send(guessed_word.encode())
        clientsocket1.send(str(nr_chances).encode())
        clientsocket2.send(guessed_word.encode())
        clientsocket2.send(str(nr_chances).encode())

        print('Sent:', guessed_word, nr_chances)
