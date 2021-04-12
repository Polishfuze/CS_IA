import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

def ReadMFRC522(debug=False):
    reader = SimpleMFRC522()

    try:
        id, text = reader.read()
        if debug:
            print(id)
            print(text)
    finally:
        GPIO.cleanup()
    return id, text

def Padder(data, debug=False):
    data = str(data)
    while len(data) < 48:
        data += ' '
    if debug:
        print(data)
    return data
    
if __name__ == '__main__':
    ReadMFRC522()