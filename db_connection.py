from pymongo import MongoClient

uri = "mongodb+srv://divyasangamesh790_db_user:oVYYwUsnkrSHGbTP@cluster0.3eaitxf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri)

client.admin.command("ping")
print("Connected to MongoDB Atlas!")