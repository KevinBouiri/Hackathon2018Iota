import requests
import sqlite3
from datetime import datetime
import RPi.GPIO as GPIO
from time import sleep

PIPin = 5
Gpin = 17
Rpin = 27
A = 18
B = 23
C = 24
D = 25
time = 0.005


# Schritte 1 - 8 festlegen
def Step1():
    GPIO.output(D, True)
    sleep(time)
    GPIO.output(D, False)


def Step2():
    GPIO.output(D, True)
    GPIO.output(C, True)
    sleep(time)
    GPIO.output(D, False)
    GPIO.output(C, False)


def Step3():
    GPIO.output(C, True)
    sleep(time)
    GPIO.output(C, False)


def Step4():
    GPIO.output(B, True)
    GPIO.output(C, True)
    sleep(time)
    GPIO.output(B, False)
    GPIO.output(C, False)


def Step5():
    GPIO.output(B, True)
    sleep(time)
    GPIO.output(B, False)


def Step6():
    GPIO.output(A, True)
    GPIO.output(B, True)
    sleep(time)
    GPIO.output(A, False)
    GPIO.output(B, False)


def Step7():
    GPIO.output(A, True)
    sleep(time)
    GPIO.output(A, False)


def Step8():
    GPIO.output(D, True)
    GPIO.output(A, True)
    sleep(time)
    GPIO.output(D, False)
    GPIO.output(A, False)


def toLeft():
    for i in range(128):
        Step8()
        Step7()
        Step6()
        Step5()
        Step4()
        Step3()
        Step2()
        Step1()


def toRight():
    for i in range(128):
        Step1()
        Step2()
        Step3()
        Step4()
        Step5()
        Step6()
        Step7()
        Step8()


def Led(x):
    if x == 0:
        GPIO.output(Rpin, 1)
        GPIO.output(Gpin, 0)
    if x == 1:
        GPIO.output(Rpin, 0)
        GPIO.output(Gpin, 1)


def Print(x):
    if x == 1:
        pass
        # print('*************************')
        # print('*   Light was blocked   *')
        # print('*************************')


def detect(chn):
    parkingspace(GPIO.input(PIPin))
    Print(GPIO.input(PIPin))


GPIO.setmode(GPIO.BCM)
GPIO.setup(Gpin, GPIO.OUT)     # Set Green Led Pin mode to output
GPIO.setup(Rpin, GPIO.OUT)     # Set Red Led Pin mode to output
GPIO.setup(PIPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V)
GPIO.setup(A, GPIO.OUT)
GPIO.setup(B, GPIO.OUT)
GPIO.setup(C, GPIO.OUT)
GPIO.setup(D, GPIO.OUT)
GPIO.output(A, False)
GPIO.output(B, False)
GPIO.output(C, False)
GPIO.output(D, False)
GPIO.add_event_detect(PIPin, GPIO.BOTH, callback=detect, bouncetime=200)

# Auto kommt
# REST Call fragt das Auto nach der ID
# GetOrCreate auf die Datenbank für die ID des Autos
#     + Timestamp
# (Prüfen ob das Auto geld hat)
# Schranke auf
# Das auto parkt
# Das auto fährt weg
# An der schranke bezahlen
#   Differrenz der Timespeps bilden für den Betrag
# IOTA Transaktion auslösen.
# Schannke geht auf, wenn die Transaktion fertig ist.

PI_CAR = 'https://iota-car.herokuapp.com'

parkingspace_is_free = True


def parkingspace(parkingspace_is_free):
    conn = sqlite3.connect('cars.db')
    c = conn.cursor()
    if parkingspace_is_free:
        print('Auto ist auf dem Parkplatz')
        GPIO.output(Rpin, 1)
        GPIO.output(Gpin, 0)
        # check ob die ein element in der lichtschranke ist
        # Identität des Autos erfragen
        r = requests.get(PI_CAR + '/identify')
        answer = r.json()['identity']
        print('Auto hat die IOTA ID: ' + str(answer))
        c.execute("INSERT INTO cars (address, timestamp) VALUES ('" + answer + "','" + str(datetime.now()) + "')")
        conn.commit()

    if not parkingspace_is_free:
        GPIO.output(Rpin, 0)
        GPIO.output(Gpin, 1)
        r = requests.get(PI_CAR + '/identify')
        answer = r.json()['identity']
        timestamp_des_parkens = c.execute("SELECT timestamp FROM cars WHERE address = '" + answer + "'").fetchall()[-1]
        # print(timestamp_des_parkens[0])
        start = datetime.strptime(timestamp_des_parkens[0], '%Y-%m-%d %H:%M:%S.%f')
        end = datetime.now()
        diff = end-start
        diff_minutes = diff.seconds/60
        print('Parkzeit: ' + str(round(diff_minutes, 2)) + '  Preis: ' + str(max(1.0, round(diff_minutes * 2.0))) + ' IOTA')
        print('Transaktion gestartet.')
        r = requests.get(PI_CAR + '/payments/' + answer + '/0')
        if r.json()['payment'] == 'OK':
            print("Transaktion Fertig")
            # Open der Schranke
            toLeft()
            sleep(2)
            toRight()
    conn.close()


while True:
    pass

GPIO.output(Gpin, GPIO.HIGH)       # Green led off
GPIO.output(Rpin, GPIO.HIGH)       # Red led off
GPIO.cleanup()
