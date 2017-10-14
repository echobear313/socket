import socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# client_socket.bind(("localhost", 23001))
address = ("localhost", 23000)
client_socket.connect(address)
messages = []
