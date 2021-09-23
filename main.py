"""
@author: Cem Akpolat
@created by cemakpolat at 2021-09-13
"""

import serial
import time, dbface


def is_card_permitted(cardid, doorid):
    doors = dbface.get_authorized_doors(cardid, dbface.get_connection(dbface.DB_NAME))
    for item in doors:
        if doorid == item:
            return True
    return False


# arduino = serial.Serial(port='COM4', baudrate=115200, timeout=.1)


def write_read(x):
    # arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    # data = arduino.readline()
    # return data
    pass


while True:
    num = input("Enter a number: ")  # Taking input from user
    num = is_card_permitted('AABBDD',num)
    # value = write_read(num)
    print(num)  # printing the value

