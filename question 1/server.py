import socket
import threading

# Pre-defined bank accounts with balances
accounts = {
    "Zahraa": {"password": "11", "balance": 500},
    "Ruky": {"password": "22", "balance": 550},
    "x": {"password": "33", "balance": 600}
}


# Function to handle each client
def handle_client(client_socket, client_address):
    print(f"New client connected from {client_address}")

    authenticated = False
    account_name = ""

    while not authenticated:
        client_socket.send("Enter your account name and password (space-separated): ".encode())
        credentials = client_socket.recv(1024).decode().strip().split()

        if len(credentials) == 2:
            account_name, password = credentials
            if account_name in accounts and accounts[account_name]["password"] == password:
                authenticated = True
                client_socket.send("Authentication successful.\n".encode())
            else:
                client_socket.send("Invalid account name or password. Try again.\n".encode())
        else:
            client_socket.send("Invalid input. Try again.\n".encode())

    while True:
        client_socket.send("Choose an option (1: Check Balance, 2: Deposit, 3: Withdraw, 4: Quit): ".encode())
        option = client_socket.recv(1024).decode().strip()

        if option == "1":
            balance = accounts[account_name]["balance"]
            client_socket.send(f"Your balance is: {balance:.2f}\n".encode())
        elif option == "2":
            client_socket.send("Enter amount to deposit: ".encode())
            amount = float(client_socket.recv(1024).decode().strip())
            accounts[account_name]["balance"] += amount
            client_socket.send(
                f"Deposit successful. New balance is: {accounts[account_name]['balance']:.2f}\n".encode())
        elif option == "3":
            client_socket.send("Enter amount to withdraw: ".encode())
            amount = float(client_socket.recv(1024).decode().strip())
            if amount > accounts[account_name]["balance"]:
                client_socket.send("Insufficient funds.\n".encode())
            else:
                accounts[account_name]["balance"] -= amount
                client_socket.send(
                    f"Withdrawal successful. New balance is: {accounts[account_name]['balance']:.2f}\n".encode())
        elif option == "4":
            client_socket.send(f"Final balance is: {accounts[account_name]['balance']:.2f}\nGoodbye!\n".encode())
            break
        else:
            client_socket.send("Invalid option. Try again.\n".encode())

    client_socket.close()
    print(f"Client from {client_address} disconnected.")


# Create and start the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server_socket.bind(('0.0.0.0', 5555))
server_socket.listen()

print("Server started. Waiting for client connections...")

while True:
    client_socket, client_address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()