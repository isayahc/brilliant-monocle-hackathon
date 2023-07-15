import touch
import display
import time
# import whisper

def change_text(button):
    new_text = display.Text(f"Button {button} touched! adding on", 0, 0, display.WHITE)
    display.show(new_text)

def record_voice():
    # button a is start record 
    # button b is end record

    a1 = time.ticks_ms()
    a2 = time.ticks_ms()
    a3 = time.ticks_diff(a1,a2)

    return microphone.read(8000*(a3//1000))


def save_byte_to_data(data,output='output.mp3'):
    with open(output, 'wb') as f:
        f.write(data)

# def speech_to_text(model_type="base",input_data="output.mp3") -> str:
#     model = whisper.load_model(model_type)
#     result = model.transcribe(input_data)
#     return (result["text"])
        

    



# microphone.record(seconds=5.0,sample_rate=16000,bit_depth=16)

# touch.callback(touch.BOTH, change_text)

# initial_text = display.Text("Tap a touch button", 0, 0, display.WHITE)
# display.show(initial_text)

print("record data")
data = record_voice()
# print("saving data")
# save_byte_to_data(data)