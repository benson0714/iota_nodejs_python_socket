import iota_client
import pymongo
import json
import hashlib

myclient = pymongo.MongoClient("mongodb://TestUser:password@140.120.40.132:27017/")
mydb = myclient["test"]
mycol = mydb["dht11_mongoDB_test"]

nodek = "http://127.0.0.1:14265"

client = iota_client.Client(
	nodes_name_password=[[nodek]])

# find the msgId of data
for x in mycol.find({},{"_id":0, "Time": 1, "Temp":1, "Humidity":1, "msgId":1 }):
    if(x["Time"] =='12/14/2022 23:28:07'):
        print("data in mongo = ")
        print(x)
        mongo_msg = x
        msgId = x["msgId"]
        del mongo_msg['msgId']
        break


# find message with index
metadata = client.get_message_data(msgId)
# print(metadata['payload']['indexation'][0]['data'])

# find data in message type object(type JSON)
metadata_list = metadata['payload']['indexation'][0]['data']

# replace hex to decimal and decode to utf-8
iota_hex_data = ' '.join(str(hex(e)) for e in metadata_list).replace(" ", "").replace("0x", "")
iota_utf_data = bytes.fromhex(iota_hex_data).decode('utf-8')
print("data in iota = \n"+iota_utf_data)

iota_msg = eval(iota_utf_data)
mongo_sha256_str = str(mongo_msg).replace(" ", "").encode('utf-8')
mongo_sha256 = hashlib.sha256(mongo_sha256_str).hexdigest()
if(mongo_sha256!=iota_msg["hash"]):
    print("資料遭竄改")
else:
    print("資料無遭竄改")