import socket
import Adafruit_DHT
import time
import json
import pymongo
import bson.json_util as json_util
import hashlib

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
            iota_dict = data_dict.copy()
            mongo_dict = data_dict.copy()

            # hash data and insert to dict
            iota_sha256 = sha256_encrypt(json.dumps(data_dict))
            iota_dict['hash'] = iota_sha256

            # change dict to string
            iota_data_str = json.dumps(iota_dict)
            
            # send data to nodejs for upload to iota
            msgId = socket_client(iota_data_str)

            # add msgId to mongo_dict and upload to mongoDB
            mongo_dict['msgId'] = msgId
            mongoDB_upload(json.loads(json_util.dumps(mongo_dict)))




def socket_client(data):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    print('send: ' + data)
    s.send(data.encode())

    indata = s.recv(1024)
    print('recv: ' + indata.decode())

    s.close()
    return indata.decode()

def mongoDB_upload(data):
    myclient = pymongo.MongoClient("mongodb://TestUser:password@140.120.40.132:27017/")
    mydb = myclient["test"]
    dblst = myclient.list_database_names()
    mycol = mydb["dht11_mongoDB_test"]
    collst = mydb.list_collection_names()
    x = mycol.insert_one(data)

# sha256
def sha256_encrypt(data):
    iota_sha256_str = data.replace(" ", "").encode('utf-8')
    iota_sha256 = hashlib.sha256(iota_sha256_str).hexdigest()
    print("iota_sha256 = "+iota_sha256)
    return iota_sha256

if __name__ == '__main__':
    dht11_collect()