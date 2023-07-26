import touch
import microphone
import bluetooth
import time

recording = False

# Define the touch callback function which is triggered upon a touch event
def fn(arg):
    global recording
    if arg == touch.A:
        print("Button A pressed! Starting recording...")
        microphone.record(seconds=4.0, bit_depth=8, sample_rate=8000)
        time.sleep(0.5)  # A short time is needed to let the FPGA prepare the buffer
        recording = True
    if arg == touch.B and recording:
        print("Button B pressed! Stopping recording...")
        while True:
            chunk = microphone.read(100)
            if chunk == None:
                time.sleep(1)
                break
            while True:
                try:
                    bluetooth.send(chunk)
                    break
                except OSError:
                    pass
        recording = False

touch.callback(touch.BOTH, fn)  # Attaches the same callback to both of the touch pads