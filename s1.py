import socket
import threading

# Predefined bank accounts (account number -> (PIN, balance))
accounts = {
    '12345': ('1111', 1000),
    '67890': ('2222', 2000),
}

# Lock for synchronizing access to account balances
lock = threading.Lock()


def handle_client(client_socket):
    try:
        authenticated = False
        account_number = None

        while True:
            request = client_socket.recv(1024).decode('utf-8').strip()
            if not request:
                break

            if not authenticated:
                account_number, pin = request.split(',')
                if account_number in accounts and accounts[account_number][0] == pin:
                    authenticated = True
                    client_socket.send(b'Authenticated\n')
                else:
                    client_socket.send(b'Authentication Failed\n')
                    break
            else:
                command, *args = request.split(',')

                with lock:
                    if command == 'BALANCE':
                        balance = accounts[account_number][1]
                        client_socket.send(f'Balance: {balance}\n'.encode('utf-8'))

                    elif command == 'DEPOSIT':
                        amount = float(args[0])
                        accounts[account_number] = (accounts[account_number][0], accounts[account_number][1] + amount)
                        client_socket.send(b'Deposit Successful\n')

                    elif command == 'WITHDRAW':
                        amount = float(args[0])
                        if accounts[account_number][1] >= amount:
                            accounts[account_number] = (
                            accounts[account_number][0], accounts[account_number][1] - amount)
                            client_socket.send(b'Withdrawal Successful\n')
                        else:
                            client_socket.send(b'Insufficient Funds\n')

                    elif command == 'LOGOUT':
                        balance = accounts[account_number][1]
                        client_socket.send(f'Final Balance: {balance}\n'.encode('utf-8'))
                        break
    finally:
        client_socket.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)
    print('Server listening on port 9999')

    while True:
        client_socket, addr = server.accept()
        print(f'Accepted connection from {addr}')
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == '__main__':
    start_server()