import bluetooth as tooth

# the MAC address of the device (you need to know this beforehand)
target_address = "00:00:00:00:00:00"

# Create the client socket
client_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

try:
    client_socket.connect((target_address, 1))
    print("Connected Successfully!")

    # now you can send or receive data
    client_socket.send("Hello World!")

except bluetooth.btcommon.BluetoothError as err:
    # Error handler
    print("An error occurred ", err)
    pass

# remember to close the connection
client_socket.close()
