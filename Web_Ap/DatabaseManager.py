import mysql.connector

db = mysql.connector.connect(
  host="pet-project.cqlvbpbplnsv.us-east-2.rds.amazonaws.com",
  user="admin",
  password="abir1971",
  database="automated_pet_door"
)

cursor = db.cursor()

dblist = cursor.execute("SHOW TABLES;")

for tables in cursor:
  print(tables)

print("completed")



