import touch
import display
import time
import microphone
import bluetooth

def change_text(button):
    new_text = display.Text(f"Button {button} touched! adding on", 0, 0, display.WHITE)
    display.show(new_text)

def record_voice():
    # button a is start record 
    # button b is end record
    # touch.A
    
    a1 = time.ticks_ms()
    a2 = time.ticks_ms()
    a3 = time.ticks_diff(a1,a2)

    return microphone.read(8000*(a3//1000))


def touch_callback(pad):
    if pad == touch.A:
        microphone.record(seconds=5.0,sample_rate=8000,bit_depth=8)

def sample():
    # microphone.record(seconds=10.0,sample_rate=16000,bit_depth=16)
    microphone.record(seconds=10.0,sample_rate=8000,bit_depth=8)

    data = b''
    while microphone.read(127):
        data += microphone.read(127)
    return data

def sample():
    # microphone.record(seconds=10.0,sample_rate=16000,bit_depth=16)
    microphone.record(seconds=10.0,sample_rate=8000,bit_depth=8)

    data = b''
    while microphone.read(127):
        data += microphone.read(127)
    return data

def bluetooth_sample(data):
    import bluetooth
    bluetooth.send(data)


def save_byte_to_data(data,output='output.mp3'):
    with open(output, 'wb') as f:
        f.write(data)


def bluetooth_send_message(message):
    while True:
        try:
            bluetooth.send(message)
            break
        except OSError:
            pass





# microphone.record(seconds=5.0,sample_rate=16000,bit_depth=16)

# touch.callback(touch.BOTH, change_text)

# initial_text = display.Text("Tap a touch button", 0, 0, display.WHITE)
# display.show(initial_text)

print("record data")
data = record_voice()
# print("saving data")
# save_byte_to_data(data)

if __name__ == '__main__':
    # if touch.A:
    #         a1 = time.ticks_ms()
    #         while not touch.B:
    #             continue
    #             if:
    #                 a2 = time.ticks_ms()
    #                 a3 = time.ticks_diff(a1,a2)
    x = sample()
    print(x)


    # return microphone.read(8000*(a3//1000))