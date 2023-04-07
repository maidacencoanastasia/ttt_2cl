import socket
import sys

# define server address and port
SERVER_ADDRESS = 'localhost'
SERVER_PORT = 5555

# create socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to server
try:
    client_socket.connect((SERVER_ADDRESS, SERVER_PORT))
except:
    print("Unable to connect to server.")
    sys.exit()

# receive initial board state from server
start_msg = client_socket.recv(1024).decode()
if start_msg != "START":
    print("Unexpected message received from server.")
    sys.exit()
board_str = client_socket.recv(1024).decode()
board_str = board_str[:45]
board_str = board_str[:45]
board = eval(board_str)
turn = board_str[45:]

#turn = client_socket.recv(1024).decode()
# print initial board state
# print("Tic Tac Toe Game")
# print("-----------------")
# print(" 0 | 1 | 2 ")
# print("-----------")
# print(" 3 | 4 | 5 ")
# print("-----------")
# print(" 6 | 7 | 8 ")
# print("-----------------")
print_board = [str(i) if board[i] == " " else board[i] for i in range(len(board))]
print(
    f"Current Board: {print_board[0]}|{print_board[1]}|{print_board[2]}\n              -+-+-\n              {print_board[3]}|{print_board[4]}|{print_board[5]}\n              -+-+-\n              {print_board[6]}|{print_board[7]}|{print_board[8]}")

# loop until game ends
while True:
    # check if it is this client's turn
    turn_msg = client_socket.recv(1024).decode()
    if turn_msg == "YOUR_TURN":
        print("Your turn.")
        # get move from user
        while True:
            move = input("Enter move (0-8): ")
            if move.isdigit() and int(move) >= 0 and int(move) <= 8 and board[int(move)] == " ":
                break
            print("Invalid move.")
        # send move to server
        client_socket.send(str.encode(move))
    elif turn_msg == "OTHER_TURN":
        print("Waiting for other player's move...")
    elif turn_msg == "GAME_ENDED":
        print("Game ended.")
        # receive winner message from server
        winner_msg = client_socket.recv(1024).decode()
        if winner_msg == "PLAYER1":
            print("Player 1 wins!")
        elif winner_msg == "PLAYER2":
            print("Player 2 wins!")
        elif winner_msg == "TIE":
            print("Tie game.")
        else:
            print("Unexpected message received from server.")
        # close connection and exit
        client_socket.close()
        sys.exit()
    else:
        print("Unexpected message received from server.")
        client_socket.close()
        sys.exit()

    # receive updated board state from server
    board_str = client_socket.recv(1024).decode()
    #board = list(board_str)
    board = eval(board_str)

    # print updated board state
    print_board = [str(i) if board[i] == " " else board[i] for i in range(len(board))]
    print(
        f"Current Board: {print_board[0]}|{print_board[1]}|{print_board[2]}\n              -+-+-\n              {print_board[3]}|{print_board[4]}|{print_board[5]}\n              -+-+-\n              {print_board[6]}|{print_board[7]}|{print_board[8]}")
