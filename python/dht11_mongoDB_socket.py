import socket
import Adafruit_DHT
import time
import json

# dht11 object and raspi pin
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

# socket server host
HOST = '0.0.0.0'
PORT = 15768

def dht11_collect():
    while True:
        humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
        if humidity is not None and temperature is not None:
            # 取得 struct_time 格式的時間
            t = time.localtime()
            # 依指定格式輸出
            now_time = time.strftime("%m/%d/%Y %H:%M:%S", t)
            print(now_time)
            print("Temp={0:0.1f}C Humidity={1:0.1f}".format(temperature, humidity))
            data_dict = {"Time":now_time, "Temp":temperature, 'Humidity': humidity}
            data_str = json.dumps(data_dict)
            print(data_str)

            # send data to nodejs for upload to iota
            socket_client(data_str)


def socket_client(data):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    print('send: ' + data)
    s.send(data.encode())

    indata = s.recv(1024)
    print('recv: ' + indata.decode())

    s.close()

if __name__ == '__main__':
    dht11_collect()