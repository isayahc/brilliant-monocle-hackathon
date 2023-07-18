import bluetooth

# Specify the Bluetooth device address
device_address = ' CD:D3:CD:60:0F:63'  # Replace with the actual device address

# Specify the Bluetooth service UUID
# service_uuid = bluetooth.UUID('00001101-0000-1000-8000-00805F9B34FB')  # Replace with the desired service UUID

# Create a Bluetooth socket
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

try:
    # Connect to the Bluetooth device
    sock.connect((device_address, 1))  # 1 is the port number used for RFCOMM

    # Receive data from the device
    while True:
        data = sock.recv(1024)
        if len(data) == 0:
            break
        print("Received:", data.decode())
except bluetooth.btcommon.BluetoothError as err:
    print("Bluetooth connection error:", err)
finally:
    # Close the Bluetooth socket
    sock.close()
