import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

def WriteMFRC522(data = '', debug=False):
    reader = SimpleMFRC522()
    if not data:
        data= input('New data: ')
    try:
        if debug:
            print("Now place your tag to write")
        reader.write(data)
        if debug:
            print("Written")
    finally:
        GPIO.cleanup()
        
        
        
if __name__ == '__main__':
    WriteMFRC522(data='-953851664')
