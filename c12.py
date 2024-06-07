import socket


def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 9999))

    account_number = input('Enter account number: ')
    pin = input('Enter PIN: ')
    client.send(f'{account_number},{pin}\n'.encode('utf-8'))

    response = client.recv(1024).decode('utf-8').strip()
    if response == 'Authenticated':
        print('Login successful!')
    else:
        print('Authentication failed!')
        client.close()
        return

    while True:
        print("\nOptions:\n1. Check Balance\n2. Deposit Money\n3. Withdraw Money\n4. Logout")
        choice = input("Enter choice: ")

        if choice == '1':
            client.send(b'BALANCE\n')
            response = client.recv(1024).decode('utf-8').strip()
            print(response)

        elif choice == '2':
            amount = input('Enter amount to deposit: ')
            client.send(f'DEPOSIT,{amount}\n'.encode('utf-8'))
            response = client.recv(1024).decode('utf-8').strip()
            print(response)

        elif choice == '3':
            amount = input('Enter amount to withdraw: ')
            client.send(f'WITHDRAW,{amount}\n'.encode('utf-8'))
            response = client.recv(1024).decode('utf-8').strip()
            print(response)

        elif choice == '4':
            client.send(b'LOGOUT\n')
            response = client.recv(1024).decode('utf-8').strip()
            print(response)
            break

        else:
            print('Invalid choice, please try again.')

    client.close()


if __name__ == '__main__':
    start_client()