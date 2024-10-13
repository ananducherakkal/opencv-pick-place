#in this lab you create a server on the python side
import socket
from Coordinates import *

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Set socket listening port. To find the robot adress use cmd and type ipconfig in the terminal, there you see the ip of the robot. 
#you may have to open the port in the firewall as well. Note that the ip adress is 127.0.0.1 if you run via Robotstudio
server_socket.bind(('192.168.125.201', 5000))
#Set up the server
#listen to incomming client connection
server_socket.listen()
print("Looking for client")
#accept and store incomming socket connection
(client_socket, client_ip) = server_socket.accept()
print(f"Robot at address {client_ip } connected.")

while True:
    color = client_socket.recv(4094).decode('utf-8')
    client_socket.send("color received".encode("UTF-8"))
    trackbar_type = client_socket.recv(4094).decode('utf-8')
    coordinates = get_coordinates(color=color, trackbar_type=trackbar_type)
    if coordinates:
        for coordinate in coordinates:
            print("Executing: ", coordinate )
            client_socket.send(str(coordinate["x"]).encode("UTF-8"))
            client_socket.recv(4094)
            client_socket.send(str(coordinate["y"]).encode("UTF-8"))
            client_socket.recv(4094)
            client_socket.send(str(coordinate["angle"]).encode("UTF-8"))
            client_socket.recv(4094)
    client_socket.send("execute".encode("UTF-8"))
    client_socket.recv(4094)
    user_input = input("exit?")
    if user_input == "yes":
        break