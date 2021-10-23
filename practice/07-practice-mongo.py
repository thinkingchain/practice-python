import pymongo
 
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["newcoins-test"]
mycol = mydb["contracts-test"] 
mydict = { "name": "RUNOOB", "alexa": "10000", "url": "https://www.runoob.com" }
#x = mycol.insert_one(mydict) 
#print(x) 

cursor = mycol.find({})

record = next(cursor, None)
if record:
      print(record["name"])
