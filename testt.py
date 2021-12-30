import pymongo

# connect
db_client = pymongo.MongoClient("mongodb+srv://manuallyenglish:sshdfkj36457.@manuallyeng.zj2ei.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")


# create or connect to database
current_db = db_client["test"]

# create or connect to collection(table)
collection = current_db["man_eng_users"]

# print(current_db.list_collection_names())
doc = {"user_name": "Georg", "user_id": 234354235, "added_date": "30.12.2021"}

collection.insert_one(document=doc)
# collection.insert_many(doc)
# param = {"user_name": "Adam"}
# collection.delete_one(param)