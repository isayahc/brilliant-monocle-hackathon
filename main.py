import touch
import display
import microphone
import bluetooth

def change_text(button):
    new_text = display.Text(f"Button {button} touched! Hello", 0, 0, display.WHITE)
    print("recording now")
    display.show(new_text)

# def record_voice(butt)

# touch.callback(touch.BOTH, change_text)

# initial_text = display.Text("Tap a touch button Hello", 0, 0, display.WHITE)
# display.show(initial_text)



if touch.callback(touch.A, callback):
    microphone.record(seconds=10.0,sample_rate=16000,bit_depth=16)


new_text = display.Text("tap a to begin recording", 0, 0, display.WHITE)
display.show(new_text)


if touch.A:
    print("recording now")
    display.show("recording now")
    data = microphone.record(seconds=5.0,sample_rate=16000,bit_depth=16)
    print(data)
    if touch.B:
        display.show("reading now")
        while microphone.read(127):
            print("recording now")

            print(microphone.read(127))


if touch.A == True:
    print("recording now")
    display.show("recording now")
    data = microphone.record(seconds=5.0,sample_rate=16000,bit_depth=16)
    print(data)
    if touch.B:
        display.show("reading now")
        while microphone.read(127):
            print("recording now")

            print(microphone.read(127))


while True:

    data = microphone.record(seconds=5.0,sample_rate=16000,bit_depth=16)
    # print(data)bluetooth.send(bytes)


microphone.record(seconds=5.0,sample_rate=16000,bit_depth=16)

bluetooth.send(microphone.read(127))