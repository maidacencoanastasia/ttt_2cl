import socket

# define host and port
HOST = ''
PORT = 5555

# create socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind socket object to host and port
server_socket.bind((HOST, PORT))

# listen for incoming connections
server_socket.listen()

print(f"Server is listening on {HOST}:{PORT}")

# define the game board
board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]


# function to print the game board
def print_board():
    print(f"{board[0]}|{board[1]}|{board[2]}")
    print("-+-+-")
    print(f"{board[3]}|{board[4]}|{board[5]}")
    print("-+-+-")
    print(f"{board[6]}|{board[7]}|{board[8]}")


# function to check if the game has ended
def game_ended():
    for i in range(0, 9, 3):
        if board[i] == board[i + 1] == board[i + 2] and board[i] != " ":
            return True
    for i in range(0, 3):
        if board[i] == board[i + 3] == board[i + 6] and board[i] != " ":
            return True
    if board[0] == board[4] == board[8] and board[0] != " ":
        return True
    if board[2] == board[4] == board[6] and board[2] != " ":
        return True
    if " " not in board:
        return True
    return False


# function to play the game
def play_game(conn1, conn2):

    # send initial board state to clients
    conn1.send("START".encode())
    conn1.send(str.encode(str(board)))
    conn2.send("START".encode())
    #board = ''.join(board)
    conn2.send(str.encode(str(board)))

    # alternate turns between players
    current_player = conn1
    while not game_ended():
        other_player = conn1 if current_player == conn2 else conn2
        current_player.send("YOUR_TURN".encode())
        other_player.send("OTHER_TURN".encode())

        # receive move from current player
        move = current_player.recv(1024).decode()
        move = int(move)

        # update board state
        board[move] = "X" if current_player == conn1 else "O"

        # send updated board state to both clients
        conn1.send(str.encode(str(board)))
        conn2.send(str.encode(str(board)))

        # switch to other player's turn
        current_player, other_player = other_player, current_player

    # send game ended message to both clients
    conn1.send("GAME_ENDED".encode())
    conn2.send("GAME_ENDED".encode())

    # determine winner or tie
    if " " not in board:
        winner = "TIE"
    else:
        winner = "PLAYER1" if current_player == conn2 else "PLAYER2"

    # send winner message to both clients
    conn1.send(str.encode(winner))
    conn2.send(str.encode(winner))

    # close connections
    conn1.close()
    conn2.close()


# accept connections from clients
conn1, addr1 = server_socket.accept()
print(f"Player 1 connected from {addr1}")
conn2, addr2 = server_socket.accept()
print(f"Player 2 connected from {addr2}")
play_game(conn1, conn2)
