from time import sleep
import board
import digitalio
import wifi
import adafruit_requests
import socketpool
import ssl
# blinks in a tabe a - 1,1 b - 1,2
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT



try:
        # Connect to the WIFI, use settings.toml to configure SSID and Password
    wifi.radio.connect("VIVACOM_FiberNet","adff55c0")
    print("Connected to WiFi")

except Exception as e:
        # Handle connection error
        # For this example we will simply print a message and exit the program
    print("Failed to connect, adorting.")
    print("Error:\n", str(e))

def make_request():
#     pool = socketpool.SocketPool(wifi.radio)
#     requests = adafruit_requests.Session(pool, ssl.create_default_context())
#     time_response = requests.get(url='http://time.jsontest.com/')
#     json_time_response = time_response.json()
#     print()
#     print('UTC time')
#     print(json_time_response)
#     sleep(10)
#     return json_time_response
    data = []
    word = "aa"
    for char in word:
        row  = (ord(char) - 96) // 5 + 1
        column = (ord(char) - 96) - row * 5 + 5
        data.append([row,column])
    print(data)
    return [[2,3],[2,4]]

def blink(rate):
    led.value = True
    sleep(rate)
    led.value = False
    sleep(rate)


def pause_inbetween_signal(time):
    sleep(time)


def blinker(rate, pause, type_of_signal, end_of_signal_time):
    for i in range(0, type_of_signal[0]):
        print("row")
        blink(rate)
    pause_inbetween_signal(pause)
    for i in range(0, type_of_signal[1]):
        print("column")
        blink(rate)
    pause_inbetween_signal(end_of_signal_time)

while True:
    sentence = make_request()
    for i in sentence:
        blinker(rate=1, pause=3, type_of_signal=i, end_of_signal_time=10)
    print("hi")